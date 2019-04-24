# -*- coding: utf-8 -*-
# Handles the transformation from markdown markup to HTML output
# Contains service class
#
# This files is part of anki-markdown-formatter addon
# @author ricardo saturnino
# -------------------------------------------------------

from .config import ConfigKey
from .core import Feedback

from markdown import markdown
# from .html2text import __init__
from . import html2text
import re
import os

class Converter:
    """
        Responsible for converting texts between differents formats
    """

    _amdArea = re.compile(r'<amd(?:\s+([\w-]+)\s*=\s*\"(\w+)\"\s*)?(?:\s+([\w-]+)\s*=\s*\"(\w+)\"\s*)?>(.*)</amd>', flags=(re.MULTILINE | re.DOTALL))
    _clozeRE = re.compile(r'<span class=cloze>((.)+)</span>')
    _inputRE = re.compile(r'(&lt;input ((.)+?)&gt;)', flags=(re.MULTILINE | re.DOTALL))
    _h2t = html2text.HTML2Text()

    ANKI_CLOZE = "<span class=cloze>[...]</span>"
    CLOZE_REPLACEMENT = '||...CLOZE...||'
    INPUT_REPLACEMENT = '||...INPUT...||'

    def convertMarkdown(self, inpt:str): 
        return markdown(inpt)


    def isAmdAreaPresent(self, input:str):
        match = self._amdArea.search(input)
        return match and len(match.groups()) >= 5


    def convertAmdAreasToMD(self, inpt:str, cleanupHTML:bool = False, isTypeMode: bool = False):
        """
            Finds areas delimited by <amd> tags. 
            Converts their contents to Markdown
        """

        match = self._amdArea.search(inpt)
        if (not match) or len(match.groups()) < 5:
            return inpt

        (start, stop) = match.span()
        content = match.group(5)
        localOpts = {match.group(1): evalBool(match.group(2)), match.group(3): evalBool(match.group(4))}

        content = self._preProcessContent(content, cleanupHTML, isTypeMode)
        content = self._wrapStyle(content)

        return inpt[:start] + content + inpt[stop:]


    def _wrapStyle(self, input):
        return '<span class="amd">{}</span>'.format(input)


    def _preProcessContent(self, content: str, cleanupHTML: bool, isTypeMode: bool):

        # to keep cloze parts
        clozeMatch = self._clozeRE.search(content)
        clozeContents = list()

        while clozeMatch:
            clozeContents.append(clozeMatch.group(1))
            content = content.replace(clozeMatch.group(0), self.CLOZE_REPLACEMENT, 1)
            clozeMatch = self._clozeRE.search(content)

        if cleanupHTML:
            content = self.getTextFromHtml(content)
                
        content = self._wrapContent(content)
        content = self.convertMarkdown(content)
        content = self._unwrapContent(content)

        if clozeContents:
            for value in clozeContents:
                content = content.replace(self.CLOZE_REPLACEMENT, 
                    self.ANKI_CLOZE.replace('[...]', value), 1)

        
        if isTypeMode:
            inputMatch = self._inputRE.search(content)

            while inputMatch:
                iValue = inputMatch.group(2)
                if not iValue.strip().endswith('/'):
                    iValue = iValue + '/'
                content = content.replace(inputMatch.group(0), "<input %s>" % iValue)
                inputMatch = self._inputRE.search(content)

        return content

    def _wrapContent(self, input):
        content = input \
            .replace('&lt;', '|/MENOR/|').replace('&gt;', '|/MAIOR/|') \
            .replace('&amp;', '|/eCom/|')

        return content

        # return ("<!-- content -->%s<!-- /content -->" % content)

    # _reContent = re.compile(r'<!-- content -->((.)+)<!-- /content -->', flags=(re.MULTILINE | re.DOTALL))

    def _unwrapContent(self, value):
        return value \
                .replace('|/MENOR/|', '&lt;').replace('|/MAIOR/|', '&gt;') \
                .replace('|/eCom/|', '&amp;')
        matcher = self._reContent.search(value)
        if matcher:
            print(matcher.groups())
            content = matcher.group(1)
            content = content \
                .replace('<', '&lt;').replace('>', '&gt;') \
                .replace('&', '&amp;')

            return re.sub(self._reContent, content, value)
        return value


    def getTextFromHtml(self, html):
        """
            Extracts clear text from an HTML input
        """
        return self._h2t.handle(html)


def evalBool(value):
    return None if value == None else ('true' == value.lower())