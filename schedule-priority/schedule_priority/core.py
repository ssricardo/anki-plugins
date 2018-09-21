# -*- coding: utf-8 -*-
#
# This files is part of schedule-priority addon
# @author ricardo saturnino

# Constants for schedule-priority

'Application reference. Must be bind on startup'
class AppHolder:

    app = None


class Priority:
    """Refer to the existing Priorities registry. 
       Holds the tag, a description (labels) and the relative name in config.json for each case"""

    priorityList = []  

    def __init__(self, description, tagName, configName, default):
        self.description = description
        self.tagName = tagName
        self.configName = configName
        self.defaultValue = default


    @classmethod
    def load(clz):
        p = []
        p.append(Priority('Lowest', 'priority:lowest', 'Lowest', 200))
        p.append(Priority('Low', 'priority:low', 'Low', 150))
        p.append(Priority('Normal', None, None, 100))
        p.append(Priority('High', 'priority:high', 'High', 75))
        p.append(Priority('Highest', 'priority:highest', 'Highest', 50))
        clz.priorityList = p



class Label:
    """ Texts in the interface """

    CARD_MENU = 'Card Priority'
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