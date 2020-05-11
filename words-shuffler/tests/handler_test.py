# -*- coding: utf-8 -*-
# Related to typein handler
# Test code for config modules

# This files is part of words-shuffler addon
# @author ricardo saturnino
# ------------------------------------------------

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../src')

from shuffler_handler import ShufflerHandler
from anki_mocks_test import TestReviewer

def hookFakeFn(*args, **vargs):
    pass

tested = ShufflerHandler()

def setUp():
    print('----------------- {} -----------------'.format(_testMethodName))
    reviewer = TestReviewer()
    tested.setupBindings(reviewer, hookFakeFn)


def test_noArea():
    res = tested.getTokenizerAreas("""
                <span class="content">
                SELECT .., <span class=cloze>...</span>  Option.
                </span>
            """)

    # print(res)
    assert not res


def test_has_area():
    res = tested.getTokenizerAreas("""
        <span class="content">
        [[tk::SELECT name, surname FROM people]]  Option.
        </span>
    """)

    print(res)
    assert res


def test_item_simple():
    res = tested.tokenizeItem('This is a simple phrase with 0 special chars')
    assert res is not None
    assert 'tk-item' in res


def test_item_with_special():
    res = tested.tokenizeItem('This is a &phrase/ \\with . $ ]]chars')
    assert res is not None
    assert 'tk-item' in res
    assert 'chars' in res
    print(res)

# TODO: support tag in the text and ignore its spaces
def test_item_with_tag():
    res = tested.tokenizeItem('This is a <span style="some"> &phrase with chars</span>')
    assert res is not None
    assert 'tk-item' in res
    assert '<span style="some"' in res
    print(res)


def test_process():
    res = tested.process("""
        Normal sentence, no spliting.
        [[tk::This is a simple phrase with 0 special]]
        
        Number 2:
        [[tk::One more phrase. Alles gut?]]
    """)
    print(res)
