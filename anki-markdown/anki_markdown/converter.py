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
from bs4 import BeautifulSoup
import re
import os

class Converter:
    """
        Responsible for converting texts between differents formats
    """

    # _amdArea = re.compile('\<amd>(.)*\</amd>', flags=(re.MULTILINE | re.DOTALL))
    _amdArea = re.compile(r'<amd(?:\s+([\w-]+)\s*=\s*\"(\w+)\"\s*)?(?:\s+([\w-]+)\s*=\s*\"(\w+)\"\s*)?>(.*)</amd>', flags=(re.MULTILINE | re.DOTALL))

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
        

    def findConvertArea(self, inpt:str, globalMustTrim: bool, globalReplaceSpace: bool):
        """
            Finds an area delimited by <amd> tags. 
            Converts its contents to Markdown
        """

        match = self._amdArea.search(inpt)
        if (not match) or len(match.groups()) < 5:
            return inpt

        (start, stop) = match.span()
        content = match.group(5)
        localOpts = {match.group(1): evalBool(match.group(2)), match.group(3): evalBool(match.group(4))}

        content = self._preProcessContent(content,
            localOpts[ConfigKey.TRIM_LINES] if ConfigKey.TRIM_LINES in localOpts else globalMustTrim,
            localOpts[ConfigKey.REPLACE_SPACES] if ConfigKey.REPLACE_SPACES in localOpts else globalReplaceSpace
        )

        return inpt[:start] + content + inpt[stop:]


    def _preProcessContent(self, content: str, mustTrim: bool, mustReplaceSpace: bool):
        hadCloze = "<span class=cloze>[...]</span>" in content

        content = self.getTextFromHtml(content, mustReplaceSpace)

        # strip / trim
        if mustTrim:
            content = self._clearLine(content)
        
        content = self.convertMarkdown(content)

        # tries to keed cloze parts - TODO improve in the future
        if hadCloze:
            content = content.replace("[...]", "<span class=cloze>[...]</span>")

        return content
    

    def getTextFromHtml(self, html, replaceSpace):
        """
            Extracts clear text from an HTML input
        """

        html = (html.replace('<br>', os.linesep)
            .replace('<br/>', os.linesep)
            .replace('<br />', os.linesep)
            .replace('</div>', os.linesep + '</div>'))

        if replaceSpace:
            html = html.replace('&nbsp;', ' ')

        soup = BeautifulSoup(html, "html.parser")
        return soup.getText('  ')

def evalBool(value):
    return None if value == None else ('true' == value.lower())