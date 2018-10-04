# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config_view.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_ConfigView(object):
    def setupUi(self, ConfigView):
        ConfigView.setObjectName(_fromUtf8("ConfigView"))
        ConfigView.resize(460, 400)
        ConfigView.setFixedSize(460, 400)       # modif
        
        self.verticalLayoutWidget = QtWidgets.QWidget(ConfigView)
        # self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 400, 292))
        self.verticalLayoutWidget.setGeometry(ConfigView.geometry())

        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)        # modif
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lbProviders = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbProviders.setObjectName(_fromUtf8("lbProviders"))
        self.verticalLayout.addWidget(self.lbProviders)
        self.tbProviders = QtWidgets.QTableWidget() # self.verticalLayoutWidget
        self.tbProviders.setObjectName(_fromUtf8("tbProviders"))
        self.verticalLayout.addWidget(self.tbProviders)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(200, -1, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btRemove = QtWidgets.QPushButton(self.getIcon(QtWidgets.QStyle.SP_TrashIcon), '', self.verticalLayoutWidget)
        self.btRemove.setObjectName(_fromUtf8("btRemove"))
        self.horizontalLayout.addWidget(self.btRemove)
        self.btAdd = QtWidgets.QPushButton(self.getIcon(QtWidgets.QStyle.SP_DirLinkIcon), '', self.verticalLayoutWidget)
        self.btAdd.setObjectName(_fromUtf8("btAdd"))
        self.horizontalLayout.addWidget(self.btAdd)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.rbKeepOpened = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.rbKeepOpened.setObjectName(_fromUtf8("rbKeepOpened"))
        self.verticalLayout.addWidget(self.rbKeepOpened)
        self.rbOnTop = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.rbOnTop.setObjectName(_fromUtf8("rbOnTop"))
        self.verticalLayout.addWidget(self.rbOnTop)

        # modif
        self.btActionsBox = QtWidgets.QHBoxLayout()
        # self.btActionsBox.setContentsMargins(10, 100, 0, -1)
        # self.btActions = QtGui.QDialogButtonBox(ConfigView)
        # self.btActions.setGeometry(QtCore.QRect(30, 300, 340, 32))
        # self.btActions.setOrientation(QtCore.Qt.Horizontal)
        bottomInfo = QtWidgets.QLabel('It may be necessary to restart Anki to apply the changes', 
        self.verticalLayoutWidget)
        bottomInfo.setStyleSheet('QLabel  {color: #960c19}')
        self.verticalLayout.addWidget(bottomInfo)

        self.btSave = QtWidgets.QPushButton(self.getIcon(QtWidgets.QStyle.SP_DialogApplyButton),'Save', self.verticalLayoutWidget)
        self.btCancel = QtWidgets.QPushButton(self.getIcon(QtWidgets.QStyle.SP_DialogCancelButton), 'Cancel', self.verticalLayoutWidget)
        self.btActionsBox.addWidget(self.btSave)
        self.btActionsBox.addWidget(self.btCancel)
        # self.verticalLayout.addWidget(QtGui.QSplitter())
        self.verticalLayout.addLayout(self.btActionsBox)

        self.tbProviders.verticalHeader().setVisible(False)
        self.tbProviders.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbProviders.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tbProviders.setColumnCount(2)
        self.tbProviders.setHorizontalHeaderLabels(('Name', 'URL'))

        # self.btActions.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        # self.btActions.setObjectName(_fromUtf8("btActions"))

        self.retranslateUi(ConfigView)
        # QtCore.QObject.connect(self.btActions, QtCore.SIGNAL(_fromUtf8("accepted()")), ConfigView.accept)
        # QtCore.QObject.connect(self.btActions, QtCore.SIGNAL(_fromUtf8("rejected()")), ConfigView.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigView)

    def retranslateUi(self, ConfigView):
        ConfigView.setWindowTitle(_translate("ConfigView", "Web Browser Config", None))
        self.lbProviders.setText(_translate("ConfigView", "Providers", None))
        self.btRemove.setText(_translate("ConfigView", "Remove", None))
        self.btAdd.setText(_translate("ConfigView", "Add", None))
        self.rbKeepOpened.setText(_translate("ConfigView", "Keep browser opened (after current card is changed)", None))
        self.rbOnTop.setText(_translate("ConfigView", "Keep always visible (on top)", None))

    def getIcon(self, qtStyle):
        return QIcon(QtWidgets.QApplication.style().standardIcon(qtStyle))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConfigView = QtWidgets.QDialog()
    ui = Ui_ConfigView()
    ui.setupUi(ConfigView)
    ConfigView.show()
    sys.exit(app.exec_())

