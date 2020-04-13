# -*- coding: utf-8 -*-
# Main interface between Anki and this addon components

# This files is part of anki-web-browser addon
# @author ricardo saturnino
# ------------------------------------------------

from anki.hooks import addHook
from aqt import mw
from aqt.qt import QAction
from aqt.reviewer import Reviewer
from aqt.utils import tooltip, showWarning, openLink

from .base_controller import BaseController
from .browser import AwBrowser
from .config import service as cfg
from .core import Feedback
from .editor_controller import EditorController
from .exception_handler import exceptionHandler
from .no_selection import NoSelectionResult

# Holds references so GC doesnt kill them
controllerInstance = None
editorCtrl = None

@staticmethod
def _ankiShowInfo(*args):
    tooltip(args, 3500)

@staticmethod
def _ankiShowError(*args):
    showWarning(str(args))

def run():
    global controllerInstance, editorCtrl
    
    Feedback.log('Setting anki-web-browser controller')
    Feedback.showInfo = _ankiShowInfo
    Feedback.showError = _ankiShowError
    Feedback.showWarn = lambda args: tooltip('<b>Warning</b><br />' + args, 7500)
    BaseController.openExternalLink = openLink

    cfg.getConfig()  # Load config
    controllerInstance = ReviewController(mw)
    controllerInstance.setupBindings()

    editorCtrl = EditorController(mw)

    if cfg.firstTime:
        controllerInstance.browser.welcome()

# ----------------------------------------------------------------------------------

class ReviewController(BaseController):
    """
        The mediator/adapter between Anki with its components and this addon specific API
    """

    browser = None
    _lastProvider = None

    def __init__(self, ankiMw):
        super(ReviewController, self).__init__(ankiMw)
        self.browser = AwBrowser.singleton(ankiMw.web, cfg.getInitialWindowSize())
        self.browser.setSelectionHandler(None)

    def setupBindings(self):
        addHook('AnkiWebView.contextMenuEvent', self.onReviewerHandle)

        Reviewer.nextCard = self.wrapOnCardShift(Reviewer.nextCard)
        Reviewer._shortcutKeys = self.wrap_shortcutKeys(Reviewer._shortcutKeys)

        # Add config to menu
        action = QAction("Anki-Web-Browser Config", self._ankiMw)
        action.triggered.connect(self.openConfig)
        self._ankiMw.form.menuTools.addAction(action)

    def openConfig(self):
        from .config import ConfigController
        cc = ConfigController(self._ankiMw)
        cc.open()

    def wrapOnCardShift(self, originalFunction):
        """
        Listens when the current showed card is changed, in Reviewer.
        Send msg to browser to cleanup its state"""

        ref = self

        def wrapped(self, focusTo=None):
            Feedback.log('Browser - CardShift')

            originalResult = None
            if focusTo:
                originalResult = originalFunction(self, focusTo)
            else:
                originalResult = originalFunction(self)

            if not ref.browser:
                return
            
            ref.browser.clearContext()
            if not cfg.getConfig().keepBrowserOpened:
                ref.browser.close()

            if ref._ankiMw.reviewer and ref._ankiMw.reviewer.card:
                ref._currentNote = ref._ankiMw.reviewer.card.note()

            return originalResult

        return wrapped


    def wrap_shortcutKeys(self, fn):
        ref = self

        def customShortcut(self):
            sList = fn(self)
            sList.append((cfg.getConfig().menuShortcut, \
                lambda: ref.createReviewerMenu(
                    ref._ankiMw.web, ref._ankiMw.web)))

            sList.append( (cfg.getConfig().repeatShortcut, ref._repeatProviderOrShowMenu ) )
            return sList

        return customShortcut

# --------------------------------------------------------------------------

    @exceptionHandler
    def _repeatProviderOrShowMenu(self):
        if not self._lastProvider:
            return self.createReviewerMenu(self._ankiMw.web, self._ankiMw.web)

        webView = self._ankiMw.web
        super()._repeatProviderOrShowMenu(webView)

    def handleProviderSelection(self, result):
        Feedback.log('Handle provider selection')
        webview = self._ankiMw.web
        query = self._getQueryValue(webview)
        self._lastProvider = result
        if not query:
            return
        Feedback.log('Query: %s' % query)        
        self.openInBrowser(query)

    @exceptionHandler
    def createReviewerMenu(self, webView, menu):
        """Handles context menu event on Reviewer"""

        self._providerSelection.showCustomMenu(menu, self.handleProviderSelection)

    # TODO: move parts to superclass / adapt
    def _getQueryValue(self, webview):
        Feedback.log('getQueryValue', webview, self._currentNote)
        if webview.hasSelection():
            return self._filterQueryValue(webview.selectedText())

        if self._noSelectionHandler.isRepeatOption():
            noSelectionResult = self._noSelectionHandler.getValue()
            if noSelectionResult.resultType == NoSelectionResult.USE_FIELD:
                if noSelectionResult.value < len(self._currentNote.fields):
                    Feedback.log('USE_FIELD {}: {}'.format(noSelectionResult.value, self._currentNote.fields[noSelectionResult.value]))
                    return self._filterQueryValue(self._currentNote.fields[noSelectionResult.value])

        return None

    def handleNoSelectionResult(self, resultValue: NoSelectionResult):
        if not resultValue or \
                resultValue.resultType in (NoSelectionResult.NO_RESULT, NoSelectionResult.SELECTION_NEEDED):
            Feedback.showInfo('No value selected')
            return
        value = resultValue.value
        if resultValue.resultType == NoSelectionResult.USE_FIELD:
            value = self._currentNote.fields[resultValue.value]
            value = self._filterQueryValue(value)
            Feedback.log('USE_FIELD {}: {}'.format(resultValue.value, value))

        return self.openInBrowser(value)
    

# ---------------------------------- Events listeners ---------------------------------

    def onReviewerHandle(self, webView, menu):
        """
            Wrapper to the real context menu handler on the reviewer;
        """

        if self._ankiMw.reviewer and self._ankiMw.reviewer.card:
            self.createReviewerMenu(webView, menu)

    def beforeOpenBrowser(self):
        self.browser.setFields(None)   # clear fields
        self.browser.setInfoList(['No action available on Reviewer mode'])

