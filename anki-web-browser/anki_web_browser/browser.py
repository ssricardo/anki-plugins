# TODO

import urllib.parse
from PyQt4.QtGui import QApplication, QMenu, QAction
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView

BLANK_PAGE = """
    <html>
        <style type="text/css">
            body {
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
    _note = None
    
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
        self.html = BLANK_PAGE

    def onClose(self):
        self._parent = None
        self.close()

    def setNote(self, note):
        self._note = note

    def onContextMenu(self, evt):
        print(self.selectedText())

        hit = self.page().currentFrame().hitTestContent(evt.pos())
        
        print('Text: ', hit.linkText())
        print(hit.isContentSelected())
        print(hit.linkUrl())

        if not self._note:
            return

        m = QMenu(self)
        for f in self._note.fields:
            act = QAction('Add selection to ', m, 
                triggered=lambda: print(f))
            m.addAction(act)

        action = m.exec_(self.mapToGlobal(evt.pos()))
