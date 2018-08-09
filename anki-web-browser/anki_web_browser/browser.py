# Web View, which creates an embedded web browser component
# Main GUI component for this addon

import const
import urllib
from PyQt4.QtGui import QApplication, QMenu, QAction, QDialog, QVBoxLayout
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView
# from PyQt4.Qt import Qt
from aqt import *       # FIXME improve this

BLANK_PAGE = """
    <html>
        <style type="text/css">
            body {
                margin-top: 30px;
                background-color: #F5F5F5;
                color: CCC;
            }
        </style>
        <body>   
            <p>Nothing loaded...</p>
        </body>   
    </html>
"""

class AwBrowser(QDialog):
    """
        Customization and configuration of a web browser to run within Anki
    """

    _parent = None
    _fields = []
    _selectedListener = None
    _web = None
    
    def __init__(self, myParent):
        QDialog.__init__(self, myParent)  # , Qt.Window
        # QWebView.__init__(self, parent=myParent)
        self._parent = myParent
        # sppliter = QSplitter(self)

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        # self.widget.setLayout(l)

        self._web = QWebView(parent=self)
        self._web.contextMenuEvent = self.contextMenuEvent
        layout.addWidget(self._web)
        self.setWindowTitle('Anki :: Web Browser Addon') 

        self.setGeometry(450, 200, 800, 400)        # TODO re check
        self.setMinimumWidth (640)
        self.setMinimumHeight(400)
        # myParent.setCentralWidget(self)

    def open(self, website, query):
        """
            Loads a given page with its replacing part with its query, and shows itself
        """
        target = website.format(query)         # urllib.parse.quote(
        self._web.load(QUrl.fromEncoded(target))
        
        
        self.show()
        return self

    def unload(self):
        print('unload')
        self._web.setHtml(BLANK_PAGE)

    def onClose(self):
        self._parent = None
        self._web.close()
        self.close()

    def _makeMenuAction(self, field, value, isLink):
        return lambda: self._selectedListener.handleSelection(field, value, isLink)

    def contextMenuEvent(self, evt):
        if not (self._fields and self._selectedListener):
            return
        
        isLink = False
        value = None
        if self.selectedText():
            isLink = False
            value = self.selectedText()
        else:
            hit = self._web.page().currentFrame().hitTestContent(evt.pos())
            if hit.linkText():
                isLink = True
                value = hit.linkUrl()

        if not value:
            return

        m = QMenu(self)
        sub = QMenu(const.Label.BROWSER_ASSIGN_TO, m)
        m.setTitle(const.Label.BROWSER_ASSIGN_TO)
        for index, f in enumerate(self._fields):
            print(f)
            act = QAction(f['name'], m, 
                triggered=self._makeMenuAction(f, value, isLink))  #FIXME
            sub.addAction(act)

        m.addMenu(sub)
        action = m.exec_(self.mapToGlobal(evt.pos()))

    def load(self, qUrl):
        self._web.load(qUrl)

#   ----------------- getter / setter  -------------------

    def setFields(self, fList):
        self._fields = fList

    def setSelectionListener(self, value):
        self._selectedListener = value



# # Singleton instance for AwBrowser
# instance = None

# def setup(parent):
#     global instance
#     instance = AwBrowser(parent)
