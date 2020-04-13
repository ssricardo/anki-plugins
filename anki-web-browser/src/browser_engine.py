# -*- coding: utf-8 -*-

# --------------------------------------------------
# Handles Web engine itself
# --------------------------------------------------

import os

from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineContextMenuData, QWebEngineSettings, QWebEnginePage
from PyQt5.QtWidgets import *

from .core import Label, Feedback, CWD


# noinspection PyPep8Naming
class AwWebEngine(QWebEngineView):

    isLoading = False
    DARK_READER = None

    def __init__(self, parent=None):
        super().__init__(parent)
        AwWebEngine.initDarkReader()
        self.create()
        self.interceptor = WebRequestInterceptor()
        self.page().profile().setRequestInterceptor(self.interceptor)

    @classmethod
    def initDarkReader(clz):
        if not clz.DARK_READER:
            with open(os.path.join(CWD, 'resources', 'darkreader.js'), 'r') as ngJS:
                clz.DARK_READER = ngJS.read()
                Feedback.log('DarkReader loaded')


    def create(self):
        self.settings().globalSettings().setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        self.settings().globalSettings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().globalSettings().setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)

        self.page().loadStarted.connect(self.onStartLoading)
        self.page().loadFinished.connect(self.onLoadFinish)

        return self

# ======   Listeners ======

    def onStartLoading(self):
        self.isLoading = True

        # self.page().runJavaScript("""
        # var loadingCss = 'body { background: red; }',
        #     head = document.head || document.getElementsByTagName('head')[0],
        #     style = document.createElement('style');
        #
        #
        # head.appendChild(style);
        #
        # style.type = 'text/css';
        # style.id = 'loadingBack';
        # style.appendChild(document.createTextNode(loadingCss));
        # """)

    def onLoadFinish(self, result):
        self.isLoading = False
        if not result:
            Feedback.log('No result on loading page! ')

        self.page().runJavaScript(AwWebEngine.DARK_READER)
        # self.page().runJavaScript("document.getElementById('loadingBack').disabled = 'disabled';")
        self.page().runJavaScript("DarkReader.setFetchMethod(window.fetch);")

        self.page().runJavaScript("""
                DarkReader.enable({
                    brightness: 105,
                    contrast: 90,
                    sepia: 10
                });

                console.log('Dark reader come through');
            """)


class WebRequestInterceptor(QWebEngineUrlRequestInterceptor):

    def __init__(self, parent=None):
        super().__init__(parent)

    def interceptRequest(self, info):
        info.setHttpHeader(b'Access-Control-Allow-Origin', b'*')

