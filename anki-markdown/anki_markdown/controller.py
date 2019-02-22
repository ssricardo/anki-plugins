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
    _editAsMarkdownEnabled = False    

    _js_rewrite_inPreEnvironment = """
        <script type="text/javascript">
        // alert('Script init');
        console.log('Script init');
        var originalPreEnvironment = inPreEnvironment;
        var editAsMarkdownEnabled = false;

        console.log(inPreEnvironment);

        function inPreEnvironment() {
            return true;
            if (editAsMarkdownEnabled) {
                return true;
            }
            return originalPreEnvironment();
        }

        console.log('Func 1 ');

        function insertNewline() {
            if (!inPreEnvironment()) {
                setFormat('insertText', '\\n');
                console.log('insertNewline IN PreEnvironment');
                return;
            }
            console.log('insertNewline: NOT inPreEnvironment');

            var r = window.getSelection().getRangeAt(0);
            if (!r.collapsed) {
                // delete any currently selected text first, making
                // sure the delete is undoable
                setFormat("delete");
            }

            var oldHeight = currentField.clientHeight;
            setFormat('inserthtml', '\\n');
            if (currentField.clientHeight === oldHeight) {
                setFormat('inserthtml', '\\n');
            }
        }

        console.log('JS Loaded');
        </script>
    """

    def __init__(self):
        self._showButton = ConfigService.read(ConfigKey.SHOW_MARKDOWN_BUTTON, bool)
        self._shortcut = ConfigService.read(ConfigKey.SHORTCUT, str)
        self._trimConfig = ConfigService.read(ConfigKey.TRIM_LINES, bool)
        self._replaceSpaceConfig = ConfigService.read(ConfigKey.REPLACE_SPACES, bool)


    def setupBindings(self):
        addHook("prepareQA", self.processField)
        addHook("setupEditorButtons", self.setupButtons)
        addHook("setupEditorShortcuts", self.setupShortcuts)
        addHook("loadNote", self.onLoadNote)

        # Editor.setupWeb = self._wrapEditorSetupWeb(Editor.setupWeb)
        # Editor.setNote = self._wrapEditorSetNote(Editor.setNote)
        # Editor.mungeHTML = self._wrapEditorMungeHTML(Editor.mungeHTML)

    def _wrapEditorSetNote(self, f):

        def wrapped(editor, note, hide=True, focusTo=None):
            processedFields = []
            for field in note.fields:
                if (field.startswith('<pre>')):
                    processedFields.append(field)
                else:
                    newValue = "<pre>{}</pre>".format(field)
                    processedFields.append(newValue)

            note.fields = processedFields

            f(editor, note, hide, focusTo)

        return wrapped

    def _wrapEditorMungeHTML(self, f):
        def wrapped(self, txt):
            print(txt)
            f(self, txt)
        return wrapped

    def onLoadNote(self, editor):
        editor.web.eval("console.log('setNote')")
        note = editor.note

        styles = """
        var prStyle = `<style type="text/css">
            pre.amd {    
                border-left: 2px solid #070777;
                margin: 0px;
            }
            </style>`;

        $(prStyle).appendTo('#fields');
        """
        editor.web.eval(styles)
        editor.web.eval("$('#fields').prepend('<h2>Markdown?</h2>')")
        editor.web.eval("""
        function handleMdKey(evt) {
            if (event.keyCode === 13 && ! evt.shiftKey) {
                event.preventDefault();
                console.log('Enter pressed');

                if (currentField) {
                    $(currentField).append('\n');
                }
            }
        }

        $('.field').wrap('<pre class=\"amd\"></pre>');
        $('.field').keypress(handleMdKey);
        """)


    def processField(self, inpt, card, phase, *args):
        inpt = inpt
        res = self._converter.findConvertArea(inpt)
        return Style.MARKDOWN + os.linesep + res


    def setupButtons(self, buttons, editor):        
        """Add buttons to editor"""        

        if not self._showButton:
            return buttons

        self._editorReference = editor
        editor._links['apply-markdown'] = self._wrapAsMarkdown
        editor._links['alert-msg'] = self._tmpAction
        editor._links['apply-btn'] = self._tmpAction2

        return buttons + [editor._addButton(
            CWD + '/' + ICON_FILE,
            "apply-markdown",  "Apply Markdown ({})".format(self._shortcut)),
            editor._addButton(
            None,
            "alert-msg",  "Tmp Alert"),
            editor._addButton(
            None,
            "apply-btn",  "Apply")]


    def setupShortcuts(self, scuts:list, editor):
        scuts.append((self._shortcut, self._wrapAsMarkdown))
        # editor.web.eval("wrap(null, \"%s\")" % self._js_rewrite_inPreEnvironment)
        
        

    def _tmpAction(self, editor = None):
        print('_tmpAction')
        
        # self.setEditAsMarkdownEnabled(not self._editAsMarkdownEnabled)  # invert
        self._editorReference.web.eval("wrap('<pre>', '</pre>')")

        self._editorReference.web.eval("console.log('editAsMarkdownEnabled? ' + editAsMarkdownEnabled);")
        self._editorReference.web.eval("console.log('Pre? ' + inPreEnvironment());")


    def _tmpAction2(self, editor = None):
        print('_tmpAction2')

        cur = self._editorReference.currentField
        note = self._editorReference.note
        newValue = self._converter.convertMarkdown(note.fields[cur])
        note.fields[cur] = newValue
        self._editorReference.setNote(note)
   

    def setEditAsMarkdownEnabled(self, value: bool):
        self._editAsMarkdownEnabled = value
        self._editorReference.web.eval('editAsMarkdownEnabled = {};'.format(str(value).lower()))


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
