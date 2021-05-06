# -*- coding: utf-8 -*-
# Handles the main integration with Anki
#
# This files is part of fill-the-blanks addon
# @author ricardo saturnino
# -------------------------------------------------------

instance = None

import os
from .handler import TypeClozeHander
from .config import ConfigService, ConfigKey 

from aqt.utils import showInfo, tooltip, showWarning
from anki.hooks import wrap, addHook
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
    instance.setupBindings(mw.reviewer, wrap)


class Controller:

    _mw = None
    JS_LOCATION = CWD + '/fill-blanks.js'

    def __init__(self, ankiMw):
        self._mw = ankiMw

    def setupBindings(self, reviewer, wrapFn):
        if not reviewer:
            print('No reviewer')
            return
        self.handler = TypeClozeHander(reviewer, addHook, ConfigService.read(ConfigKey.IGNORE_CASE, bool))
        reviewer._initWeb = self.wrapInitWeb(reviewer._initWeb)

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

        return _initReviewerWeb

    

