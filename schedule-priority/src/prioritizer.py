# -*- coding: utf-8 -*-
#
# This files is part of schedule-priority addon
# @author ricardo saturnino

import json


class PrioInterface:
    """ Detach module for unit test (avoid error with relative import) """

    @classmethod
    def priority_list(cls):
        raise NotImplementedError()

    @classmethod
    def showInfo(cls, *args):
        raise NotImplementedError()

    @classmethod
    def showError(cls, *args):
        raise NotImplementedError()


def set_priority_tag(note, level):
    """
        Sets the level based on controlling note's tags
    """

    if not note:
        PrioInterface.showError('Could not get the instance of note. Cancelling process...')
        return

    # clear previous tags
    for pr in PrioInterface.priority_list():
        if not pr.tagName:
            continue

        if note.has_tag(pr.tagName):
            note.remove_tag(pr.tagName)

    newPriority = PrioInterface.priority_list()[level]

    # Not normal
    if newPriority.tagName:
        note.add_tag(newPriority.tagName)

    note.flush()
    priorityStr = newPriority.description
    PrioInterface.showInfo('Priority set as {}'.format(priorityStr))


def get_priority_tag_command(note, level) -> str:
    """
        Sets the level based on controlling note's tags
    """

    if not note:
        PrioInterface.showError('Could not get the instance of note. Cancelling process...')
        return ""

    cur_tags = note.tags

    # clear previous tags
    for pr in PrioInterface.priority_list():
        if not pr.tagName:
            continue

        if pr.tagName in cur_tags:
            cur_tags.remove(pr.tagName)

    new_priority = PrioInterface.priority_list()[level]

    # Not normal
    if new_priority.tagName:
        cur_tags.append(new_priority.tagName)

    json_tags = json.dumps(cur_tags)

    PrioInterface.showInfo('Priority tags list {}'.format(json_tags))
    return "saveTags:%s" % json_tags


def get_prioritized_time(card, resTime):
    """
        Get the estimated time to be shown on top of buttons
    """

    note = card.note()

    for item in PrioInterface.priority_list():
        if not item.tagName:
            continue

        if note.has_tag(item.tagName):
            resTime = round(resTime * (item.value / 100))

    return resTime


def get_card_multiplier(card) -> float:
    note = card.note()

    for item in PrioInterface.priority_list():
        if not item.tagName:
            continue

        if note.has_tag(item.tagName):
            return float(item.value / 100)

    return 1.0
