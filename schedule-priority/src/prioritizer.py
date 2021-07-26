# -*- coding: utf-8 -*-
#
# This files is part of schedule-priority addon
# @author ricardo saturnino

import math

from .exception import InvalidConfiguration
from . import core

from .core import Feedback
from .core import Priority


# Responsible for the main logic for this addon
# Integrates with anki Scheduler
class Prioritizer:

    @classmethod
    def setPriority(clz, note, level):
        """
            Sets the level based on controlling note's tags
        """

        if not note:
            Feedback.showError('Could not get the instance of note. Cancelling process...')
            return

        # clear previous tags
        for pr in Priority.priorityList:
            if not pr.tagName:
                continue

            if note.hasTag(pr.tagName):
                note.delTag(pr.tagName)

        newPriority = Priority.priorityList[level]

        # Not normal
        if newPriority.tagName:
            note.addTag(newPriority.tagName)

        note.flush()
        priorityStr = newPriority.description
        Feedback.showInfo('Priority set as {}'.format(priorityStr))

    @classmethod
    def getPrioritizedTime(clz, card, resTime):
        """
            Get the estimated time to be shown on top of buttons
        """

        note = card._note

        for item in Priority.priorityList:
            if not item.tagName:
                continue

            if note.hasTag(item.tagName):
                resTime = int(resTime * (item.value / 100))

        return resTime

    # Deprecation: To be removed when support for scheduler v1 is dropped
    @staticmethod
    def getNextInterval(scheduleInstance, *args, **kargs):
        """ Decorator for estimate next schedule time for a given option. 
            This time is shown above the card while studying
        """

        f = kargs['_old']
        res = f(scheduleInstance, args[0], args[1])
        card = args[0]  # card

        return Prioritizer.getPrioritizedTime(card, res)

    # Deprecation: To be removed when support for scheduler v1 is dropped
    @staticmethod
    def priorityUpdateRevision(scheduleInst, *args, **kargs):
        """ Decorator for get next revision date, based on priority. 
            Used to schedule the next date.
        """

        f = kargs['_old']
        card = args[0]
        f(scheduleInst, card, args[1])  # _updateRevIvl(self, card, ease)
        card.ivl = Prioritizer.getPrioritizedTime(card, card.ivl)
