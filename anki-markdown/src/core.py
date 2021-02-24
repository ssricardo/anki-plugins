# -*- coding: utf-8 -*-
# Contains center components useful across this addon
# Holds Contansts

# This files is part of anki-markdown addon
# @author ricardo saturnino
# ------------------------------------------------

'Application reference. Must be bind on startup'
class AppHolder:
    app = None


class Label:
    CARD_MENU = 'Apply markdown'
    BROWSER_ASSIGN_TO = '&Assign to field'


# --------------------------- Util function ----------------------------

class Feedback:
    'Responsible for messages and logs'

    @staticmethod
    def log(*args, **kargs):
        pass
        # print(args, kargs)

    @staticmethod
    def showInfo(*args):
        pass

    @staticmethod
    def showError(*args):
        pass