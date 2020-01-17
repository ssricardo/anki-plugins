# -*- coding: utf-8 -*-

# Web View, which creates an embedded web browser component
# Main GUI component for this addon
# ---------------------------------------

import urllib.parse
from datetime import datetime
from textwrap import shorten
from .config import service as cfg
from .core import Label, Feedback, Style
from .provider_selection import ProviderSelectionController
from .exception_handler import exceptionHandler

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QImage, QMouseEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, Qt, QSize, QEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineContextMenuData

import os

CWD = os.path.dirname(os.path.realpath(__file__))

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
    TITLE = 'Anki :: Web Browser Addon'

    _parent = None
    _fields = []
    _selectionHandler = None
    _web = None
    _context = None
    _lastAssignedField = None
    infoList = []
    providerList = []
    
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
        self.setWindowTitle(AwBrowser.TITLE)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setGeometry(450, 200, 800, 450)        
        self.setMinimumWidth (640)
        self.setMinimumHeight(450)
        self.setStyleSheet(Style.DARK_BG)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)

        self._web = QWebEngineView(self)
        self._web.contextMenuEvent = self.contextMenuEvent
        self._web.page().loadStarted.connect(self.onStartLoading)
        self._web.page().loadFinished.connect(self.onLoadFinish)
        self._web.page().loadProgress.connect(self.onProgress)
        self._web.page().urlChanged.connect(self.onPageChange)

        # -------------------- Top / toolbar ----------------------
        navtbar = QToolBar("Navigation")
        navtbar.setIconSize( QSize(16,16) )
        mainLayout.addWidget(navtbar)

        backBtn = QAction( QtGui.QIcon(os.path.join(CWD, 'assets', 'arrow-back.png')), "Back", self)
        backBtn.setStatusTip("Back to previous page")
        backBtn.triggered.connect( self._web.back )
        navtbar.addAction(backBtn)        

        self.forwardBtn = QAction( QtGui.QIcon(os.path.join(CWD, 'assets', 'arrow-forward.png')), "Forward", self)
        self.forwardBtn.setStatusTip("Next visited page")
        self.forwardBtn.triggered.connect( self._web.forward )
        navtbar.addAction(self.forwardBtn)

        refreshBtn = QAction( QtGui.QIcon(os.path.join(CWD, 'assets', 'reload.png')), "Reload", self)
        refreshBtn.setStatusTip("Reload")
        refreshBtn.triggered.connect( self._web.reload )
        navtbar.addAction(refreshBtn)

        self.createProvidersMenu(navtbar)

        self._itAddress = QtWidgets.QLineEdit(self)
        self._itAddress.setObjectName("itSite")
        self._itAddress.setStyleSheet('background-color: #F5F5F5;')
        self._itAddress.returnPressed.connect(self._goToAddress)
        navtbar.addWidget(self._itAddress)

        cbGo = QAction( QtGui.QIcon(os.path.join(CWD, 'assets','go-icon.png')), "Go", self)
        cbGo.setObjectName("cbGo")
        navtbar.addAction(cbGo)
        cbGo.triggered.connect(self._goToAddress)

        self.stopBtn = QAction( QtGui.QIcon(os.path.join(CWD, 'assets','stop.png')), "Stop", self)
        self.stopBtn.setStatusTip("Stop loading")
        self.stopBtn.triggered.connect( self._web.stop )
        navtbar.addAction(self.stopBtn)
        # -------------------- Center ----------------------
        mainLayout.addWidget(self._web)
        # -------------------- Bottom bar ----------------------
        
        bottomWidget = QtWidgets.QWidget(self)
        bottomWidget.setFixedHeight(30)

        bottomLayout = QtWidgets.QHBoxLayout(bottomWidget)
        bottomLayout.setObjectName("bottomLayout")
        bottomWidget.setStyleSheet('color: #FFF;')
        
        lbSite = QtWidgets.QLabel(bottomWidget)
        lbSite.setObjectName("label")
        lbSite.setText("Context: ")
        lbSite.setFixedWidth(70)
        lbSite.setStyleSheet('font-weight: bold;')
        bottomLayout.addWidget(lbSite)

        self.ctxWidget = QtWidgets.QLabel(bottomWidget)
        self.ctxWidget.width = 300
        self.ctxWidget.setStyleSheet('text-align: left;')
        bottomLayout.addWidget(self.ctxWidget)        

        self._loadingBar = QtWidgets.QProgressBar(bottomWidget)
        self._loadingBar.setFixedWidth(100)
        self._loadingBar.setProperty("value", 100)
        self._loadingBar.setObjectName("loadingBar")
        bottomLayout.addWidget(self._loadingBar)

        mainLayout.addWidget(bottomWidget)

        if cfg.getConfig().browserAlwaysOnTop:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)


    # def dragEnterEvent(self, e):
    #     print('Enter: ')
    #     print(e.mimeData().formats())
    #     print(e.mimeData().text())
    #     print(e.mimeData().urls())
    #     QApplication.clipboard().setMimeData(e.mimeData())

        # e.mimeData().clear()

        # if (e.mimeData().urls()):
        #     url = e.mimeData().urls()[0]
        #     if self._checkSuffix(url):
        #         data = url.toEncoded()
        #         e.mimeData().clear()
        #         e.mimeData().setData('application/octet-stream', data)
        #         # e.mimeData().setImageData(QImage(url.toString(), 'image/png'))
        #         # e.mimeData().setUrls([])
        #         # e.mimeData().setHtml(None)
        #         # e.mimeData().setText(None)

        # print(e.mimeData().formats())

        # e.accept()

        # if e.mimeData().hasText() or e.mimeData().hasHtml() or e.mimeData().hasImage():
        #     e.accept()
        #     print('accepted')
        # else:
        #     e.ignore()
        #     print('ignored')

    @classmethod
    def singleton(clz, parent):
        if not clz.SINGLETON:
            clz.SINGLETON = AwBrowser(parent)
        return clz.SINGLETON

    def formatTargetURL(self, website: str, query: str = ''):
        return website.format(urllib.parse.quote(query, encoding='utf8'))

    @exceptionHandler
    def open(self, website, query: str):
        """
            Loads a given page with its replacing part with its query, and shows itself
        """

        self._context = query
        self._updateContextWidget()        
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
        self.stopBtn.setEnabled(True)
        self._loadingBar.setProperty("value", 1)

    def onProgress(self, prog):
        self._loadingBar.setProperty("value", prog)

    def onLoadFinish(self, result):
        self.stopBtn.setDisabled(True)    
        self._loadingBar.setProperty("value", 100)

        if not result:
            Feedback.log('No result on loading page! ')

    def _goToAddress(self):
        q = QUrl( self._itAddress.text() )
        if q.scheme() == "":
            q.setScheme("http")

        self._web.load(q)
        self._web.show()
    
    def onPageChange(self, url):
        if url and url.toString().startswith('http'):
            self._itAddress.setText(url.toString())
        self.forwardBtn.setEnabled( self._web.history().canGoForward() ) 

    def welcome(self):        
        self._web.setHtml(WELCOME_PAGE)
        self._itAddress.setText('about:blank')
        self.show()
        self.raise_()

    def _updateContextWidget(self):
        self.ctxWidget.setText(self._context)

# ---------------------------------------------------------------------------------
    def createProvidersMenu(self, parentWidget):
        providerBtn = QAction( QtGui.QIcon(os.path.join(CWD, 'assets', 'gear-icon.png')), "Providers", parentWidget)
        providerBtn.setStatusTip("Search with Provider")
        providerBtn.triggered.connect( lambda: self.newProviderMenu(providerBtn) )
        parentWidget.addAction(providerBtn)

    def newProviderMenu(self, parentBtn):
        ctx = ProviderSelectionController()
        ctx.showCustomMenu(parentBtn.parentWidget(), self.reOpenSameQuery)

    @exceptionHandler
    def reOpenSameQuery(self, website):
        self.open(website, self._context)


# ------------------------------------ Menu ---------------------------------------

    def _makeMenuAction(self, field, value, isLink):
        """
            Creates correct operations for the context menu selection.
            Only with lambda, it would repeat only the last element
        """

        def _processMenuSelection():
            self._lastAssignedField = field
            self._selectionHandler(field, value, isLink)

        return _processMenuSelection


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


        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            if self._assignToLastField(value, isLink):
                return

        self.createCtxMenu(value, isLink, evt)


    def _checkSuffix(self, value):
        if value and not value.toString().endswith(("jpg", "jpeg", "png", "gif")):
            msgLink = value.toString()
            if len(value.toString()) < 80:
                msgLink = msgLink[:50] + '...' + msgLink[50:]
            answ = QMessageBox.question(self, 'Anki support', 
                """This link may not be accepted by Anki: \n\n "%s" \n
Usually the suffix should be one of 
(jpg, jpeg, png, gif).
Try it anyway? """ % msgLink, QMessageBox.Yes|QMessageBox.No)

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


    def _assignToLastField(self, value, isLink):
        'Tries to set the new value to the same field used before, if set...'

        if self._lastAssignedField:
            if self._lastAssignedField in self._fields:
                self._selectionHandler(self._lastAssignedField, value, isLink)
                return True
            else:
                self._lastAssignedField = None
        return False

    
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