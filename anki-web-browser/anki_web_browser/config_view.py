# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config_view.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ConfigView(object):
    def setupUi(self, ConfigView):
        ConfigView.setObjectName(_fromUtf8("ConfigView"))
        ConfigView.resize(450, 380)
        ConfigView.setFixedSize(450, 380)       # modif
        
        self.verticalLayoutWidget = QtGui.QWidget(ConfigView)
        # self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 400, 292))
        self.verticalLayoutWidget.setGeometry(ConfigView.geometry())

        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(10)        # modif
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lbProviders = QtGui.QLabel(self.verticalLayoutWidget)
        self.lbProviders.setObjectName(_fromUtf8("lbProviders"))
        self.verticalLayout.addWidget(self.lbProviders)
        self.tbProviders = QtGui.QTableWidget() # self.verticalLayoutWidget
        self.tbProviders.setObjectName(_fromUtf8("tbProviders"))
        self.verticalLayout.addWidget(self.tbProviders)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(200, -1, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btRemove = QtGui.QPushButton(self.getIcon(QtGui.QStyle.SP_TrashIcon), '', self.verticalLayoutWidget)
        self.btRemove.setObjectName(_fromUtf8("btRemove"))
        self.horizontalLayout.addWidget(self.btRemove)
        self.btAdd = QtGui.QPushButton(self.getIcon(QtGui.QStyle.SP_DirLinkIcon), '', self.verticalLayoutWidget)
        self.btAdd.setObjectName(_fromUtf8("btAdd"))
        self.horizontalLayout.addWidget(self.btAdd)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.rbKeepOpened = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.rbKeepOpened.setObjectName(_fromUtf8("rbKeepOpened"))
        self.verticalLayout.addWidget(self.rbKeepOpened)
        self.rbOnTop = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.rbOnTop.setObjectName(_fromUtf8("rbOnTop"))
        self.verticalLayout.addWidget(self.rbOnTop)

        # modif
        self.btActionsBox = QtGui.QHBoxLayout()
        # self.btActionsBox.setContentsMargins(10, 100, 0, -1)
        # self.btActions = QtGui.QDialogButtonBox(ConfigView)
        # self.btActions.setGeometry(QtCore.QRect(30, 300, 340, 32))
        # self.btActions.setOrientation(QtCore.Qt.Horizontal)
        self.btSave = QtGui.QPushButton(self.getIcon(QtGui.QStyle.SP_DialogApplyButton),'Save', self.verticalLayoutWidget)
        self.btCancel = QtGui.QPushButton(self.getIcon(QtGui.QStyle.SP_DialogCancelButton), 'Cancel', self.verticalLayoutWidget)
        self.btActionsBox.addWidget(self.btSave)
        self.btActionsBox.addWidget(self.btCancel)
        self.verticalLayout.addWidget(QtGui.QSplitter())
        self.verticalLayout.addLayout(self.btActionsBox)

        self.tbProviders.verticalHeader().setVisible(False)
        self.tbProviders.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tbProviders.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        # self.tbProviders.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)        # FIXME
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
        return QIcon(QtGui.QApplication.style().standardIcon(qtStyle))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ConfigView = QtGui.QDialog()
    ui = Ui_ConfigView()
    ui.setupUi(ConfigView)
    ConfigView.show()
    sys.exit(app.exec_())

