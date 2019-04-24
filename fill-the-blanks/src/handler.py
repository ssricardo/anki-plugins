# -*- coding: utf-8 -*-
# ...
# ...
#
# This files is part of fill-the-blanks addon
# @author ricardo saturnino
# -------------------------------------------------------

import os
import json
import re
import shutil

currentLocation = os.path.dirname(os.path.realpath(__file__))

class TypeClozeHander:

    DEFAULT_ANKI_CLOZE = """
    <center>
    <input type=text id=typeans onkeypress="_typeAnsPress();"
    style="font-family: '%s'; font-size: %spx;">
    </center>
    """
        
    def setupBindings(self, reviewer):
        self.reviewer = reviewer

        reviewer.typeAnsQuestionFilter = self.typeAnsQuestionFilter
        # reviewer.typeAnsAnswerFilter = self.typeAnsAnswerFilter

    def typeAnsQuestionFilter(self, buf):
        self.typeCorrect = None
        clozeIdx = None

        text = buf
        entries = []
        cCard = self.reviewer.card
        ref = self.reviewer

        # buf = re.escape(buf)
        m = re.search(ref.typeAnsPat, buf)
        if not m:
            return buf

        fld = m.group(1)
        # if it's a cloze, extract data
        if fld.startswith("cloze:"):
            clozeIdx = cCard.ord + 1
            fld = fld.split(":")[1]
        
        for f in cCard.model()['flds']:
            if f['name'] == fld:
                ref.typeCorrect = cCard.note()[f['name']]
                if clozeIdx:
                    (text, entries) = self._customContentForCloze(
                        ref.typeCorrect, clozeIdx)

                ref.typeFont = f['font']
                ref.typeSize = f['size']
                break
        if not ref.typeCorrect:
            if ref.typeCorrect is None:
                if clozeIdx:
                    warn = _("""\
Please run Tools>Empty Cards""")
                else:
                    warn = _("Type answer: unknown field %s") % fld
                return re.sub(ref.typeAnsPat, warn, buf)
            else:
                # empty field, remove type answer pattern
                return re.sub(ref.typeAnsPat, "", buf)

        if not clozeIdx:
            return re.sub(ref.typeAnsPat, DEFAULT_ANKI_CLOZE % (ref.typeFont, ref.typeSize), buf)

        else:
            ref.typeCorrect = None
            result = re.sub(ref.typeAnsPat, 
                self._formatTypeCloze(text, entries), buf)

            # not working
            # ref.web.eval("""
            #     (function (){
            #         $('#typeans0').focus();
            #     }())
            # """)
            return result
            

    def _customContentForCloze(self, txt, idx):
        reCloze = re.compile(r"\{\{c%s::(.+?)\}\}"%idx, re.DOTALL)
        matches = re.findall(reCloze, txt)
        if not matches:
            return (txt, [])

        matches = [self._noHint(txt) for txt in matches]
        words = matches

        txt = re.sub(reCloze, "[...]", txt)

        # Replace other cloze (not current id)
        txt = re.sub(r"\{\{c\d::(.+?)\}\}", r'\1', txt, re.DOTALL)

        return (txt, words)


    def _noHint(self, txt):
            if "::" in txt:
                return txt.split("::")[0]
            return txt


    def _formatTypeCloze(self, text, entries):
        res = text
        for idx, val in enumerate(entries):
            item = """<input type="text" id="typeans{0}" 
     onkeyup="checkFieldValue('{1}', $('#typeans{0}'));"
     class="ftb" style="width: {2}em" />""".format(idx, val, (len(val) * 0.62)) 
            res = res.replace('[...]', item, 1)
            autofocus = ''
        return res

    def typeAnsAnswerFilter(self, buf):
        if not self.typeCorrect:
            return re.sub(self.typeAnsPat, "", buf)
        origSize = len(buf)
        buf = buf.replace("<hr id=answer>", "")
        hadHR = len(buf) != origSize
        # munge correct value
        parser = html.parser.HTMLParser()
        cor = self.mw.col.media.strip(self.typeCorrect)
        cor = re.sub("(\n|<br ?/?>|</?div>)+", " ", cor)
        cor = stripHTML(cor)
        # ensure we don't chomp multiple whitespace
        cor = cor.replace(" ", "&nbsp;")
        cor = parser.unescape(cor)
        cor = cor.replace("\xa0", " ")
        cor = cor.strip()
        given = self.typedAnswer
        # compare with typed answer
        res = self.correct(given, cor, showBad=False)
        # and update the type answer area
        def repl(match):
            # can't pass a string in directly, and can't use re.escape as it
            # escapes too much
            s = """
<span style="font-family: '%s'; font-size: %spx">%s</span>""" % (
                self.typeFont, self.typeSize, res)
            if hadHR:
                s = "<hr id=answer>" + s
            return s
        return re.sub(self.typeAnsPat, repl, buf)