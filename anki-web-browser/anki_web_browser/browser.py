# TODO

import urllib
from PyQt4.QtGui import QApplication, QMenu, QAction
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView

class AwBrowser(QWebView):
    """
        Customization and configuration of a web browser to run within Anki
    """
    
    def __init__(self):
        QWebView.__init__(self)

    def open(self, website, query):
        target = website.format(urllib.quote(query))        
        self.load(QUrl.fromEncoded(target))
        self.show()
        return self

