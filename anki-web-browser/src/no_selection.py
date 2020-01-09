# -*- coding: utf-8 -*-

# Handles operation when no text is selected. 
# Decorates View, making changes without affect generated file.
# ---------------------------------------
from .no_selection_view import Ui_Dialog
from .core import Feedback

import os
import json
import re
import shutil
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox, QAction
from PyQt5.Qt import QIcon

class NoSelectionResult:
    SELECTION_NEEDED = -1
    NO_RESULT = 0
    USE_QUERY = 1
    USE_FIELD = 2

    resultType = None
    value = None

    def __init__(self, rType, rValue):
        self.resultType = rType
        self.value = rValue


class NoSelectionController:
    _ui = None
    _callback = None

    def __init__(self, parent):
        self._ui = NoSelectionViewAdapter(parent)
        self._ui.window.finished.connect(self.onClose)


    def setFields(self, fields):
        cb = self._ui.cbField
        cb.clear()
        for index, f in fields.items():
            cb.addItem(f, index)

    def handle(self, callback):
        self._callback = callback
        self.open()

    def open(self):
        self._ui.window.open()

    def isRepeatOption(self):
        return self._ui.cbMemorize.isChecked() and self.getValue().resultType != NoSelectionResult.NO_RESULT

    def getValue(self):
        d = self._ui
        if d.rbUseTerm.isChecked():
            return  NoSelectionResult(NoSelectionResult.USE_QUERY, d.teTerm.text())
        elif d.rbUseField.isChecked():
            return NoSelectionResult(NoSelectionResult.USE_FIELD, d.cbField.itemData(d.cbField.currentIndex()))
        elif d.rbUseNone.isChecked():
            return NoSelectionResult(NoSelectionResult.SELECTION_NEEDED, None)

        return NoSelectionResult(NoSelectionResult.NO_RESULT, None)

    
    def onClose(self, result):
        if result == QDialog.Accepted:
            result = self.getValue()
            if not result or result.resultType == NoSelectionResult.NO_RESULT \
                    or result.resultType == NoSelectionResult.SELECTION_NEEDED:
                Feedback.log('No value from NoSelection')
                Feedback.showInfo('No value selected')
                return
            self._callback(result)
        else:
            Feedback.log('NoSelection canceled')


class NoSelectionViewAdapter(Ui_Dialog):

    def __init__(self, myParent):
        self.window = QtWidgets.QDialog(parent=myParent)
        self.setupUi(self.window)

        self.rbUseField.clicked.connect(self.selectionChanged)
        self.rbUseTerm.clicked.connect(self.selectionChanged)
        self.rbUseNone.clicked.connect(self.selectionChanged)

        self.originalAccept = self.window.accept
        self.originalCancel = self.window.reject
        self.window.accept = self.onAccept
        self.window.reject = self.onCancel
        self.rbUseTerm.setChecked(True)
        self.selectionChanged()       

    def selectionChanged(self):
        if self.rbUseTerm.isChecked():
            self.cbMemorize.setChecked(False)
            self.cbMemorize.setDisabled(True)
            self.teTerm.setDisabled(False)
        else:
            self.cbMemorize.setDisabled(False)
            self.teTerm.setText('')
            self.teTerm.setDisabled(True)

    def onAccept(self):
        if self.rbUseTerm.isChecked():
            if not self.teTerm.text():
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Please fill in some term")
                msg.setWindowTitle("Invalid value")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.open()
                self.currentMsg = msg
                return
        return self.originalAccept()

    def onCancel(self):
        self.rbUseField.setChecked(False)
        self.rbUseTerm.setChecked(False)
        self.rbUseNone.setChecked(False)
        return self.originalCancel()

    def result(self):
        return self._ui.window.result

    def getIcon(self, qtStyle):
        return QIcon(QtWidgets.QApplication.style().standardIcon(qtStyle))
