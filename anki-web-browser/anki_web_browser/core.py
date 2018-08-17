# -*- coding: utf-8 -*-
# Contains center components useful across this addon
# Holds Contansts

# This files is part of anki-web-browser addon
# @author ricardo saturnino
# ------------------------------------------------


class Label:
    CARD_MENU = 'Search in Web'
    BROWSER_ASSIGN_TO = 'Assign to field'

class Config:
    """
        Keeps global addon configuration
    """

    keepBrowserOpened = False

    browserAlwaysOnTop = False

    providers = {}

# --------------------------- Useful function ----------------------------

class Feedback:

    @staticmethod
    def log(*args, **kargs):
        print(args, kargs)

    def showInfo(*args):
        pass

    def showError(*args):
        pass