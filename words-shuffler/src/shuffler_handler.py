# -*- coding: utf-8 -*-
# Class responsible for the processing
#
# This file is part of words-shuffler addon
# @author ricardo saturnino
# -------------------------------------------------------

import os
import re
import random

currentLocation = os.path.dirname(os.path.realpath(__file__))


class ShufflerHandler:
    _currentFirst = None
    _currentIndex = 0

    CONTAINER_TEMPLATE = """
        <input type="hidden" id="originalVal-%s" class="tkOriginalVal" value="%s" />
        <ul id="tkContainer-%s" class="tk-container"> %s </ul>
    """

    RE_TOKENS_TEXT = re.compile(r"\[\[ws::(.+?)]]")

    def getTokenizerAreas(self, txt: str):
        return ShufflerHandler.RE_TOKENS_TEXT.search(txt, re.DOTALL)

    def tokenizeItem(self, tkArea: str):
        if not tkArea:
            return ''

        def item(i):
            return """<li class="item tk-item">%s</li>""" % i
        parts = list(map(item, tkArea.split(' ')))
        random.shuffle(parts)

        self._currentIndex += 1
        items = ' '.join(parts)
        curField = 'f' + str(self._currentIndex)
        return ShufflerHandler.CONTAINER_TEMPLATE % (
            curField, tkArea, curField, items)

    def process(self, inputTxt: str):
        tkAreas = self.getTokenizerAreas(inputTxt)
        if not tkAreas:
            return inputTxt
        self._currentIndex = 0

        return re.sub(ShufflerHandler.RE_TOKENS_TEXT, lambda a: self.tokenizeItem(a.group(1)), inputTxt)

    def extractCleanText(self, inputTxt: str):
        tkAreas = self.getTokenizerAreas(inputTxt)
        if not tkAreas:
            return inputTxt
        self._currentIndex = 0

        fieldsResult = re.sub(ShufflerHandler.RE_TOKENS_TEXT, lambda a: self._formatResponse(a.group(1)), inputTxt)
        return fieldsResult

    def _formatResponse(self, value: str) -> str:
        return """
            %s
            <div class="tk-feedback"></div>
        """ % value
