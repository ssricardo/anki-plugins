# -*- coding: utf-8 -*-
# Related to typein handler
# Test code for config modules

# This files is part of fill-the-blanks addon
# @author ricardo saturnino
# ------------------------------------------------

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../src')

import unittest
# import config as cc

from handler import TypeClozeHander
from anki_mocks_test import TestReviewer

class HandlerTest(unittest.TestCase):

    tested = TypeClozeHander()

    def setUp(self):
        print('----------------- {} -----------------'.format(self._testMethodName))
        self.reviewer = TestReviewer()
        self.tested.setupBindings(self.reviewer)


    def test_nocloze(self):
        res = self.reviewer.typeAnsQuestionFilter("""
            <span class="content">
            Single valeu
            Multiline
            </span>
        """)

        print(res)

    def test_cloze_notype(self):
        res = self.reviewer.typeAnsQuestionFilter("""
            <span class="content">
            SELECT .., <span class=cloze>...</span>  Option.
            </span>
        """)

        print(res)

    def test_single_clozeType(self):
        self.reviewer.card.note()['Text'] = 'Meu valor {{c1::Alterado}} usando cloze '
        res = self.reviewer.typeAnsQuestionFilter("""
            <span class="content">
            [[type:cloze:Text]]
            </span>
        """)

        print(res)

    def test_multiple_clozeType(self):
        self.reviewer.card.note()['Text'] = """A small {{c1::step}} for a man, 
        a big {{c1::one}}...
            {{c2::plainText}}
        """

        res = self.reviewer.typeAnsQuestionFilter("""
            <span class="content">
            [[type:cloze:Text]]
            </span>
        """)

        print(res)

    def test_withRegexStr(self):
        self.reviewer.card.note()['Text'] = """
            Some content here with [ \\t\\n\\x\\r\\f].
        """

        res = self.reviewer.typeAnsQuestionFilter("""
            <span class="content">
            [[type:cloze:Text]]
            </span>
        """)

        print(res)

unittest.main()