# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\anki-web-browser\src\no_selection_view.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(320, 255)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 220, 301, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.teTerm = QtWidgets.QLineEdit(Dialog)
        self.teTerm.setGeometry(QtCore.QRect(60, 50, 231, 21))
        self.teTerm.setObjectName("teTerm")
        self.rbUseTerm = QtWidgets.QRadioButton(Dialog)
        self.rbUseTerm.setGeometry(QtCore.QRect(40, 30, 141, 17))
        self.rbUseTerm.setObjectName("rbUseTerm")
        self.rbUseField = QtWidgets.QRadioButton(Dialog)
        self.rbUseField.setGeometry(QtCore.QRect(40, 84, 251, 17))
        self.rbUseField.setObjectName("rbUseField")
        self.cbField = QtWidgets.QComboBox(Dialog)
        self.cbField.setGeometry(QtCore.QRect(62, 107, 231, 22))
        self.cbField.setObjectName("cbField")
        self.rbUseNone = QtWidgets.QRadioButton(Dialog)
        self.rbUseNone.setGeometry(QtCore.QRect(40, 140, 241, 17))
        self.rbUseNone.setObjectName("rbUseNone")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(10, 160, 301, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.cbMemorize = QtWidgets.QCheckBox(Dialog)
        self.cbMemorize.setGeometry(QtCore.QRect(40, 180, 231, 20))
        self.cbMemorize.setObjectName("cbMemorize")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 301, 211))
        self.groupBox.setObjectName("groupBox")
        self.groupBox.raise_()
        self.buttonBox.raise_()
        self.teTerm.raise_()
        self.rbUseTerm.raise_()
        self.rbUseField.raise_()
        self.cbField.raise_()
        self.rbUseNone.raise_()
        self.line_2.raise_()
        self.cbMemorize.raise_()

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Anki Web Browser - No Selection"))
        self.rbUseTerm.setText(_translate("Dialog", "Search term(s):"))
        self.rbUseField.setText(_translate("Dialog", "Use content of field:"))
        self.rbUseNone.setText(_translate("Dialog", "Require text selection"))
        self.cbMemorize.setText(_translate("Dialog", "Memorize option on this session"))
        self.groupBox.setTitle(_translate("Dialog", "Select the source for querying:"))


