# -*- coding: utf-8 -*-
# Contains center components useful across this addon
# Holds Contansts

# This files is part of anki-web-browser addon
# @author ricardo saturnino
# ------------------------------------------------


class Label:
    CARD_MENU = 'Search on &Web'
    BROWSER_ASSIGN_TO = 'Assign to field:'


# --------------------------- Useful function ----------------------------

class Feedback:
    'Responsible for messages and logs'

    @staticmethod
    def log(*args, **kargs):
        # pass
        print(args, kargs)
        # import os
        # import config
        # if not os.path.exists (config.currentLocation + '/ab.log'):
        # f = open(config.currentLocation + '/ab.log', 'w')
        # f.write(args)
        # f.close()

    @staticmethod
    def showInfo(*args):
        pass

    @staticmethod
    def showWarn(*args):
        pass

    @staticmethod
    def showError(*args):
        pass