# -*- coding: utf-8 -*-

# --------------------------------------------------------
# Web browser main dialog
# Main GUI component for this addon
# --------------------------------------------------------

import os
import urllib.parse

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QUrl, Qt, QSize, QObject
from PyQt5.QtGui import QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineContextMenuData, QWebEngineSettings, QWebEnginePage
from PyQt5.QtWidgets import *

from .config import service as cfg
from .core import Label, Feedback, Style, CWD
from .exception_handler import exceptionHandler
from .provider_selection import ProviderSelectionController

from .browser_context_menu import AwBrowserMenu, StandardMenuOption
from .browser_engine import AwWebEngine

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
                Now it's also possible to use it without selecting a text.
            </p>
            <div>
                Check more details on the <a href="https://github.com/ssricardo/anki-plugins/tree/master/anki-web-browser">documentation</a>
            </div>
        </body>   
    </html>
"""


# noinspection PyPep8Naming
class AwBrowser(QMainWindow):
    """
        Customization and configuration of a web browser to run within Anki
    """

    SINGLETON = None
    TITLE = 'Anki :: Web Browser Addon'

    _parent = None
    _web = None
    _context = None
    _currentWeb = None

    providerList = []

    def __init__(self, myParent: QWidget, sizingConfig: tuple):
        QDialog.__init__(self, None)
        self._parent = myParent
        self.setupUI(sizingConfig)
        self._setupShortcuts()

        self._menuDelegator = AwBrowserMenu([
            StandardMenuOption('Open in new tab', lambda add: self.openUrl(add, True))
        ])

        if myParent:
            def wrapClose(fn):
                def kloseBrowser(evt):
                    self.close()
                    self.deleteLater()
                    return fn(evt)
                return kloseBrowser
            myParent.closeEvent = wrapClose(myParent.closeEvent)

    @classmethod
    def singleton(cls, parent, sizeConfig: tuple):
        if not cls.SINGLETON:
            cls.SINGLETON = AwBrowser(parent, sizeConfig)
        return cls.SINGLETON

    # ======================================== View setup =======================================

    def setupUI(self, widthHeight: tuple):
        self.setWindowTitle(AwBrowser.TITLE)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setGeometry(400, 200, widthHeight[0], widthHeight[1])
        self.setMinimumWidth(640)
        self.setMinimumHeight(450)
        self.setStyleSheet(Style.DARK_BG)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # -------------------- Top / toolbar ----------------------
        navtbar = QToolBar("Navigation")
        navtbar.setIconSize(QSize(16, 16))
        mainLayout.addWidget(navtbar)

        self.backBtn = QAction(QtGui.QIcon(os.path.join(CWD, 'assets', 'arrow-back.png')), "Back", self)
        self.backBtn.setStatusTip("Back to previous page")
        navtbar.addAction(self.backBtn)
        self.backBtn.triggered.connect(self._onBack)

        self.forwardBtn = QAction(QtGui.QIcon(os.path.join(CWD, 'assets', 'arrow-forward.png')), "Forward", self)
        self.forwardBtn.setStatusTip("Next visited page")
        navtbar.addAction(self.forwardBtn)
        self.forwardBtn.triggered.connect(self._onForward)

        self.refreshBtn = QAction(QtGui.QIcon(os.path.join(CWD, 'assets', 'reload.png')), "Reload", self)
        self.refreshBtn.setStatusTip("Reload")
        navtbar.addAction(self.refreshBtn)
        self.refreshBtn.triggered.connect(self._onReload)

        self.createProvidersMenu(navtbar)

        self.newTabBtn = QAction(QtGui.QIcon(os.path.join(CWD, 'assets', 'plus-signal.png')), "New Tab", self)
        self.newTabBtn.setStatusTip("New tab")
        navtbar.addAction(self.newTabBtn)
        self.newTabBtn.triggered.connect(lambda: self.add_new_tab())

        self._itAddress = QtWidgets.QLineEdit(self)
        self._itAddress.setObjectName("itSite")
        self._itAddress.setStyleSheet('background-color: #F5F5F5;')
        self._itAddress.returnPressed.connect(self._goToAddress)
        navtbar.addWidget(self._itAddress)

        cbGo = QAction(QtGui.QIcon(os.path.join(CWD, 'assets', 'go-icon.png')), "Go", self)
        cbGo.setObjectName("cbGo")
        navtbar.addAction(cbGo)
        cbGo.triggered.connect(self._goToAddress)

        self.stopBtn = QAction(QtGui.QIcon(os.path.join(CWD, 'assets', 'stop.png')), "Stop", self)
        self.stopBtn.setStatusTip("Stop loading")
        self.stopBtn.triggered.connect(self._onStopPressed)

        navtbar.addAction(self.stopBtn)


        # -------------------- Center ----------------------
        widget = QWidget()
        widget.setLayout(mainLayout)

        self.setCentralWidget(widget)

        self._tabs = QTabWidget()
        self._tabs.setDocumentMode(True)
        self._tabs.currentChanged.connect(self.current_tab_changed)
        self._tabs.setTabsClosable(True)
        self._tabs.tabCloseRequested.connect(self.close_current_tab)

        mainLayout.addWidget(self._tabs)
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

    def _setupShortcuts(self):
        newTabShort = QShortcut(QtGui.QKeySequence("Ctrl+t"), self)
        newTabShort.activated.connect(self.add_new_tab)
        closeTabShort = QShortcut(QtGui.QKeySequence("Ctrl+w"), self)
        closeTabShort.activated.connect(lambda: self.close_current_tab(self._tabs.currentIndex()))
        providersShort = QShortcut(QtGui.QKeySequence("Ctrl+p"), self)
        providersShort.activated.connect(lambda: self.newProviderMenu())
        providerNewTab = QShortcut(QtGui.QKeySequence("Ctrl+n"), self)
        providerNewTab.activated.connect(lambda: self.newProviderMenu(True))

    # ======================================== Tabs =======================================

    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            qurl = QUrl('')

        browser = AwWebEngine(self)
        browser.setUrl(qurl)
        browser.contextMenuEvent = self._menuDelegator.contextMenuEvent
        browser.page().loadStarted.connect(self.onStartLoading)
        browser.page().loadFinished.connect(self.onLoadFinish)
        browser.page().loadProgress.connect(self.onProgress)
        browser.page().urlChanged.connect(self.onPageChange)

        i = self._tabs.addTab(browser, label)
        self._tabs.setCurrentIndex(i)
        self._currentWeb = self._tabs.currentWidget()
        self._menuDelegator.setCurrentWeb(self._currentWeb)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(self.updateTabTitle(i, browser))

    def current_tab_changed(self, i):
        self._currentWeb = self._tabs.currentWidget()
        self._menuDelegator.setCurrentWeb(self._tabs.currentWidget())

        if self._tabs.currentWidget():
            qurl = self._tabs.currentWidget().url()
            self.update_urlbar(qurl, self._tabs.currentWidget())

        self._updateButtons()

    def close_current_tab(self, i):
        Feedback.log('Close current tab with index: %d' % i)
        if self._tabs.count() < 2:
            if self._currentWeb:
                self._currentWeb.setUrl(QUrl('about:blank'))
            return

        self._tabs.currentWidget().deleteLater()
        self._tabs.setCurrentWidget(None)
        self._tabs.removeTab(i)

    def update_urlbar(self, q, browser=None):
        if browser != self._tabs.currentWidget():
            return

        self._itAddress.setText(q.toString())
        self._itAddress.setCursorPosition(0)

    def updateTabTitle(self, index: int, browser: QWebEngineView):
        def fn():
            title = browser.page().title() if len(browser.page().title()) < 18 else (browser.page().title()[:15] + '...')
            self._tabs.setTabText(index, title)
        return fn

    # =================================== General control ======================

    def formatTargetURL(self, website: str, query: str = ''):
        return website.format(urllib.parse.quote(query, encoding='utf8'))

    @exceptionHandler
    def open(self, website, query: str, bringUp=False):
        """
            Loads a given page with its replacing part with its query, and shows itself
        """

        self._context = query
        self._updateContextWidget()
        target = self.formatTargetURL(website, query)

        self.openUrl(target)

        if bringUp:
            self.show()
            self.raise_()

    def openUrl(self, address: str, newTab=False):
        if self._tabs.count() == 0 or newTab:
            self.add_new_tab(QUrl(address), 'Loading...')
        elif self._currentWeb:
            self._currentWeb.setUrl(QUrl(address))

    def clearContext(self):
        numTabs = self._tabs.count()
        if numTabs == 0:
            return
        for tb in range(numTabs, 0, -1):
            self.close_current_tab(tb - 1)

        self._context = None
        self._updateContextWidget()

    def onClose(self):
        self._currentWeb.setUrl(QUrl('about:blank'))
        self._currentWeb = None
        for c in self._tabs.count():
            c.close()
        super().close()

    def onStartLoading(self):
        self.stopBtn.setEnabled(True)
        self._loadingBar.setProperty("value", 1)

    def onProgress(self, progress: int):
        self._loadingBar.setProperty("value", progress)

    def onLoadFinish(self, result):
        self.stopBtn.setDisabled(True)
        self._loadingBar.setProperty("value", 100)

    def _updateButtons(self):
        isLoading: bool = self._currentWeb and self._currentWeb.isLoading
        self.stopBtn.setEnabled(isLoading)
        self.forwardBtn.setEnabled(self._currentWeb and self._currentWeb.history().canGoForward())

    def _goToAddress(self):
        q = QUrl(self._itAddress.text())
        if q.scheme() == "":
            q.setScheme("http")

        self._currentWeb.load(q)
        self._currentWeb.show()

    def onPageChange(self, url):
        if url and url.toString().startswith('http'):
            self._itAddress.setText(url.toString())
        self.forwardBtn.setEnabled(self._currentWeb.history().canGoForward())

    def _onBack(self, *args):
        self._currentWeb.back()

    def _onForward(self, *args):
        self._currentWeb.forward()

    def _onReload(self, *args):
        self._currentWeb.reload()

    def _onStopPressed(self):
        self._currentWeb.stop()

    def welcome(self):
        self._web.setHtml(WELCOME_PAGE)
        self._itAddress.setText('about:blank')
        self.show()
        self.raise_()

    def _updateContextWidget(self):
        self.ctxWidget.setText(self._context)

    # ---------------------------------------------------------------------------------
    def createProvidersMenu(self, parentWidget):
        providerBtn = QAction(QtGui.QIcon(os.path.join(CWD, 'assets', 'gear-icon.png')), "Providers", parentWidget)
        providerBtn.setStatusTip("Search with Provider")
        providerBtn.triggered.connect(lambda: self.newProviderMenu())
        parentWidget.addAction(providerBtn)

        multiBtn = QAction(QtGui.QIcon(os.path.join(CWD, 'assets', 'multi-cogs.png')), "Providers in New tab", parentWidget)
        multiBtn.setStatusTip("Open providers in new tab")
        multiBtn.triggered.connect(lambda: self.newProviderMenu(True))
        parentWidget.addAction(multiBtn)

    def newProviderMenu(self, newTab=False):
        ctx = ProviderSelectionController()
        callBack = self.reOpenQueryNewTab if newTab else self.reOpenSameQuery
        ctx.showCustomMenu(self._itAddress, callBack)

    @exceptionHandler
    def reOpenSameQuery(self, website):
        self.open(website, self._context)

    @exceptionHandler
    def reOpenQueryNewTab(self, website):
        self.add_new_tab()
        self.open(website, self._context)

    # ------------------------------------ Menu ---------------------------------------

    def load(self, qUrl):
        self._web.load(qUrl)

    #   ----------------- getter / setter  -------------------

    def setFields(self, fList):
        self._menuDelegator._fields = fList

    def setSelectionHandler(self, value):
        Feedback.log('Set selectionHandler % s' % str(value))
        self._menuDelegator._selectionHandler = value

    def setInfoList(self, data: list):
        self._menuDelegator.infoList = tuple(data)
