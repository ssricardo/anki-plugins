# -*- coding: utf-8 -*-

# TODO: check how to resolver the relatives imports, which are used in the production version within Anki

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import unittest
from anki import *

from schedule_priority.prioritizer import Prioritizer
import schedule_priority.core
from schedule_priority.core import Priority

class PrioritizerTest(unittest.TestCase):

    @classmethod
    def setUpClass(clz):
        Priority.load()

    def test_prioritizedTime(self):
        pass

    def test_highTime(self):
        c = TestCard()
        c._note._tag = Priority.priorityList[3].tagName # High

        time = Prioritizer.getPrioritizedTime(c, 1000)
        self.assertEqual(750, time)

    def test_lowTime(self):
        c = TestCard()
        c._note._tag = Priority.priorityList[1].tagName # Low
        
        time = Prioritizer.getPrioritizedTime(c, 1000)
        self.assertEqual(1500, time)


if __name__ == '__main__':
    unittest.main()