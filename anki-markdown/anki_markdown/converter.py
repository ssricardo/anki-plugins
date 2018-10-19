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

    _amdArea = re.compile('\<amd>(.)*\</amd>', flags=(re.MULTILINE + re.DOTALL))

    def convertMarkdown(self, inpt:str): 
        return markdown(inpt)


    def _clearLine(self, content: str):
        """
            Trims each line, because it matters for markdown.
            Tries to preserv lines within code blocks
        """

        inCode = False
        result = ''
        for line in content.split(os.linesep):
            trimed = line.strip()
            if inCode:
                if trimed != os.linesep:
                    result += line
            else:
                result += trimed

            if "```" in trimed:
                if (line.count("```") % 2) != 0:
                    inCode = not inCode

            result += os.linesep

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
        # print('='*80, 'Text: ', content, '='*80, sep='\n')

        # strip
        content = self._clearLine(content)
        print('='*80, 'Striped: ', content, '='*80, sep='\n')
        
        content = self.convertMarkdown(content)
        # print('='*80, 'HTML: ', content, '='*80, sep='\n')
        return inpt[:start] + content + inpt[stop:]

    
    def getTextFromHtml(self, html):
        html = (html.replace('<br>', os.linesep)
            .replace('<br/>', os.linesep)
            .replace('<br />', os.linesep)
            .replace('</div>', os.linesep + '</div>'))

        soup = BeautifulSoup(html, "html.parser")
        return soup.getText('  ')

        # data = soup.findAll(text=True)
        # result = filter(self._visibleFilter, data)
        
        # return '  '.join(data)


    def _visibleFilter(self, element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True