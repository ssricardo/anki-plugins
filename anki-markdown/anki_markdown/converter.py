# -*- coding: utf-8 -*-
# Handles the transformation from markdown markup to HTML output
# Contains service class
#
# This files is part of anki-markdown addon
# @author ricardo saturnino
# -------------------------------------------------------

from markdown import markdown
from bs4 import BeautifulSoup
import re
import os

class Converter:
    """
        Responsible for converting texts between differents formats
    """

    _amdArea = re.compile('\<amd>(.)*\</amd>', flags=(re.MULTILINE + re.DOTALL))

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
        

    def findConvertArea(self, inpt:str):
        """
            Finds an area delimited by <amd> tags. 
            Converts its contents as Markdown
        """

        match = self._amdArea.search(inpt)
        if not match:
            return inpt

        (start, stop) = match.span()
        content = inpt[start:stop]

        content = self.getTextFromHtml(content)

        # strip
        content = self._clearLine(content)
        
        content = self.convertMarkdown(content)

        # adjusment for code blocks
        content = content.replace('<code>', '<code><pre>').replace('</code>', '</pre></code>')

        return inpt[:start] + content + inpt[stop:]

    
    def getTextFromHtml(self, html):
        """
            Extracts clear text from an HTML input
        """

        html = (html.replace('<br>', os.linesep)
            .replace('<br/>', os.linesep)
            .replace('<br />', os.linesep)
            .replace('</div>', os.linesep + '</div>'))
            # .replace('&nbsp;', ' ')

        soup = BeautifulSoup(html, "html.parser")
        return soup.getText('  ')