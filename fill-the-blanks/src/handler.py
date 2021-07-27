# -*- coding: utf-8 -*-
# Class responsible for the processing
#
# This file is part of fill-the-blanks addon
# @author ricardo saturnino
# -------------------------------------------------------

import os
import re
from bs4 import BeautifulSoup
import html

try:
    from anki.utils import stripHTML
    from aqt.utils import (tr, TR)
except ImportError:
    print('anki.utils not available. Probably running from test')

currentLocation = os.path.dirname(os.path.realpath(__file__))
original_typeAnsAnswerFilter = None
original_typeAnsQuestionFilter = None
original_getTypedAnswer = None

class FieldState:
    value: str = None
    hint: str = None

    def __init__(self, _value: str, _hint: str = None) -> None:
        super().__init__()
        self.value = _value
        self.hint = _hint


class FieldsContext:
    answers: list = list()

    def __init__(self, _text: str, _values: list) -> None:
        super().__init__()
        self.text = _text
        self.entries = _values


class TypeClozeHander:
    _currentFirst = None
    reviewer = None

    DEFAULT_ANKI_CLOZE = """
    <center>
    <input type=text id=typeans onkeypress="_typeAnsPress();"
    style="font-family: '%s'; font-size: %spx;">
    </center>
    """

    RE_REMAINING_TEXT = re.compile(r"\{\{c\d\d?::(.+?)(::.*?)?\}\}")

    def __init__(self, reviewer, addHook, _ignoreCase = False) -> None:
        global original_typeAnsAnswerFilter, original_typeAnsQuestionFilter, original_getTypedAnswer

        super().__init__()
        self.reviewer = reviewer
        self._mw = reviewer.mw
        self.isIgnoreCase = _ignoreCase

        original_typeAnsAnswerFilter = reviewer.typeAnsAnswerFilter
        original_typeAnsQuestionFilter = reviewer.typeAnsQuestionFilter
        original_getTypedAnswer = reviewer._getTypedAnswer

        reviewer.typeAnsQuestionFilter = self.typeAnsQuestionFilter
        reviewer.typeAnsAnswerFilter = self.typeAnsAnswerFilter
        reviewer._getTypedAnswer = self._getTypedAnswer
        addHook("showQuestion", self.on_show_question)


    def typeAnsQuestionFilter(self, buf: str) -> str:
        ref = self.reviewer
        ref.typeCorrect = None
        clozeIdx = None
        self._currentFirst = None

        cCard = self.reviewer.card

        m = re.search(ref.typeAnsPat, buf)
        if not m:
            return buf

        fld = m.group(1)
        if fld.startswith("cloze:"):
            clozeIdx = cCard.ord + 1
            fld = fld.split(":")[1]

        for f in cCard.model()['flds']:
            if f['name'] == fld:
                _fieldContent = cCard.note()[f['name']]
                if clozeIdx:
                    ref.typeCorrect = self._createFieldsContext(
                        _fieldContent, clozeIdx)

                ref.typeFont = f['font']
                ref.typeSize = f['size']
                break

        if not ref.typeCorrect:
            return original_typeAnsQuestionFilter(buf)

        if not clozeIdx:
            return re.sub(ref.typeAnsPat, TypeClozeHander.DEFAULT_ANKI_CLOZE % (ref.typeFont, ref.typeSize), buf)

        else:
            result = buf[:m.start()] + \
                self._formatTypeCloze(ref.typeCorrect) + \
                buf[m.end():]
            # ref.typeCorrect = None      # FIXME

            return result

    def _createFieldsContext(self, txt, idx) -> FieldsContext:
        reCloze = re.compile(r"\{\{c%s::(.+?)\}\}" % idx, re.DOTALL)
        matches = re.findall(reCloze, txt)
        if not matches:
            return FieldsContext(txt, [])

        matches = [self._splitHint(txt) for txt in matches]
        _fieldStates = map(self._extractFieldState, matches)
        txt = re.sub(reCloze, "[...]", txt)

        # Replace other cloze (not current id)
        txt = TypeClozeHander.RE_REMAINING_TEXT.sub(r'\1', txt, re.DOTALL)
        txt = self._handleLargeText(txt)
        if '[sound:' in txt:
            txt = re.sub(r'\[sound:(\w|\d|\.|\-|_)+?\]', '', txt, re.DOTALL)

        return FieldsContext(txt, list(_fieldStates))


    def _extractFieldState(self, inputWithHint) -> FieldState:
        try:
            (_input, hint) = inputWithHint
            content = BeautifulSoup('<span/>' + _input, 'html.parser')
            text = ''.join(content.findAll(text=True))
            return FieldState(text, hint)
        except UserWarning:
            return FieldState(*inputWithHint)


    def _splitHint(self, txt):
        if "::" in txt:
            return tuple(txt.split("::", 1))
        return (txt, "")


    def _formatTypeCloze(self, fieldsCtx: FieldsContext):
        res = fieldsCtx.text

        for idx, field in enumerate(fieldsCtx.entries):
            (val, hint) = field.value, field.hint
            item = """<input type="hidden" id="ansval%d" value="%s" />""" % (idx, val.replace('"', '&quot;'))
            item = item + """<input type="text" id="typeans{0}" placeholder="{1}" 
                class="ftb" style="width: {2}em" />
                <script type="text/javascript">
                    setUpFillBlankListener($('#ansval{0}').val(), {0})
                </script>""".format(idx, hint, (max(len(val), len(hint)) * 0.62))
            res = res.replace('[...]', item, 1)

        if not self._currentFirst:
            self._currentFirst = 'typeans0'

        # placeholder for callback result
        res = res + """
            <input type="hidden" id="ansval" value="" />
        """

        return res


    def _handleLargeText(self, data: str) -> str:
        """ Handle weird issue #82 """
        if len(data) <= 2048:
            return data
        return TypeClozeHander.RE_REMAINING_TEXT.sub(r'\1', data, re.DOTALL)    # apply it again


    def on_show_question(self):
        web = self.reviewer.mw.web
        if self._currentFirst:
            web.setFocus()
            web.eval("focusOnFirst();")
        if self.reviewer.typeCorrect and isinstance(self.reviewer.typeCorrect, FieldsContext):
            web.eval("cleanUpTypedWords();")
            ctx: FieldsContext = self.reviewer.typeCorrect
            web.eval("prepareTypedWords(%d);" % len(ctx.entries))

# --------------------------------- Handle answer ----------------------------------------

    def typeAnsAnswerFilter(self, buf):
        ref = self.reviewer

        if not ref.typeCorrect or not isinstance(ref.typeCorrect, FieldsContext):
            return original_typeAnsAnswerFilter(buf)

        ctx: FieldsContext = ref.typeCorrect

        origSize = len(buf)
        buf = buf.replace("<hr id=answer>", "")
        hadHR = len(buf) != origSize

        result = buf
        for index, field in enumerate(ctx.entries):
            cor = self.original_clear_correct_value(field.value)
            given = ctx.answers[index] if ctx.answers and len(ctx.answers) == len(ctx.entries) else "None"
            field_res = self.format_field_result(given, cor)
            result = result.replace('<span class=cloze>%s</span>' % field.value, field_res, 1)

        # from original
        def repl(match):
            s = """
        <span style="font-family: '%s'; font-size: %spx">%s</span>""" % (
                ref.typeFont,
                ref.typeSize,
                match,
            )
            if hadHR:
                s = "<hr id=answer>" + s
            return s

        return re.sub(ref.typeAnsPat, repl, result)

    def format_field_result(self, given: str, expected: str):
        if given.strip() == expected.strip():
            return "<span class='cloze st-ok'>%s</span>" % expected
        if self.isIgnoreCase and given.strip().lower() == expected.strip().lower():
            return "<span class='cloze st-ok'>%s</span>" % expected
        return "<span class='cloze st-expected'>%s</span> <span class='cloze st-error'>(%s)</span>" % (expected, given)

    def original_clear_correct_value(self, value: str):
        cor = self._mw.col.media.strip(value)
        cor = re.sub("(\n|<br ?/?>|</?div>)+", " ", cor)
        cor = stripHTML(cor)
        # ensure we don't chomp multiple whitespace
        cor = cor.replace(" ", "&nbsp;")
        cor = html.unescape(cor)
        cor = cor.replace("\xa0", " ")
        cor = cor.strip()
        return cor

    def _getTypedAnswer(self) -> None:
        reviewer = self.reviewer
        if reviewer.typeCorrect and isinstance(reviewer.typeCorrect, FieldsContext):
            self.reviewer.web.evalWithCallback("typedWords ? typedWords : []", self._onFillBlankAnswer)
        return original_getTypedAnswer()

    def _onFillBlankAnswer(self, val) -> None:
        reviewer = self.reviewer
        if reviewer.typeCorrect and isinstance(reviewer.typeCorrect, FieldsContext):
            reviewer.typeCorrect.answers = val
        reviewer._showAnswer()
