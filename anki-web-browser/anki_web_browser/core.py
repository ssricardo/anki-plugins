# -*- coding: utf-8 -*-
# Contains center components useful across this addon
# Holds Contansts

# This files is part of anki-web-browser addon
# @author ricardo saturnino
# ------------------------------------------------


class Label:
    CARD_MENU = 'Search in Web'
    BROWSER_ASSIGN_TO = 'Assign to field'


# --------------------------- Useful function ----------------------------

class Feedback:
    'Responsible for messages and logs'

    @staticmethod
    def log(*args, **kargs):
        print(args, kargs)

    @staticmethod
    def showInfo(*args):
        pass

    @staticmethod
    def showError(*args):
        pass