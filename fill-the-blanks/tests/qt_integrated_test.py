# A test for GUI components integrated with the framework used
# Uses PyQt4
# Must not be packed within the distributable file

import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../../anki-web-browser')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../src')

import anki_web_browser.browser as brw
from  controller import Controller
from inspector import Inspector

def wiki(self):
    print('Load')
    self.load(QUrl('https://en.wikipedia.org'))

if __name__ == '__main__':
    print('Running Qt App')
    app = QApplication(sys.argv)
    web = brw.AwBrowser(None)
    # ctr = Controller(None)
    web.open('https://www.google.com/?q={}', 'my app test')
    # ctr.setupBindings(web._web)
    insp = Inspector(web)
    insp.inspect(web._web)
    web.show()
    sys.exit(app.exec_())