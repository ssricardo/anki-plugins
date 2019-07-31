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

def hookFakeFn(*args, **vargs):
    pass

class HandlerTest(unittest.TestCase):

    tested = TypeClozeHander()

    def setUp(self):
        print('----------------- {} -----------------'.format(self._testMethodName))
        self.reviewer = TestReviewer()
        self.tested.setupBindings(self.reviewer, hookFakeFn)


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

    def test_with_quotes(self):
        self.reviewer.card.note()['Text'] = """A small step for a man, 
        a big {{c1::one("q", 'step')}}, {{c1::..}}...
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

    
    def test_issue_14(self):
        self.reviewer.card.note()['Text'] = """
<center><table class="highlighttable"><tbody><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">1
2</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="color: #008000; font-weight: bold">def</span> test():
    {{c1::Print(<span style="font-family: &quot;DejaVu Sans&quot;; color: rgb(186, 33, 33);">"Test"</span><span style="font-family: &quot;DejaVu Sans&quot;;">)}}</span>
</pre></div>
</td></tr></tbody></table></center><br>
        """

        res = self.reviewer.typeAnsQuestionFilter("""
            <span class="content">
            [[type:cloze:Text]]
            </span>
        """)

        print(res)

unittest.main()