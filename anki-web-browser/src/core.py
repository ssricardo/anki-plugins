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
        try:
            pass
            # print(args, kargs)
        except:
            pass

    @staticmethod
    def showInfo(*args):
        pass

    @staticmethod
    def showWarn(*args):
        pass

    @staticmethod
    def showError(*args):
        pass

class Style:

    DARK_BG = """
        QMessageBox {
            background-color: #FFFFBB;
            color: #FFF;
        }
        AwBrowser {
            background-color: #152032;
        }
        QLineEdit {
            color: #000;
        }
    """
    
    # "background-color: #152032;"
    MENU_STYLE = """
            QMenu {
                background-color: #B0C4DE;
                color: #333;
            }
            QMenu::item:selected {
                background-color: #6495ED;
            }
        """