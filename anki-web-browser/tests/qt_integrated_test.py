# A test for GUI components integrated with the framework used
# Uses PyQt4
# Must not be packed within the distributable file

import sys
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../anki_web_browser')

import browser

def wiki(self):
    print('Load')
    self.load(QUrl('https://en.wikipedia.org'))

def menu(self, evt):
    mn = QMenu(self)
    ac1 = QAction('Unload', mn, 
            triggered=lambda: self.unload())
    mn.addAction(ac1)

    ac2 = QAction('Close', mn, 
            triggered=lambda: self.onClose())
    mn.addAction(ac2)

    ac3 = QAction('Wikipedia', mn, 
            triggered=lambda: wiki(self))
    mn.addAction(ac3)

    ac4 = QAction('Print link', mn, 
            triggered=lambda: print(self.linkUrl()))
    mn.addAction(ac4)

    ac4 = QAction('Print text', mn, 
            triggered=lambda: print(self.selectedText()))
    mn.addAction(ac4)

    action = mn.exec_(self.mapToGlobal(evt.pos()))

#browser.AwBrowser.contextMenuEvent = menu

def onSelected(field, value, isLink):
        print('Field {} (link? {}): {}'.format(field, isLink, value))

if __name__ == '__main__':
    print('Running Qt App')
    app = QApplication(sys.argv)
    browser.setup(None)
    web = browser.instance
    web.setSelectionListener(onSelected)
    web.setFields([
        {'name': 'Front'},
        {'name': 'Back'},
        {'name': 'Example'}
    ])
    web.load(QUrl('https://images.google.com/'))
    web.show()
    sys.exit(app.exec_())