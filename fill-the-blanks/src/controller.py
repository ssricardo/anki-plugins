# -*- coding: utf-8 -*-
# Handles the main integration with Anki
#
# This files is part of fill-the-blanks addon
# @author ricardo saturnino
# -------------------------------------------------------

instance = None

import os
from .handler import TypeClozeHandler, AnkiInterface
from .config import ConfigService, ConfigKey 

from aqt.utils import showInfo, tooltip, showWarning
from aqt.reviewer import Reviewer
from anki.hooks import wrap, addHook
from aqt import gui_hooks
from anki.utils import stripHTML
from aqt import mw

CWD = os.path.dirname(os.path.realpath(__file__))

CSS_STYLE = """
<style type="text/css">
input.ftb {    
    border-radius: 5px;
    border: 1px solid;
    width: 150px;
    min-width: 120px;
    max-width: 400px;
    padding: 3px;    
    margin: 2px;
}
input.st-incomplete {
    background-color: #FFFF77;
    color: #333;
}
input.st-error {
    background-color: #ff9999;
    color: #333;
}
input.st-ok {
    background-color: #99ff99;
    color: #333;
}

.cloze.st-error {
    color: #ff4949;
    text-decoration: line-through;
}
.cloze.st-expected {
    color: orange;
}
.cloze.st-ok {
    color: #3bd03b;
}

</style>
"""

def _ankiConfigRead(key):
    return mw.addonManager.getConfig(__name__)[key]


def run():
    
    # tooltip('Loading fill-the-blanks Handler')
    ConfigService._f = _ankiConfigRead

    instance = Controller(mw)
    instance.setupBindings(mw.reviewer)


class Controller:

    _mw = None
    handler = None
    JS_LOCATION = CWD + '/fill-blanks.js'
    warn_template_shown = False

    def __init__(self, ankiMw):
        self._mw = ankiMw

    def setupBindings(self, reviewer):
        if not reviewer:
            print('Unexpected state on Fill-blanks: No reviewer')
            return

        anki_interface = self.bind_anki_interface()

        self.handler = TypeClozeHandler(reviewer, anki_interface, ConfigService.read(ConfigKey.IGNORE_CASE, bool),
                                        ConfigService.read(ConfigKey.LEN_MULTIPLIER, int))
        reviewer._initWeb = self.wrapInitWeb(reviewer._initWeb)

        gui_hooks.card_layout_will_show.append(Controller.warn_template_editor)

    @staticmethod
    def warn_template_editor(*args):
        if not Controller.warn_template_shown:
            tooltip("[Fill-in-the-blanks] Be aware: The add-on does not apply to the template editor. To check it, please go to Review mode", 8000)
            Controller.warn_template_shown = True

    @staticmethod
    def bind_anki_interface():
        anki_interface = AnkiInterface()
        anki_interface.staticReviewer = Reviewer
        anki_interface.addHook = addHook
        anki_interface.wrap = wrap
        anki_interface.stripHTML = stripHTML
        return anki_interface

    def wrapInitWeb(self, fn):

        def _initReviewerWeb(*args):
            fn()

            addStylesJs = """
                var prStyle = `{}`;
    
                $(prStyle).appendTo('body');
                """.format(CSS_STYLE)

            self._mw.reviewer.web.eval(addStylesJs)

            f = open(self.JS_LOCATION, 'r')
            self._mw.reviewer.web.eval("""
                %s
            """ % f.read())

            if not ConfigService.read(ConfigKey.FEEDBACK_ENABLED, bool):
                self._mw.reviewer.web.eval('disableInstantFb();')

            if ConfigService.read(ConfigKey.IGNORE_CASE, bool):
                self._mw.reviewer.web.eval('ignoreCaseOnFeedback();')

            if ConfigService.read(ConfigKey.IGNORE_ACCENTS, bool):
                self._mw.reviewer.web.eval('ignoreAccentsOnFeedback();')

            if ConfigService.read(ConfigKey.ASIAN_CHARS, bool):
                print('Enabling experimental Asian Chars mode')
                self._mw.reviewer.web.eval('enableAsianChars();')

        return _initReviewerWeb

    

