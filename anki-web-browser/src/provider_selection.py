# -*- coding: utf-8 -*-
# Plugin: anki-web-browser - Context menu for notes
# Responsible for adding options in the context menu on Anki notes
# Shows registered providers (websites) to search for the selected sentence
# --------------------------------------------

from .core import Label, Feedback, Style
from .config import service as cfgService
from PyQt5.QtWidgets import QMenu, QAction


class ProviderSelectionController:

    _providerList = []

    def __init__(self):
        self._providerList = cfgService.getConfig().providers


    def showCustomMenu(self, menuParent, menuFn):
        """ Builds the addon entry in the context menu, adding options according to the providers """

        if not menuFn:
            raise AttributeError('Callback Fn must be not null')

        if not menuParent:
            raise AttributeError('menuParent must be not null')

        submenu = QMenu(Label.CARD_MENU, menuParent)
        submenu.setStyleSheet(Style.MENU_STYLE)

        pList = self._providerList
        for index, prov in enumerate(pList):
            act = QAction('(&' + str(index + 1) + ') ' + prov.name, submenu, 
                triggered=self._makeMenuAction(prov.url, menuFn))
            submenu.addAction(act)

        if not isinstance(menuParent, QMenu):
            submenu.popup(menuParent.mapToGlobal( menuParent.pos() ))
        else:
            menuParent.addMenu(submenu)


    def _makeMenuAction(self, value, menuCallback):
        """
            Creates correct action for the context menu selection. Otherwise, it would repeat only the last element
        """
        return lambda: menuCallback(value)


# -----------------------------------------------------------------------------