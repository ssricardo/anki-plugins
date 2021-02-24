# -*- coding: utf-8 -*-
# Handles the transformation from markdown markup to HTML output
# Contains service class
#
# This files is part of anki-markdown-formatter addon
# @author ricardo saturnino
# -------------------------------------------------------

from markdown import markdown
import re


class Converter:
    """
        Responsible for converting texts between differents formats
    """

    _attributeParts = '(?:\s+([\w-]+)\s*=\s*\"(\w+)\"\s*)?(?:\s+([\w-]+)\s*=\s*\"(\w+)\"\s*)'
    _amdArea = re.compile(r"<amd%s?>(?P<value>.*?)</amd>" % _attributeParts, flags=(re.MULTILINE | re.DOTALL))
    _clozeRE = re.compile(r'(<span class=(?:\"|\')?cloze((?:\w|\s|-)*)(?:\"|\')?>(.*?)</span>)')
    _inputRE = re.compile(r'(&lt;input ((.)+?)&gt;)', flags=(re.MULTILINE | re.DOTALL))

    ANKI_CLOZE = "<span class=\"cloze ||...CLASSES..||\">[...]</span>"
    CLOZE_REPLACEMENT = '||...CLOZE...||'
    INPUT_REPLACEMENT = '||...INPUT...||'

    def convertMarkdown(self, inpt:str):
        return markdown(inpt)

    def isAmdAreaPresent(self, input:str):
        match = self._amdArea.search(input)
        return match and len(match.groups()) >= 5

    def convertAmdAreasToMD(self, inpt: str, cleanupHTML:bool = False, isTypeMode: bool = False):
        """
            Finds areas delimited by <amd> tags. 
            Converts their contents to Markdown
        """

        match = self._amdArea.search(inpt)
        if (not match) or len(match.groups()) < 5:
            return inpt

        (start, stop) = match.span()
        content = match.group('value')

        content = self._processQuotes(content)
        content = self._processContent(content, cleanupHTML, isTypeMode)
        content = self._wrapStyle(content)

        return inpt[:start] + content + inpt[stop:]

    def _wrapStyle(self, input):
        return '<span class="amd">{}</span>'.format(input)

    # TODO testar
    def _processQuotes(self, content: str):
        result = list()
        for line in content.split('\n'):
            resLine = line.replace('&gt; ', '> ', 1) if line.startswith('&gt; ') else line
            result.append(resLine)
        return '\n'.join(result)

    def _processContent(self, content: str, cleanupHTML: bool, isTypeMode: bool):

        # to keep cloze parts
        clozeMatch = self._clozeRE.search(content)
        clozeContents = list()
        clozeClasses = list()

        while clozeMatch:
            clozeContents.append(clozeMatch.group(3))
            clozeClasses.append(clozeMatch.group(2))
            content = content.replace(clozeMatch.group(1), self.CLOZE_REPLACEMENT, 1)
            clozeMatch = self._clozeRE.search(content)

        if cleanupHTML:
            content = self.getTextFromHtml(content)

        content = self._wrapContent(content)
        content = self.convertMarkdown(content)
        content = self._unwrapContent(content)

        if clozeContents:
            for pos, value in enumerate(clozeContents):
                item = self.ANKI_CLOZE.replace('[...]', value)\
                    .replace('||...CLASSES..||', clozeClasses[pos] if clozeClasses[pos] else '')
                content = content.replace(self.CLOZE_REPLACEMENT, item, 1)

        if isTypeMode:
            content = self._fix_escaped_inputs(content)

        return content

    def _fix_escaped_inputs(self, content):
        inputMatch = self._inputRE.search(content)
        while inputMatch:
            iValue = inputMatch.group(2)
            if not iValue.strip().endswith('/'):
                iValue = iValue + '/'
            content = content.replace(inputMatch.group(1), "<input %s>" % iValue)
            inputMatch = self._inputRE.search(content)
        return content

    def _wrapContent(self, value: str):
        return value \
            .replace('&lt;', '|/MENOR/|').replace('&gt;', '|/MAIOR/|') \
            .replace('&amp;', '|/eCom/|')

    def _unwrapContent(self, value: str):
        return value \
                .replace('|/MENOR/|', '&lt;').replace('|/MAIOR/|', '&gt;') \
                .replace('|/eCom/|', '&amp;')
        matcher = self._reContent.search(value)
        if matcher:
            content = matcher.group(1)
            content = content \
                .replace('<', '&lt;').replace('>', '&gt;') \
                .replace('&', '&amp;')

            return re.sub(self._reContent, content, value)
        return value

    def getTextFromHtml(self, html):
        """
            Extracts clear text from an HTML input.
            > Must be overridden with html component.
        """
        return html

    def stripAmdTagForField(self, value: str, fieldName: str, regexField = None):
        _amdField = regexField if regexField else \
            re.compile(r"<amd%s?>\s*(?P<value>\{\{((type:)?(cloze:)?){0,1}%s\}\})\s*</amd>" %
                       (self._attributeParts, fieldName), flags=(re.MULTILINE | re.DOTALL))

        match = _amdField.search(value)
        if not match:
            return value

        result = value[:match.start()] + \
                 match.group('value') + \
                 value[match.end():]

        return self.stripAmdTagForField(result, fieldName, _amdField)

def evalBool(value):
    return None if value is None else ('true' == value.lower())
