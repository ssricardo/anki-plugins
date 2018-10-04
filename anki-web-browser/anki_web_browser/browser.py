# -*- coding: utf-8 -*-

# Web View, which creates an embedded web browser component
# Main GUI component for this addon
# ---------------------------------------

import urllib.parse
from .config import service as cfg
from .core import Label, Feedback

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QDialog, QVBoxLayout, QStatusBar, QLabel
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineContextMenuData
from requests.utils import requote_uri

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
            <h1>Nothing loaded...</h1>
        </body>   
    </html>
"""

WELCOME_PAGE = """
    <html>
        <style type="text/css">
            body {
                margin-top: 30px;
                background-color: #F5F5F5;
                color: 003366;
            }

            p {
                margin-bottom: 20px;
            }
        </style>
        <body>   
            <h1>Welcome</h1>
            <hr />

            <div>
                Anki-Web-Browser is installed!
            </div>
            <p>
                Its use is pretty simple.<br />
                It is based on <i>text selecting</i> and <i>context menu</i>.
            </p>
            <div>
                Check more details on the <a href="#">documentation</a>
            </div>
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
        self.setGeometry(450, 200, 800, 450)
        self.setMinimumWidth (640)
        self.setMinimumHeight(450)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)

        topWidget = QtWidgets.QWidget(self)
        topWidget.setFixedHeight(50)

        topLayout = QtWidgets.QHBoxLayout(topWidget)
        topLayout.setObjectName("topLayout")
        
        lbSite = QtWidgets.QLabel(topWidget)
        lbSite.setObjectName("label")
        lbSite.setText("Website: ")

        topLayout.addWidget(lbSite)
        self._itAddress = QtWidgets.QLineEdit(topWidget)
        self._itAddress.setObjectName("itSite")
        topLayout.addWidget(self._itAddress)
        cbGo = QtWidgets.QCommandLinkButton(topWidget)
        cbGo.setObjectName("cbGo")
        cbGo.setFixedSize(30, 30)
        topLayout.addWidget(cbGo)
        # cbImport = QtWidgets.QCommandLinkButton(topWidget)
        # cbImport.setObjectName("cbImport")
        # cbImport.setFixedSize(30, 30)
        # topLayout.addWidget(cbImport)
        self._loadingBar = QtWidgets.QProgressBar(topWidget)
        self._loadingBar.setFixedWidth(100)
        self._loadingBar.setProperty("value", 100)
        self._loadingBar.setObjectName("loadingBar")
        topLayout.addWidget(self._loadingBar)

        mainLayout.addWidget(topWidget)

        self._web = QWebEngineView(self)
        self._web.contextMenuEvent = self.contextMenuEvent
        self._web.page().loadStarted.connect(self.onStartLoading)
        self._web.page().loadFinished.connect(self.onLoadFinish)
        self._web.page().loadProgress.connect(self.onProgress)
        self._web.page().urlChanged.connect(self.onPageChange)

        cbGo.clicked.connect(self._goToAddress)

        mainLayout.addWidget(self._web)

        if cfg.getConfig().browserAlwaysOnTop:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def open(self, website, query: str):
        """
            Loads a given page with its replacing part with its query, and shows itself
        """

        target = website.format(urllib.parse.quote(query, encoding='utf8'))  #encode('utf8', 'ignore')
        self._web.load(QUrl( target ))
        self._itAddress.setText(target)
        
        self.show()
        return self._web

    def unload(self):
        self._web.setHtml(BLANK_PAGE)

    def onClose(self):
        self._parent = None
        self._web.close()
        self.close()

    def onStartLoading(self):
        self._loadingBar.setProperty("value", 1)

    def onProgress(self, prog):
        self._loadingBar.setProperty("value", prog)

    def onLoadFinish(self, result):
        self._loadingBar.setProperty("value", 100)
        if not result:
            Feedback.showInfo('Error loading page')
            Feedback.log('Error on loading page! ', result)

    def _goToAddress(self):
        self._web.load(QUrl( self._itAddress.text() ))
        self._web.show()
    
    def onPageChange(self, url):
        self._itAddress.setText(url.toString())

    def welcome(self):
        self._web.setHtml(WELCOME_PAGE)
        self.show()

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
            if (self._web.page().contextMenuData().mediaType() == QWebEngineContextMenuData.MediaTypeImage
                    and self._web.page().contextMenuData().mediaUrl()):
                isLink = True
                value = self._web.page().contextMenuData().mediaUrl()

        if not value:
            return

        self.createCtxMenu(value, isLink, evt)

    def createCtxMenu(self, value, isLink, evt):
        'Creates and configures the menu itself'
        
        m = QMenu(self)
        sub = QMenu(Label.BROWSER_ASSIGN_TO, m)
        m.setTitle(Label.BROWSER_ASSIGN_TO)
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
