# anki-web-browser - UI Components

from PyQt4.QtGui import QMenu

class NoteMenuBuilder:
    _providers = {}
    _menu = QMenu()

    def __init__(self):
        self.updateMenu()

    def updateMenu(self):
        pass

    def providers(self, newValue: dict):
        if newValue:
            self._providers = newValue
        self.updateMenu()

class AwBrowser():
    pass

