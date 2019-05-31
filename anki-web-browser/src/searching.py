# -*- coding: utf-8 -*-
# Plugin: anki-web-browser - Context menu for notes
# Responsible for adding options in the context menu on Anki notes
# Shows registered providers (websites) to search for the selected sentence
# --------------------------------------------

from .core import Label, Feedback
from .config import service as cfgService
from PyQt5.QtWidgets import QMenu, QAction

class SearchingContext:

    _note = None
    _searchString = None
    _menuAction = None

    def __init__(self, note, query: str, menuFn):
        self._note = note
        if not menuFn:
            raise AttributeError('Callback Fn must be not null')
        self._menuAction = menuFn
        if query:
            self._searchString = query


    def showCustomMenu(self, menuParent):
        """ Builds the addon entry in the context menu, adding options according to the providers """

        if not menuParent:
            raise AttributeError('menuParent must be not null')

        submenu = QMenu(Label.CARD_MENU, menuParent)

        pList = cfgService.getConfig().providers
        for index, prov in enumerate(pList):
            act = QAction('(&' + str(index + 1) + ') ' + prov.name, submenu, 
                triggered=self._makeMenuAction(prov.url))
            submenu.addAction(act)

        if not isinstance(menuParent, QMenu):
            submenu.popup(menuParent.mapToGlobal( menuParent.pos() ))
        else:
            menuParent.addMenu(submenu)


    def _makeMenuAction(self, value):
        """
            Creates correct action for the context menu selection. Otherwise, it would repeat only the last element
        """
        return lambda: self.showInBrowser(value)


    def showInBrowser(self, website):
        if not self._menuAction:
            Feedback.showWarn(_("Error! No Web Browser were found"), period=5000)

        self._menuAction(website, self._searchString)

# -----------------------------------------------------------------------------