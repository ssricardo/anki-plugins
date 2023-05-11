# -*- coding: utf-8 -*-

# TODO: check how to resolver the relatives imports, which are used in the production version within Anki

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../src')

import unittest
from anki_test import *

from prioritizer import get_prioritized_time, get_priority_tag_command, set_priority_tag, PrioInterface
from core import Priority

PrioInterface.priority_list = lambda: Priority.priorityList
PrioInterface.showInfo = lambda msg: print(msg)
PrioInterface.showError = lambda msg: print(msg)

Priority.load()


def test_prioritizedTime():
    pass

def test_highTime():
    c = TestCard()
    c._note._tag = Priority.priorityList[3].tagName # High

    time = get_prioritized_time(c, 1000)
    assert 750 == time

def test_lowTime():
    c = TestCard()
    c._note._tag = Priority.priorityList[1].tagName # Low

    time = get_prioritized_time(c, 1000)
    assert 1500 == time


if __name__ == '__main__':
    unittest.main()