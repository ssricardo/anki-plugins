# -*- coding: utf-8 -*-
# Main interface between Anki and this addon components
# -------------------------------------------------------

# Holds references so GC does kill them
controllerInstance = None

from config import Config
from notemenu import NoteMenuHandler
import browser
import anki
import json

from aqt.editor import Editor
from aqt.reviewer import Reviewer

def run():
    global controllerInstance
    
    from aqt import mw    
    from notemenu import ankiSetup

    print('Setting anki-web-browser controller')
    
    ankiSetup()
    NoteMenuHandler.setOptions(Config.providers)
    controllerInstance = Controller(mw)
    controllerInstance.setupBindings()

    if True:    # FIXME
        from aqt.utils import showInfo, tooltip, showWarning
        controllerInstance.openInBrowser('https://google.com/search?q={}', 'api-test', None)


class Controller:
    """
        The mediator/adapter between Anki with its components and this addon specific API
    """

    _browser = None
    _editorReference = None
    _currentNote = None
    _ankiMw = None    

    def __init__(self, ankiMw):
        NoteMenuHandler.setController(self)
        self._browser = browser.AwBrowser(None)
        self._browser.setSelectionListener(self)
        self._ankiMw = ankiMw

    def setupBindings(self):
        anki.hooks.addHook('EditorWebView.contextMenuEvent', self.onEditorHandle)
        anki.hooks.addHook('AnkiWebView.contextMenuEvent', self.onReviewerHandle)

        Reviewer.nextCard = self.wrapOnCardShift(Reviewer.nextCard)
        Editor.loadNote = self.wrapOnCardShift(Editor.loadNote)

    def isEditing(self):
        'Checks anki current state. Whether is editing or not'

        return True if (self._ankiMw and self._editorReference) else False


    def wrapOnCardShift(self, originalFunction, *args):
        """
        Listens when the current showed card is changed. Either in Reviewer or Editor.
        Send msg to browser to cleanup its state"""

        def wrapped(args):
            originalFunction(args)

            if not self._browser:
                return

            if self.isEditing():
                if self._currentNote == self._editorReference.note:
                    return

            self._browser.unload()
            if not Config.keepBrowserOpened:
                self._browser.close()
                

        return wrapped

# ---------------------------------- Events listeners ---------------------------------

    def onEditorHandle(self, webView, menu):
        """
            Wrapper to the real context menu handler on the editor;
            Also holds a reference to the editor
        """

        self._editorReference = webView.editor
        NoteMenuHandler.onEditorMenu(webView, menu)        

    def onReviewerHandle(self, webView, menu):
        """
            Wrapper to the real context menu handler on the reviewer;
            Cleans up editor reference
        """

        self._editorReference = None
        note = self._ankiMw.reviewer.card.note()
        NoteMenuHandler.onReviewerMenu(webView, menu, note)

    def onEditorLoadNote(self, focusTo = False):
        print('Loading note...')

    def onReviewerNext(self):
        print('Reviewing next card...')

# ---------------------------------- --------------- ---------------------------------
    def openInBrowser(self, website, query, note, isEditMode = False):
        """
            Setup enviroment for web browser and invoke it
        """

        self._currentNote = note
        print('OpenInBrowser: {} ({})'.format(note, self.isEditing()))
        
        if self.isEditing():
            fieldList = note.model()['flds']
            fieldsNames = {ind: val for ind, val in enumerate(map(lambda i: i['name'], fieldList))}
            self._browser.setFields(fieldsNames)
        else:
            self._browser.setFields(None)   # clear fields

        self._browser.open(website, query)

    def handleSelection(self, fieldIndex, value, isUrl = False):
        """
            Callback from the web browser. 
            Invoked when there is a selection coming from the browser. It need to be delivered to a given field
        """

        if self._currentNote != self._editorReference.note:
            showWarning('Inconsistent state found. The current note is not the same as the Web Browser reference. No update will be done!')
            return

        self._editorReference.currentField = fieldIndex

        if isUrl:
            self.handleUrlSelection(fieldIndex, value)
        else:
            self.handleTextSelection(fieldIndex, value)        

    def handleUrlSelection(self, fieldIndex, value):
        """
        Imports an image from the link 'value' to the collection. 
        Adds this new image tag to the given field in the current note"""

        url = value.data()
        imgReference = self._editorReference.urlToLink(url)

        self._editorReference.web.eval("focusField(%d);" % fieldIndex)
        self._editorReference.web.eval("setFormat('inserthtml', %s);" % json.dumps(imgReference))

    def handleTextSelection(self, fieldIndex, value):
        'Adds the selected value to the given field of the current note'

        newValue = self._currentNote.fields[fieldIndex] + '\n ' + value
        self._currentNote.fields[fieldIndex] = newValue
        self._editorReference.setNote(self._currentNote)