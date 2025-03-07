# -*- coding: utf-8 -*-
# Handles the main integration (bindings) with Anki
#
# This files is part of fill-the-blanks addon
# @author ricardo saturnino
# -------------------------------------------------------

instance = None

import os

from anki import hooks
from anki.hooks import wrap, addHook
from anki.utils import strip_html
from aqt import gui_hooks
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.utils import tooltip

from .config import ConfigService, ConfigKey
from .handler import TypeClozeHandler, AnkiInterface

CWD = os.path.dirname(os.path.realpath(__file__))

CSS_STYLE = """
<style type="text/css">
input.ftb {    
    border-radius: 5px;
    border: 1px solid;
    min-width: 50px;
    max-width: 400px;
    padding: 3px;    
    margin: 2px;
}
input.ftb-md {
    width: 150px;
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

_handler = None
JS_LOCATION = CWD + '/fill-blanks.js'
_warn_template_shown = False

def _ankiConfigRead(key):
    return mw.addonManager.getConfig(__name__)[key]


def _bind_anki_interface():
    anki_interface = AnkiInterface()
    anki_interface.staticReviewer = Reviewer
    anki_interface.addHook = addHook
    anki_interface.wrap = wrap
    anki_interface.strip_HTML = strip_html
    return anki_interface


def warn_template_editor(*args):
    global _warn_template_shown
    if not _warn_template_shown:
        tooltip("[Fill-in-the-blanks] Be aware: The add-on does not apply to the template editor. To check it, please go to Review mode", 8000)
        _warn_template_shown = True


def wrapInitWeb(anki_mw, fn):
    def _initReviewerWeb(*args):
        fn()

        addStylesJs = """
                var prStyle = `{}`;

                $(prStyle).appendTo('body');
                """.format(CSS_STYLE)

        anki_mw.reviewer.web.eval(addStylesJs)

        f = open(JS_LOCATION, 'r')
        anki_mw.reviewer.web.eval("""
                %s
            """ % f.read())

        if not ConfigService.read(ConfigKey.FEEDBACK_ENABLED, bool):
            anki_mw.reviewer.web.eval('disableInstantFb();')

        if ConfigService.read(ConfigKey.IGNORE_CASE, bool):
            anki_mw.reviewer.web.eval('ignoreCaseOnFeedback();')

        if ConfigService.read(ConfigKey.IGNORE_ACCENTS, bool):
            anki_mw.reviewer.web.eval('ignoreAccentsOnFeedback();')

        if ConfigService.read(ConfigKey.ASIAN_CHARS, bool):
            print('Enabling experimental Asian Chars mode')
            anki_mw.reviewer.web.eval('enableAsianChars();')

    return _initReviewerWeb


def _setup_bindings():
    global _handler

    if not ConfigService.read(ConfigKey.OVERRIDE_TYPE_CLOZE, bool):
        return

    reviewer = mw.reviewer
    if not reviewer:
        print('Unexpected state on Fill-blanks: No reviewer')
        return

    anki_interface = _bind_anki_interface()

    _handler = TypeClozeHandler(reviewer, anki_interface, ConfigService.read(ConfigKey.IGNORE_CASE, bool),
                                ConfigService.read(ConfigKey.LEN_MULTIPLIER, int))


def _setup_new_integration():
    if not ConfigService.read(ConfigKey.ENABLE_NEW_FILTER, bool):
        return

    from .handler_new import addon_field_filter, on_show_question, handle_answer, AnkiInterfaceNew, getTypedAnswer
    AnkiInterfaceNew.staticReviewer = mw.reviewer
    AnkiInterfaceNew.strip_HTML = strip_html

    hooks.field_filter.append(addon_field_filter)
    addHook("showQuestion", on_show_question)

    gui_hooks.card_layout_will_show.append(warn_template_editor)
    gui_hooks.card_will_show.append(handle_answer)

    Reviewer._getTypedAnswer = wrap(Reviewer._getTypedAnswer,
                                    lambda _, _old: getTypedAnswer(_old), "around")


def run():
    # tooltip('Loading fill-the-blanks Handler')
    ConfigService.load_config = _ankiConfigRead

    reviewer = mw.reviewer
    reviewer._initWeb = wrapInitWeb(mw, reviewer._initWeb)

    _setup_bindings()
    _setup_new_integration()
