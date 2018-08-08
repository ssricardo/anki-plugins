# Initial version

providers = {
    'Google Web': 'https://google.com/search?q={}',
    'Google Images': 'https://www.google.com/search?tbm=isch&q={}',
}

import anki_web_browser.controller as ctr

ctr.run(providers)

if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication, QMenu, QAction
    from PyQt4.QtCore import QUrl
    from PyQt4.QtWebKit import QWebView

    class RssBrowser(QWebView):

        ctxMenu = None

        def __init__(self):
            QWebView.__init__(self)
            self.loadFinished.connect(self._result_available)
            # self.setGeometry(800, 200, 400, 200)

            m = QMenu(self)
            a1 = QAction('Add selection to ', m, 
                    triggered=lambda: self._updFieldFromSelection('test', None))
            a2 = QAction('Examples', m, 
                    triggered=lambda: self._updFieldFromSelection('test', None))
            m.addAction(a1)
            m.addAction(a2)

            self.ctxMenu = m

        def _updFieldFromSelection(self, field, value):
            pass

        def _result_available(self, ok):
            frame = self.page().mainFrame()

        def contextMenuEvent(self, evt):
            print(self.selectedText())

            hit = self.page().currentFrame().hitTestContent(evt.pos())
            # print(dir(hit))
            print('Text: ', hit.linkText())
            print(hit.isContentSelected())
            print(hit.linkUrl())

            action = self.ctxMenu.exec_(self.mapToGlobal(evt.pos()))

        def handleSelectionChanged(self):
            cursor = self.edit.textCursor()
            print ("Selection start: %d end: %d" % 
            (cursor.selectionStart(), cursor.selectionEnd()))

        def newSelection(self): 
            print(self.selectedText)

    app = QApplication(sys.argv)
    view = RssBrowser()
    view.load(QUrl('https://images.google.com/'))
    view.show()
    sys.exit(app.exec_())