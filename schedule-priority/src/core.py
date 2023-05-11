# -*- coding: utf-8 -*-
#
# This files is part of schedule-priority addon
# @author ricardo saturnino

import math
# Constants for schedule-priority

class AppHolder:
    """Application reference. Must be bound on startup"""

    app = None


class Priority:
    """Refer to the existing Priorities registry. 
       Holds the tag, a description (labels) and the relative name in config.json for each case"""

    priorityList = []

    def __init__(self, description, tagName, configName, default):
        self.description = description
        self.tagName = tagName
        self.configName = configName
        self.value = float(default)

    @classmethod
    def load(clz):
        p = []
        p.append(Priority('Lowest', 'priority:lowest', 'Lowest', 200))
        p.append(Priority('Low', 'priority:low', 'Low', 150))
        p.append(Priority('Normal', None, None, 100))
        p.append(Priority('High', 'priority:high', 'High', 75))
        p.append(Priority('Highest', 'priority:highest', 'Highest', 50))
        clz.priorityList = (p)  # no adding or removing

    @classmethod
    def setValue(clz, key, val):
        if math.isnan(val):
            raise InvalidConfiguration('Value should be a number. Got: {}'.format(val))

        lastValue = math.inf
        for item in clz.priorityList:            
            if item.configName == key:
                if val >= lastValue:
                    raise InvalidConfiguration('One or more value are invalid. From the lowest to the highest, values MUST BE smaller then the previous one. '
                    + 'Given Normal = 100. Got: {} for {}'.format(val, item.description))
                item.setValue = float(val)
                break
            lastValue = item.value


class Label:
    """ Texts in the interface """

    CARD_MENU = '&Card Priority'
    MENU_LOW = 'Low'
    MENU_NORMAL = 'Normal'
    MENU_HIGH = 'High'

# --------------------------- Useful function ----------------------------

class Feedback:
    'Responsible for messages and logs'

    @staticmethod
    def log(*args, **kargs):
        print(args, kargs)

    @staticmethod
    def showInfo(*args):
        pass    # will be bind to Anki in the controller

    @staticmethod
    def showError(*args):
        pass    # will be bind to Anki in the controller

# -----------------------------------------------------------------------------


class InvalidConfiguration(Exception):

    def __init__(self, message):
        super().__init__(message)
