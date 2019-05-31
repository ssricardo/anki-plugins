# -*- coding: utf-8 -*-

# Web View, which creates an embedded web browser component
# Main GUI component for this addon
# ---------------------------------------

import urllib.parse
from .config import service as cfg
from .core import Label, Feedback

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineContextMenuData

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
                It is based on <i>text selecting</i> and <i>context menu</i> (or shortcut).
            </p>
            <div>
                Check more details on the <a href="https://github.com/ssricardo/anki-plugins/tree/master/anki-web-browser">documentation</a>
            </div>
        </body>   
    </html>
"""

class AwBrowser(QDialog):
    """
        Customization and configuration of a web browser to run within Anki
    """

    SINGLETON = None

    _parent = None
    _fields = []
    _selectionHandler = None
    _web = None
    _urlInfo = None
    infoList = []
    
    def __init__(self, myParent):
        QDialog.__init__(self, None)
        self._parent = myParent
        self.setupUI()

        if myParent:
            def wrapClose(fn):
                def clozeBrowser(evt):                    
                    self.close()
                    fn(evt)
                return clozeBrowser
            myParent.closeEvent = wrapClose(myParent.closeEvent)
        
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

    @classmethod
    def singleton(clz, parent):
        if not clz.SINGLETON:
            clz.SINGLETON = AwBrowser(parent)
        return clz.SINGLETON

    def formatTargetURL(self, website: str, query: str = ''):
        return website.format(urllib.parse.quote(query, encoding='utf8'))

    def open(self, website, query: str):
        """
            Loads a given page with its replacing part with its query, and shows itself
        """

        target = self.formatTargetURL(website, query)
        self._web.load(QUrl( target ))
        self._itAddress.setText(target)
        
        self.show()
        self.raise_()
        return self._web

    def unload(self):
        try:
            self._web.setHtml(BLANK_PAGE)
            self._itAddress.setText('about:blank')
        except (RuntimeError) as err:
            pass

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
        if url and url.toString().startswith('http'):
            self._itAddress.setText(url.toString())

    def welcome(self):        
        self._web.setHtml(WELCOME_PAGE)
        self._itAddress.setText('about:blank')
        self.show()

# ------------------------------------ Menu ---------------------------------------

    def _makeMenuAction(self, field, value, isLink):
        """
            Creates correct operations for the context menu selection.
            Only with lambda, it would repeat only the last element
        """

        return lambda: self._selectionHandler(field, value, isLink)

    def contextMenuEvent(self, evt):
        """
            Handles the context menu in the web view. 
            Shows and handle options (from field list), only if in edit mode.
        """

        if not (self._fields and self._selectionHandler):
            return self.createInfoMenu(evt)

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
                Feedback.log('Link: '+ value.toString())
                Feedback.log('toLocal: ' + value.toLocalFile())             

                if not self._checkSuffix(value):
                    return

        if not value:
            Feedback.log('No value')
            return self.createInfoMenu(evt)

        self.createCtxMenu(value, isLink, evt)

    def _checkSuffix(self, value):
        if value and not value.toString().endswith(("jpg", "jpeg", "png", "gif")):
            answ = QMessageBox.question(self, 'Anki support', 
                """This link may not be accepted by Anki. 
Usually the suffix should be one of 
(jpg, jpeg, png, gif).
Try it anyway? """, QMessageBox.Yes|QMessageBox.No)

            if answ != QMessageBox.Yes:
                return False

        return True

    def createCtxMenu(self, value, isLink, evt):
        'Creates and configures the menu itself'
        
        m = QMenu(self)
        m.addAction(QAction('Copy',  m, 
            triggered=lambda: self._copy(value)))
        m.addSeparator()

        labelAct = QAction(Label.BROWSER_ASSIGN_TO, m)
        labelAct.setDisabled(True)
        m.addAction(labelAct)
        # sub = QMenu(Label.BROWSER_ASSIGN_TO, m)
        m.setTitle(Label.BROWSER_ASSIGN_TO)
        for index, label in self._fields.items():
            act = QAction(label, m, 
                triggered=self._makeMenuAction(index, value, isLink))
            m.addAction(act)

        # m.addMenu(sub)
        action = m.exec_(self.mapToGlobal(evt.pos()))


    def createInfoMenu(self, evt):
        'Creates and configures a menu with only some information'
        m = QMenu(self)
        for item in self.infoList:
            act = QAction(item)
            act.setEnabled(False)
            m.addAction(act)
        action = m.exec_(self.mapToGlobal(evt.pos()))

    
    def _copy(self, value):
        if not value:
            return
        clip = QApplication.clipboard()        
        clip.setText(value if isinstance(value, str) else value.toString())


    def load(self, qUrl):
        self._web.load(qUrl)

#   ----------------- getter / setter  -------------------

    def setFields(self, fList):
        self._fields = fList

    def setSelectionHandler(self, value):
        self._selectionHandler = value