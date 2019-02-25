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

    # _amdArea = re.compile('\<amd>(.)*\</amd>', flags=(re.MULTILINE | re.DOTALL))
    _amdArea = re.compile(r'<amd(?:\s+([\w-]+)\s*=\s*\"(\w+)\"\s*)?(?:\s+([\w-]+)\s*=\s*\"(\w+)\"\s*)?>(.*)</amd>', flags=(re.MULTILINE | re.DOTALL))
    _clozeRE = re.compile(r'<span class=cloze>(\w+|\[\.\.\.\])</span>')
    # _replacementRE = re.compile(r'\[\[\.\.\.(\w+|\[\.\.\.\])\.\.\.\]\]')
    _h2t = html2text.HTML2Text()

    ANKI_CLOZE = "<span class=cloze>[...]</span>"
    CLOZE_REPLACEMENT = '[[...CLOZE...]]'

    def convertMarkdown(self, inpt:str): 
        return markdown(inpt)


    def _clearLine(self, content: str):
        """
            Trims each line, because it matters for markdown.
            Tries to preserv lines within code blocks
        """

        isInCode = False
        result = ''

        for line in content.split(os.linesep):
            wasInCode = isInCode
            trimed = line.strip()
            if isInCode:
                if trimed == os.linesep:
                    continue
                trimed = line

            if "```" in trimed:

                # not balanced, it's either opening or closing from other line
                if (trimed.count("```") % 2) != 0:
                    isInCode = not isInCode                    
                
            result += trimed + os.linesep

        return result
        

    def convertAmdAreasToMD(self, inpt:str, cleanupHTML:bool = False):
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

        content = self._preProcessContent(content, cleanupHTML)

        # ,
          #  localOpts[ConfigKey.TRIM_LINES] if ConfigKey.TRIM_LINES in localOpts else globalMustTrim,
           # localOpts[ConfigKey.REPLACE_SPACES] if ConfigKey.REPLACE_SPACES in localOpts else globalReplaceSpace

        return inpt[:start] + content + inpt[stop:]


    def _preProcessContent(self, content: str, cleanupHTML: bool):

        print('-----------------------------')
        # to keep cloze parts
        clozeMatch = self._clozeRE.search(content)
        clozeContents = list()
        
        while clozeMatch:
            print(clozeMatch)
            clozeContents.append(clozeMatch.group(1))
            content = content.replace(clozeMatch.group(0), self.CLOZE_REPLACEMENT, 1)
            clozeMatch = self._clozeRE.search(content)

        if cleanupHTML:
            content = self.getTextFromHtml(content)

        content = self.convertMarkdown(content)

        print(clozeContents)

        if clozeContents:
            for value in clozeContents:
                content = content.replace(self.CLOZE_REPLACEMENT, 
                    self.ANKI_CLOZE.replace('[...]', value), 1)

        return content
    

    def getTextFromHtml(self, html):
        """
            Extracts clear text from an HTML input
        """
        return self._h2t.handle(html)

def evalBool(value):
    return None if value == None else ('true' == value.lower())