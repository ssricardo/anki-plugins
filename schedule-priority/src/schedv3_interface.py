# -*- coding: utf-8 -*-
#
# This files is part of schedule-priority addon
# @author ricardo saturnino

from anki.cards import Card
from aqt import mw
from .prioritizer import get_card_multiplier


def set_card_priority(text: str, card: Card, kind: str) -> str:
    multiplier = get_card_multiplier(card)
    mw.reviewer.web.eval("""
        var card_multiplier = %f;
    """ % multiplier)
    return text
