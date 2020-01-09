# -*- coding: utf-8 -*-
# Main interface between Anki and this addon components

# This files is part of anki-web-browser addon
# @author ricardo saturnino
# ------------------------------------------------

from .config import service as cfg
from .core import Feedback
from .browser import AwBrowser
from .editor_controller import EditorController
from .provider_selection import ProviderSelectionController
from .exception_handler import exceptionHandler

import anki
import json

from aqt.reviewer import Reviewer
from aqt.qt import QAction
from aqt.utils import showInfo, tooltip, showWarning, openLink
from anki.hooks import addHook
from aqt import mw

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
        
    controllerInstance = Controller(mw)
    controllerInstance.setupBindings()

    editorCtrl = EditorController(mw)

    if cfg._firstTime:
        controllerInstance.browser.welcome()

# ----------------------------------------------------------------------------------

class Controller:
    """
        The mediator/adapter between Anki with its components and this addon specific API
    """

    browser = None
    _currentNote = None
    _ankiMw = None
    _lastProvider = None

    def __init__(self, ankiMw):
        self.browser = AwBrowser.singleton(ankiMw)
        self.browser.setSelectionHandler(None)
        self._ankiMw = ankiMw
        self._providerSelection = ProviderSelectionController()


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

            if focusTo:
                originalFunction(self, focusTo)
            else:
                originalFunction(self)

            if not ref.browser:
                return
            
            ref.browser.unload()
            if not cfg.getConfig().keepBrowserOpened:
                ref.browser.close()

            if (ref._ankiMw.reviewer and ref._ankiMw.reviewer.card):
                self._currentNote = ref._ankiMw.reviewer.card.note()

        return wrapped


    def wrap_shortcutKeys(self, fn):
        ref = self

        def customShortcut(self):
            sList = fn(self)
            sList.append( (cfg.getConfig().menuShortcut, \
                lambda: ref.createReviewerMenu(
                    ref._ankiMw.web, ref._ankiMw.web, ref.openInBrowser)) )

            sList.append( (cfg.getConfig().repeatShortcut, ref._repeatProviderOrShowMenu ) )
            return sList

        return customShortcut

    @exceptionHandler
    def _repeatProviderOrShowMenu(self):
        if not self._lastProvider:
            return self.createReviewerMenu(self._ankiMw.web, self._ankiMw.web, self.openInBrowser)

        webView = self._ankiMw.web
        if not webView.hasSelection():
            return
        query = webView.selectedText()
        self.openInBrowser(self._lastProvider, query)

    @exceptionHandler
    def createReviewerMenu(self, webView, menu, menuFn):
        'Handles context menu event on Reviewer'

        note = self._currentNote
        if not webView.hasSelection():
            return
        query = webView.selectedText()

        if not query:
            return

        self._providerSelection.showCustomMenu(menu)
    

# ---------------------------------- Events listeners ---------------------------------

    def onReviewerHandle(self, webView, menu):
        """
            Wrapper to the real context menu handler on the reviewer;
            Cleans up editor reference
        """

        if self._ankiMw.reviewer and self._ankiMw.reviewer.card:
            note = self._ankiMw.reviewer.card.note()
            self.createReviewerMenu(webView, menu, self.openInBrowser)


    def openInBrowser(self, website, query):
        """
            Setup enviroment for web browser and invoke it
        """

        Feedback.log('OpenInBrowser: {}'.format(self._currentNote))
        self._lastProvider = website

        if cfg.getConfig().useSystemBrowser:
            target = self.browser.formatTargetURL(website, query)
            openLink(target)
            return
        
        self.browser.setFields(None)   # clear fields
        self.browser.infoList = ['No action available on Reviewer mode']
        self.browser.open(website, query)
