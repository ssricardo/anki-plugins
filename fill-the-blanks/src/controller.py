# -*- coding: utf-8 -*-
# Handles the main integration with Anki
#
# This files is part of fill-the-blanks addon
# @author ricardo saturnino
# -------------------------------------------------------

instance = None

import os
from .handler import TypeClozeHander

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
    color: #333 !important;
    margin: 2px;
}
input.st-incomplete {
    background-color: #ABDAFC !important;
}
input.st-error {
    background-color: #ff9999 !important;
}
input.st-ok {
    background-color: #99ff99 !important;
}

</style>
"""

def run():
    from aqt.utils import showInfo, tooltip, showWarning
    from anki.hooks import wrap
    # tooltip('Loading fill-the-blanks Handler')

    from aqt import mw
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
        self.handler = TypeClozeHander()
        self.handler.setupBindings(reviewer)
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

        return _initReviewerWeb

    

