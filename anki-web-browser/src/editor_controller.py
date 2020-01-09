# ---------------------------------- ================ ---------------------------------
# ---------------------------------- Editor Control -----------------------------------
# ---------------------------------- ================ ---------------------------------

from .config import service as cfg
from .core import Feedback
from .browser import AwBrowser
from .no_selection import NoSelectionController, NoSelectionResult
from .provider_selection import ProviderSelectionController

from aqt.editor import Editor
from anki.hooks import addHook
from aqt.utils import openLink
import json

class EditorController:
    _browser = None
    _editorReference = None
    _currentNote = None
    _ankiMw = None
    _lastProvider = None
    _noSelectionHandler = None

    def __init__(self, ankiMw):
        self._browser = AwBrowser.singleton(ankiMw)
        self._browser.setSelectionHandler(self.handleSelection)
        self._ankiMw = ankiMw
        self._noSelectionHandler = NoSelectionController(ankiMw)
        self._providerSelection = ProviderSelectionController()
        self.setupBindings()

# ------------------------ Anki interface ------------------

    def setupBindings(self):
        addHook('EditorWebView.contextMenuEvent', self.onEditorHandle)
        addHook("setupEditorShortcuts", self.setupShortcuts)

        Editor.loadNote = self.wrapOnLoadNote(Editor.loadNote)


    def wrapOnLoadNote(self, originalFunction):
        """
        Listens when the current showed card is changed. 
        Send msg to browser to cleanup its state"""

        ref = self
        def wrapped(self, focusTo=None):

            if focusTo:
                originalFunction(self, focusTo)
            else:
                originalFunction(self)

            if not ref._browser:
                return

            if ref._currentNote == ref._editorReference.note:
                return
            
            ref._currentNote = ref._editorReference.note
            ref._browser.unload()
            if not cfg.getConfig().keepBrowserOpened:
                ref._browser.close()

        return wrapped


    def onEditorHandle(self, webView, menu):
        """
            Wrapper to the real context menu handler on the editor;
            Also holds a reference to the editor
        """

        self._editorReference = webView.editor
        self.createEditorMenu(menu, self.handleProviderSelection)


    def setupShortcuts(self, scuts:list, editor):
        self._editorReference = editor
        scuts.append((cfg.getConfig().menuShortcut, self._showBrowserMenu))
        scuts.append((cfg.getConfig().repeatShortcut, self._repeatProviderOrShowMenu))

# ------------------------ Addon operation -------------------------

    def _showBrowserMenu(self, parent = None):
        if not parent:
            parent = self._editorReference

        self.createEditorMenu(parent.web, self.handleProviderSelection)


    def _repeatProviderOrShowMenu(self):
        webView = self._editorReference.web
        if not self._lastProvider:
            return self.createEditorMenu(webView, self.handleProviderSelection)

        query = self._getQueryValue(webView)
        if not query:
            return
        self.openInBrowser(query)

    
    def createEditorMenu(self, parent, menuFn):
        """ Deletegate the menu creation and work related to providers """

        return self._providerSelection.showCustomMenu(parent, menuFn)

    def handleProviderSelection(self, result):
        if not self._editorReference:
            raise Exception('Illegal state found. It was not possible to recover the reference to Anki editor')
        webview = self._editorReference.web
        query = self._getQueryValue(webview)
        self._lastProvider = result
        if not query:
            return
        Feedback.log('Query: %s' % query)
        self._currentNote = self._editorReference.note
        self.openInBrowser(query)


    def _getQueryValue(self, webview):
        if webview.hasSelection():
            return webview.selectedText()

        if self._noSelectionHandler.isRepeatOption():
            noSelectionResult = self._noSelectionHandler.getValue()
            if noSelectionResult.resultType == NoSelectionResult.USE_FIELD:
                self._editorReference.currentField = noSelectionResult.value

                Feedback.log('USE_FIELD {}: {}'.format(noSelectionResult.value, self._currentNote.fields[result]))
                return self._currentNote.fields[noSelectionResult.value]
        else:
            note = webview.editor.note
            fieldList = note.model()['flds']
            fieldsNames = {ind: val for ind, val in enumerate(map(lambda i: i['name'], fieldList))}
            self._noSelectionHandler.setFields(fieldsNames)
            self._noSelectionHandler.handle(self.handleNoSelectionResult)

        return None

    def handleNoSelectionResult(self, resultValue: NoSelectionResult):
        if not resultValue or \
                resultValue.resultType in (NoSelectionResult.NO_RESULT, NoSelectionResult.SELECTION_NEEDED):
            Feedback.showInfo('No value selected')
            return
        value = resultValue.value
        if resultValue.resultType == NoSelectionResult.USE_FIELD:
            self._editorReference.currentField = resultValue.value    # fieldIndex
            value = self._currentNote.fields[resultValue.value]
            Feedback.log('USE_FIELD {}: {}'.format(resultValue.value, value))

        return self.openInBrowser(value)

# ---------------------------------- --------------- ---------------------------------
    def openInBrowser(self, query):
        """
            Setup enviroment for web browser and invoke it
        """

        website = self._lastProvider
        note = self._currentNote
        
        Feedback.log('OpenInBrowser: %s < %s' % (query, website))

        if cfg.getConfig().useSystemBrowser:
            target = self._browser.formatTargetURL(website, query)
            openLink(target)
            return
        
        fieldList = note.model()['flds']
        fieldsNames = {ind: val for ind, val in enumerate(map(lambda i: i['name'], fieldList))}
        self._browser.infoList = ['No action available', 'Required: Text selected or link to image']
        self._browser.setFields(fieldsNames)
        self._browser.open(website, query)


    def handleSelection(self, fieldIndex, value, isUrl = False):
        """
            Callback from the web browser. 
            Invoked when there is a selection coming from the browser. It needs to be delivered to a given field
        """

        if self._currentNote != self._editorReference.note:
            Feedback.showWarn("""Inconsistent state found. 
            The current note is not the same as the Web Browser reference. 
            Try closing and re-opening the browser""")
            return

        self._editorReference.currentField = fieldIndex

        if isUrl:
            self.handleUrlSelection(fieldIndex, value)
        else:
            self.handleTextSelection(fieldIndex, value)

    def handleUrlSelection(self, fieldIndex, value):
        """
        Imports an image from the link 'value' to the collection. 
        Adds this new img tag to the given field in the current note"""

        url = value.toString() if value else ''
        Feedback.log("Selected from browser: {} || ".format(url))

        imgReference = self._editorReference.urlToLink(url)        

        if (not imgReference) or not imgReference.startswith('<img'):
            Feedback.showWarn('URL invalid! Only URLs with references to image files are supported (ex: http://images.com/any.jpg,  any.png)')
            return

        Feedback.log('handleUrlSelection.imgReference: ' + imgReference)

        self._editorReference.web.eval("focusField(%d);" % fieldIndex)
        self._editorReference.web.eval("setFormat('inserthtml', %s);" % json.dumps(imgReference))

    def handleTextSelection(self, fieldIndex, value):
        'Adds the selected value to the given field of the current note'

        newValue = self._currentNote.fields[fieldIndex] + '\n ' + value
        self._currentNote.fields[fieldIndex] = newValue
        self._editorReference.setNote(self._currentNote)
