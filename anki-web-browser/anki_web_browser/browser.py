# Web View, which creates an embedded web browser component
# Main GUI component for this addon

import const
import urllib.parse
from PyQt4.QtGui import QApplication, QMenu, QAction
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView

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

class AwBrowser(QWebView):
    """
        Customization and configuration of a web browser to run within Anki
    """

    _parent = None
    _fields = []
    _selectedListener = None
    
    def __init__(self, myParent):
        QWebView.__init__(self, parent=myParent)
        self._parent = myParent

    def open(self, website, query):
        """
            Loads a given page with its replacing part with its query, and shows itself
        """
        target = website.format(urllib.parse.quote(query))        
        self.load(QUrl.fromEncoded(target))
        self.show()
        return self

    def unload(self):
        print('unload')
        self.setHtml(BLANK_PAGE)

    def onClose(self):
        self._parent = None
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
            hit = self.page().currentFrame().hitTestContent(evt.pos())
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

#   ----------------- getter / setter  -------------------

    def setFields(self, fList):
        print(fList)        # TODO tirar
        self._fields = fList

    def setSelectionListener(self, value):
        self._selectedListener = value



# # Singleton instance for AwBrowser
# instance = None

# def setup(parent):
#     global instance
#     instance = AwBrowser(parent)
