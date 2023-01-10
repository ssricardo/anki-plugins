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


class AnkiInterface:
    """
        Decouples internal components from Anki, making it easier for unit testing
    """

    staticReviewer = None

    @staticmethod
    def stripHTML(*value):
        raise NotImplementedError("Must be replaced")

    @staticmethod
    def tr(*value):
        raise NotImplementedError("Must be replaced")

    @staticmethod
    def TR(*value):
        raise NotImplementedError("Must be replaced")

    @staticmethod
    def wrap(*args):
        raise NotImplementedError("Must be replaced")

    @staticmethod
    def addHook(*args):
        raise NotImplementedError("Must be replaced")

    @staticmethod
    def stripHTML(*args):
        raise NotImplementedError("Must be replaced")


currentLocation = os.path.dirname(os.path.realpath(__file__))


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
        self.effectiveText = _text
        self.entries = _values


class TypeClozeHandler:
    _currentFirst = None
    reviewer = None
    _stripHTML = None

    DEFAULT_ANKI_CLOZE = """
    <center>
    <input type=text id=typeans onkeypress="_typeAnsPress();"
    style="font-family: '%s'; font-size: %spx;">
    </center>
    """

    RE_REMAINING_TEXT = re.compile(r"\{\{c\d\d?::(.+?)(::.*?)?\}\}", flags=re.DOTALL)

    def __init__(self, reviewer, anki: AnkiInterface, _ignoreCase=False, lengthMultiplier: int = 62) -> None:

        super().__init__()
        self.reviewer = reviewer

        self._mw = reviewer.mw
        self.isIgnoreCase = _ignoreCase
        self._lengthMultiplier = lengthMultiplier

        TypeClozeHandler._stripHTML = anki.stripHTML
        reviewer_class = anki.staticReviewer
        reviewer_class.typeAnsQuestionFilter = anki.wrap(reviewer_class.typeAnsQuestionFilter,
                                                         lambda _, buf, _old: self.typeAnsQuestionFilter(buf, _old), "around")
        reviewer_class.typeAnsAnswerFilter = anki.wrap(reviewer_class.typeAnsAnswerFilter,
                                                       lambda _, buf, _old: self.typeAnsAnswerFilter(buf, _old), "around")
        reviewer_class._getTypedAnswer = anki.wrap(reviewer_class._getTypedAnswer,
                                                   lambda _, _old: self._getTypedAnswer(_old), "around")

        anki.addHook("showQuestion", self.on_show_question)

    def typeAnsQuestionFilter(self, buf: str, _old) -> str:
        ref = self.reviewer
        ref.typeCorrect = None
        clozeIdx = None
        self._currentFirst = None

        rev_card = self.reviewer.card

        m = re.search(ref.typeAnsPat, buf)
        if not m:
            return buf

        fld = m.group(1)
        if fld.startswith("cloze:"):
            clozeIdx = rev_card.ord + 1
            fld = fld.split(":")[1]

        for f in rev_card.note_type()['flds']:
            if f['name'] == fld:
                _fieldContent = rev_card.note()[f['name']]
                if clozeIdx:
                    ref.typeCorrect = self._createFieldsContext(
                        _fieldContent, clozeIdx)

                ref.typeFont = f['font']
                ref.typeSize = f['size']
                break

        if not ref.typeCorrect:
            return _old(ref, buf)

        if not clozeIdx:
            return re.sub(ref.typeAnsPat, TypeClozeHandler.DEFAULT_ANKI_CLOZE % (ref.typeFont, ref.typeSize), buf)

        return buf[:m.start()] + \
                 self._formatHtmlContent(ref.typeCorrect) + \
                 buf[m.end():]

    CURRENT_CARD_FIELD_PLACEHOLDER = "[...]"

    def _createFieldsContext(self, txt, idx) -> FieldsContext:
        reCloze = re.compile(r"\{\{c%s::(.+?)\}\}" % idx, flags=re.DOTALL)
        matches = re.findall(reCloze, txt)
        if not matches:
            return FieldsContext(txt, [])

        matches = [self._splitHint(txt) for txt in matches]
        _fieldStates = map(self._extractFieldState, matches)
        txt = re.sub(reCloze, self.CURRENT_CARD_FIELD_PLACEHOLDER, txt)

        # Replace other cloze (not current id)
        txt = TypeClozeHandler.RE_REMAINING_TEXT.sub(r'\1', txt)
        txt = self._handleLargeText(txt)

        if '[sound:' in txt:
            txt = re.sub(r'\[sound:(\w|\d|\.|\-|_)+?\]', '', txt, flags=re.DOTALL)

        return FieldsContext(txt, list(_fieldStates))

    def _extractFieldState(self, inputWithHint) -> FieldState:
        try:
            (_input, hint) = inputWithHint
            content = BeautifulSoup('<span/>' + _input, 'html.parser')
            text = ''.join(content.findAll(text=True))
            text = self.clear_correct_value_as_reviewer(text)
            return FieldState(text, hint)
        except UserWarning:
            return FieldState(*inputWithHint)

    def _splitHint(self, txt):
        if "::" in txt:
            return tuple(txt.split("::", 1))
        return (txt, "")

    def _handleLargeText(self, data: str) -> str:
        """ Handle weird issue #82 """
        if len(data) <= 2048:
            return data
        return TypeClozeHandler.RE_REMAINING_TEXT.sub(r'\1', data)  # apply it again

    def _formatHtmlContent(self, fieldsCtx: FieldsContext):
        res = fieldsCtx.effectiveText

        for idx, field in enumerate(fieldsCtx.entries):
            (val, hint) = field.value, field.hint
            item = """<input type="hidden" id="ansval%d" value="%s" />""" % (idx, val.replace('"', '&quot;'))
            item = item + """<input type="text" id="typeans{0}" placeholder="{1}"
class="ftb" style="width: {2}em" /><script type="text/javascript">setUpFillBlankListener($('#ansval{0}').val(), {0})
</script>""".format(idx, hint, self._getInputLength(hint, val))
            res = res.replace(self.CURRENT_CARD_FIELD_PLACEHOLDER, item, 1)

        if not self._currentFirst:
            self._currentFirst = 'typeans0'

        # placeholder for callback result
        res = res + """
            <input type="hidden" id="ansval" value="" />
        """

        return res

    def _getInputLength(self, hint, val):
        return (max(len(val), len(hint)) * (0.01 * self._lengthMultiplier))

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

    def typeAnsAnswerFilter(self, currentText, _originalFn):
        reviewer = self.reviewer

        if not reviewer.typeCorrect or not isinstance(reviewer.typeCorrect, FieldsContext):
            return _originalFn(reviewer, currentText)

        ctx: FieldsContext = reviewer.typeCorrect

        origSize = len(currentText)
        currentText = currentText.replace("<hr id=answer>", "")
        hadHR = len(currentText) != origSize

        result = currentText
        for index, field in enumerate(ctx.entries):
            cor = field.value
            given = html.escape(ctx.answers[index]) if ctx.answers and len(ctx.answers) == len(ctx.entries) else "None"
            field_res = self.format_field_result(given, cor)
            result = re.sub(r'<span class="?cloze\s*"?(\s*data-ordinal="\d\d?")?>%s</span>' % html.escape(field.value),
                            field_res, result, 1)

        # copy from reviewer original
        def repl(match):
            s = """
        <span style="font-family: '%s'; font-size: %spx">%s</span>""" % (
                reviewer.typeFont,
                reviewer.typeSize,
                match,
            )
            if hadHR:
                s = "<hr id=answer>" + s
            return s

        return re.sub(reviewer.typeAnsPat, repl, result)

    def format_field_result(self, given: str, expected: str):
        if given.strip() == expected.strip():
            return "<span class='cloze st-ok'>%s</span>" % expected
        if self.isIgnoreCase and given.strip().lower() == expected.strip().lower():
            return "<span class='cloze st-ok'>%s</span>" % expected
        return "<span class='cloze st-expected'>%s</span> <span class='cloze st-error'>(%s)</span>" % (expected, given)

    def clear_correct_value_as_reviewer(self, value: str):
        """Mostly copy from original reviewer code"""

        cor = self._mw.col.media.strip(value)
        cor = re.sub("(\n|<br ?/?>|</?div>)+", " ", cor)
        cor = TypeClozeHandler._stripHTML(cor)
        # ensure we don't chomp multiple whitespace
        cor = cor.replace(" ", "&nbsp;")
        cor = html.unescape(cor)
        cor = cor.replace("\xa0", " ")
        cor = cor.strip()
        cor = html.escape(cor)
        return cor

    def _getTypedAnswer(self, _old) -> None:
        reviewer = self.reviewer
        if reviewer.typeCorrect and isinstance(reviewer.typeCorrect, FieldsContext):
            self.reviewer.web.evalWithCallback("typedWords ? typedWords : []", self._onFillBlankAnswer)
        return _old(reviewer)

    def _onFillBlankAnswer(self, val) -> None:
        reviewer = self.reviewer
        if reviewer.typeCorrect and isinstance(reviewer.typeCorrect, FieldsContext):
            reviewer.typeCorrect.answers = val
        reviewer._showAnswer()
