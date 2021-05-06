# -*- coding: utf-8 -*-
# Handles the main integration with Anki
#
# This files is part of words-shuffler addon
# @author ricardo saturnino
# -------------------------------------------------------
instance = None

import os
from .shuffler_handler import ShufflerHandler
from .config import ConfigService, ConfigKey 

from anki.hooks import wrap, addHook
from aqt import mw

CWD = os.path.dirname(os.path.realpath(__file__))
ICON_FILE = 'resources/reload.png'

def _ankiConfigRead(key):
    return mw.addonManager.getConfig(__name__)[key]


def run():
    global instance
    instance = Controller(mw)
    instance.setupBindings(mw.reviewer, wrap)

    ConfigService._f = _ankiConfigRead

class Controller:

    _mw = None
    CSS_LOCATIONS = [CWD + '/resources/dragula.min.css', CWD + '/resources/atokenizer.css']
    JS_LOCATIONS = [CWD + '/resources/dragula.min.js', CWD + '/resources/atokenizer.js']
    cssStyles = []
    jsList = []

    def __init__(self, ankiMw):
        self._mw = ankiMw
        self.handler = ShufflerHandler()
        Controller.loadResources()

    @classmethod
    def loadResources(clz):
        if len(clz.cssStyles) > 0:
            return      # already read

        for cl in clz.CSS_LOCATIONS:
            with open(cl, 'r') as f:
                clz.cssStyles.append(f.read())

        for jsl in clz.JS_LOCATIONS:
            with open(jsl, 'r') as f:
                clz.jsList.append(f.read())

    def setupBindings(self, reviewer, wrapFn):
        if not reviewer:
            print('No reviewer')
            return

        # Reviewer
        reviewer._initWeb = self.wrapInitWeb(reviewer._initWeb)
        # gui_hooks.card_will_show.append(self.processField)
        addHook("prepareQA", self.processField)
        addHook("showQuestion", self.afterShowQuestion)

        # Editor
        addHook("setupEditorButtons", self.setupEditorButtons)
        addHook("setupEditorShortcuts", self.setupShortcuts)

    def processField(self, inpt, card, phase) -> str:
        value = inpt if isinstance(inpt, str) else None
        if not value:
            if hasattr(inpt, "question_text"):
                value = inpt["question_text"]
            else:
                return value

        if self._mw.state == "review":
            if phase == 'reviewQuestion':
                return self.handler.process(value)
            else:
                self._extractResponses()

        return self.handler.extractCleanText(value)

    def wrapInitWeb(self, fn):

        def _initReviewerWeb(*args):
            fn()

            for css in Controller.cssStyles:
                addStylesJs = """
                    var prStyle = `{}`;
    
                    $(prStyle).appendTo('body');
                    """.format('<style type="text/css">' + css + '</style>')

                self._mw.reviewer.web.eval(addStylesJs)

            for js in Controller.jsList:
                self._mw.reviewer.web.eval("""
                    %s
                """ % js)

        return _initReviewerWeb

    def afterShowQuestion(self):
        self._mw.reviewer.web.eval("""
            setTimeout(function() {        
                %s
            }, 150);
        """ % 'initTokenizer();')

    def _extractResponses(self):
        self._mw.reviewer.web.evalWithCallback("getResult()", self._handleResponseCb)

    def _handleResponseCb(self, val) -> None:
        res = """setTimeout(function() {        
                setFeedback([%s])
            }, 50);
        """ % ", ".join(map(lambda v: '"%s"' % v, val))
        self._mw.reviewer.web.eval(res)

    def setupEditorButtons(self, buttons, editor):
        """Add buttons to editor"""

        def addTkMarkup(arg):
            editor.web.eval("wrap('[[ws::', ']]');")

        editor._links['ws-surround'] = addTkMarkup

        return buttons + [
            editor._addButton(
            CWD + '/' + ICON_FILE,
            'ws-surround',  "Words-shuffler marker({})".format('Ctrl+Shift+w'),
            toggleable=False, id='bt_add_tk')]

    def setupShortcuts(self, scuts:list, editor):
        def addTkMarkup():
            editor.web.eval("wrap('[[ws::', ']]');")

        scuts.append(('Ctrl+Shift+w', addTkMarkup))
