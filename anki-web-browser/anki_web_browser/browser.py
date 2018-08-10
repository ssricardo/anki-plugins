# -*- coding: utf-8 -*-

# Web View, which creates an embedded web browser component
# Main GUI component for this addon

import urllib
import config
from PyQt4.QtGui import QApplication, QMenu, QAction, QDialog, QVBoxLayout, QStatusBar, QLabel
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView
# from aqt import *       # FIXME remove direct reference to anki

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
    _urlInfo = None
    
    def __init__(self, myParent):
        QDialog.__init__(self, myParent)
        self._parent = myParent
        self.setupUI()
        
    def setupUI(self):
        self.setWindowTitle('Anki :: Web Browser Addon') 
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.setGeometry(450, 200, 800, 400)
        self.setMinimumWidth (640)
        self.setMinimumHeight(400)

        self._web = QWebView(parent=self)
        self._web.contextMenuEvent = self.contextMenuEvent
        self._web.page().mainFrame().loadStarted.connect(self.onStartLoading)
        self._web.page().mainFrame().loadFinished.connect(self.onLoadFinish)        

        layout.addWidget(self._web)

        self._statusBar = QStatusBar(self)
        self._statusBar.setMaximumHeight(40)
        self._urlInfo = QLabel(self)
        self._statusBar.addPermanentWidget(self._urlInfo)
        layout.addWidget(self._statusBar)

    def open(self, website, query):
        """
            Loads a given page with its replacing part with its query, and shows itself
        """
        target = website.format( query )    # .encode('utf8', 'ignore')
        self._web.load(QUrl.fromEncoded( target ))      # urllib.quote(target)
        self._urlInfo.setText(target)
        
        self.show()
        return self._web

    def unload(self):
        self._web.setHtml(BLANK_PAGE)

    def onClose(self):
        self._parent = None
        self._web.close()
        self.close()

    def onStartLoading(self):
        self._statusBar.showMessage('Loading...')

    def onLoadFinish(self, result):
        self._statusBar.clearMessage()
        if not result:
            self._statusBar.showMessage('Error on loading page', 5000)
            print('Error on loading page! ', result)


# ------------------------------------ Menu ---------------------------------------

    def _makeMenuAction(self, field, value, isLink):
        """
            Creates correct operations for the context menu selection.
            Only with lambda, it would repeat only the last element
        """

        return lambda: self._selectedListener.handleSelection(field, value, isLink)

    def contextMenuEvent(self, evt):
        """
            Handles the context menu in the web view. 
            Shows and handle options (from field list), only if in edit mode.
        """

        if not (self._fields and self._selectedListener):
            return
        
        isLink = False
        value = None
        if self._web.selectedText():
            isLink = False
            value = self._web.selectedText()
        else:
            hit = self._web.page().currentFrame().hitTestContent(evt.pos())

            if hit.imageUrl():
                isLink = True
                value = hit.imageUrl().toEncoded()

        if not value:
            return

        self.createCtxMenu(value, isLink, evt)

    def createCtxMenu(self, value, isLink, evt):
        'Creates and configures the menu itself'
        
        m = QMenu(self)
        sub = QMenu(config.Label.BROWSER_ASSIGN_TO, m)
        m.setTitle(config.Label.BROWSER_ASSIGN_TO)
        for index, label in self._fields.items():
            act = QAction(label, m, 
                triggered=self._makeMenuAction(index, value, isLink))
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

