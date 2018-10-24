# -*- coding: utf-8 -*-
# Main interface between Anki and this addon components

# This files is part of anki-markdown-formatter addon
# @author ricardo saturnino
# ------------------------------------------------

from .config import ConfigKey, ConfigService
from .core import Feedback, AppHolder, Style
from .converter import Converter

import anki
import os

from aqt.editor import Editor
from aqt.reviewer import Reviewer
from aqt.qt import QAction
from PyQt5 import QtWidgets
from aqt.utils import showInfo, tooltip, showWarning
from anki.hooks import addHook

# Holds references so GC does kill them
controllerInstance = None

CWD = os.path.dirname(os.path.realpath(__file__))
ICON_FILE = 'icons/markdown-3.png'

# ---------------------------- Injected functions -------------------
@staticmethod
def _ankiShowInfo(*args):
    tooltip(args)

@staticmethod
def _ankiShowError(*args):
    showWarning(str(args))

def _ankiConfigRead(key):
    return AppHolder.app.addonManager.getConfig(__name__)[key]

# ------------------------ Init ---------------------------------

def run():
    global controllerInstance
    
    from aqt import mw  

    Feedback.log('Setting anki-markdown controller')
    Feedback.showInfo = _ankiShowInfo
    Feedback.showError = _ankiShowError
    
    AppHolder.app = mw
    ConfigService._f = _ankiConfigRead

    controllerInstance = Controller()
    controllerInstance.setupBindings()


class Controller:
    """
        The mediator/adapter between Anki with its components and this addon specific API
    """

    _converter = Converter()
    _showButton = None
    _shortcut = None
    _trimConfig = None
    _replaceSpaceConfig = None

    def __init__(self):
        self._showButton = ConfigService.read(ConfigKey.SHOW_MARKDOWN_BUTTON, bool)
        self._shortcut = ConfigService.read(ConfigKey.SHORTCUT, str)
        self._trimConfig = ConfigService.read(ConfigKey.TRIM_LINES, bool)
        self._replaceSpaceConfig = ConfigService.read(ConfigKey.REPLACE_SPACES, bool)

    def setupBindings(self):
        addHook("prepareQA", self.processField)
        addHook("setupEditorButtons", self.setupButtons)
        addHook("setupEditorShortcuts", self.setupShortcuts)


    def processField(self, inpt, card, phase, *args):
        inpt = Style.MARKDOWN + inpt
        res = self._converter.findConvertArea(inpt, self._trimConfig, self._replaceSpaceConfig)
        return res


    def setupButtons(self, buttons, editor):        
        """Add buttons to editor"""

        if not self._showButton:
            return buttons

        self._editorReference = editor
        editor._links['apply-markdown'] = self._wrapAsMarkdown
        return buttons + [editor._addButton(
            CWD + '/' + ICON_FILE,
            "apply-markdown", 
            "Apply Markdown ({})".format(self._shortcut))]


    def setupShortcuts(self, scuts:list, editor):
        self._editorReference = editor
        scuts.append((self._shortcut, self._wrapAsMarkdown))        

   
    def _wrapAsMarkdown(self, editor = None):
        if not editor:
            if not self._editorReference:
                return
            editor = self._editorReference

        editor.web.eval("wrap('<amd>', '</amd>');")
        Feedback.showInfo('Anki Markdown :: Added successfully')

    def _unwrapMarkdown(self):
        pass

    def isEditing(self):
        'Checks anki current state. Whether is editing or not'

        return True if (self._ankiMw and self._editorReference) else False


# ---------------------------------- Events listeners ---------------------------------
