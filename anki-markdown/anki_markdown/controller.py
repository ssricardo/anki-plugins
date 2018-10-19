# -*- coding: utf-8 -*-
# Main interface between Anki and this addon components

# This files is part of anki-markdown addon
# @author ricardo saturnino
# ------------------------------------------------

from .config import service as cfg
from .core import Feedback, AppHolder
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

@staticmethod
def _ankiShowInfo(*args):
    tooltip(args)

@staticmethod
def _ankiShowError(*args):
    showWarning(str(args))

def run():
    global controllerInstance
    
    from aqt import mw  

    Feedback.log('Setting anki-markdown controller')
    Feedback.showInfo = _ankiShowInfo
    Feedback.showError = _ankiShowError
        
    # NoteMenuHandler.setOptions(cfg.getConfig().providers)
    AppHolder.app = mw
    controllerInstance = Controller()
    controllerInstance.setupBindings()


class Controller:
    """
        The mediator/adapter between Anki with its components and this addon specific API
    """

    _converter = Converter()
    ADD_SHORTCUT = 'Ctrl+Shift+M'
    CLEAR_SHORTCUT = 'Ctrl+Shift+W'

    def __init__(self):
        _curPath = os.path.dirname(__file__)
        self._iconsPath = os.path.join(_curPath, "icons")
        if not os.path.exists(self._iconsPath):
            self._iconsPath = ""

    def setupBindings(self):
        addHook("prepareQA", self.processField)
        addHook("setupEditorButtons", self.setupButtons)
        addHook("setupEditorShortcuts", self.setupShortcuts)


    def processField(self, inpt, card, phase, *args):
        res = self._converter.findConvertArea(inpt)
        return res


    def setupButtons(self, buttons, editor):        
        """Add buttons to editor"""

        if not os.path.exists(self._iconsPath.join('markdown-2.svg')):
            print('[WARNING] Icon not found')

# self._iconsPath.join('markdown-2.svg')

        self._editorReference = editor
        editor._links['apply-markdown'] = self._wrapAsMarkdown
        return buttons + [editor._addButton(
            'M',
            "M", 
            "Apply Markdown ({})<br>".format(Controller.ADD_SHORTCUT))]


    def setupShortcuts(self, scuts:list, editor):
        self._editorReference = editor
        scuts.append((Controller.ADD_SHORTCUT, self._wrapAsMarkdown))        

   
    def _wrapAsMarkdown(self, editor = None):
        if not editor:
            if self._editorReference:
                self._editorReference.web.eval("wrap('<amd>', '</amd>');")
                Feedback.showInfo('Anki Markdown :: Added successfully')
        else:
            editor.web.eval("wrap('<amd>', '</amd>');")
            Feedback.showInfo('Anki Markdown :: Added successfully')

    def _unwrapMarkdown(self):
        pass

    def isEditing(self):
        'Checks anki current state. Whether is editing or not'

        return True if (self._ankiMw and self._editorReference) else False


# ---------------------------------- Events listeners ---------------------------------
