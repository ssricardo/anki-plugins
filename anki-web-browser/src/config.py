# -*- coding: utf-8 -*-
# Handles Configuration reading, saving and the integration with the config UI
# Contains model, service and view controller for Config
#
# This files is part of anki-web-browser addon
# @author ricardo saturnino
# -------------------------------------------------------

from .config_view import Ui_ConfigView
from .core import Feedback

import os
import json
import re
import shutil
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.Qt import QIcon

currentLocation = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = 'config.json'

# ---------------------------------- Model ------------------------------

class ConfigHolder:
    SHORTCUT = 'Ctrl+Shift+B'
    RP_SHORT = 'F10'

    def __init__(self, keepBrowserOpened = True, browserAlwaysOnTop = False, menuShortcut = SHORTCUT, \
            providers = [], repeatShortcut = RP_SHORT, useSystemBrowser = False, **kargs):
        self.providers = [ConfigHolder.Provider(**p) for p in providers ] #providers
        self.keepBrowserOpened = keepBrowserOpened
        self.browserAlwaysOnTop = browserAlwaysOnTop
        self.useSystemBrowser = useSystemBrowser
        self.menuShortcut = menuShortcut
        self.repeatShortcut = repeatShortcut

    def toDict(self):
        res = dict({
            'keepBrowserOpened': self.keepBrowserOpened,
            'browserAlwaysOnTop': self.browserAlwaysOnTop,
            'useSystemBrowser': self.useSystemBrowser,
            'menuShortcut': self.menuShortcut,
            'repeatShortcut': self.repeatShortcut, 
            'providers': [p for p in  map(lambda p: p.__dict__, self.providers)]
        })
        return res

    class Provider:

        def __init__(self, name, url, **kargs):
            self.name = name
            self.url = url


# ------------------------------ Service class --------------------------
class ConfigService:
    """
        Responsible for reading and storing configurations
    """
    _config = None
    _validURL = re.compile('^((http|ftp){1}s{0,1}://)([\w._/?&=%#@]|-)+{}([\w._/?&=%#+]|-)*$')
    _firstTime = None

    def getConfig(self):
        if not self._config:
            return self.load()
        return self._config        


    def load(self, createIfNotExists = True):
        Feedback.log('[INFO] Trying to read config file in {}'.format(currentLocation + '/' + CONFIG_FILE))
        try:
            conf = self._readFileToObj()
        except:
            conf = False        

        if not conf and createIfNotExists:
            conf = self._createConfiguration()
        self._config = conf
        return conf

    def _readFileToObj(self):
        with open(currentLocation + '/' + CONFIG_FILE) as f:
            obj = json.load(f)
            Feedback.log(obj)
            conf = ConfigHolder(**obj)

        return conf


    def __writeToFile(self, config):
        'Handles file writing...'

        bkpName = None  #
        try:
            if os.path.exists(currentLocation + '/' + CONFIG_FILE):
                bkpName = shutil.copyfile(currentLocation + '/' + CONFIG_FILE, currentLocation + '/.bkp_' + CONFIG_FILE)
            with(open(currentLocation + '/' + CONFIG_FILE, 'w')) as cfgFile:
                json.dump(config.toDict(), cfgFile)
        except Exception as e:
            if bkpName:
                shutil.copyfile(bkpName, currentLocation + '/' + CONFIG_FILE) # restore
            Feedback.showError(e)
        finally:
            if bkpName:
                os.remove(bkpName)


    def _createConfiguration(self):
        """
            Creates a new default configuration file. 
            A simple JSON from a dictionary. Should be called only if the file doesn't exist yet
        """

        Feedback.log('[INFO] Creating a new config file in {}'.format(currentLocation + '/' + CONFIG_FILE))

        conf = ConfigHolder()

        # default providers
        conf.providers = [
            ConfigHolder.Provider('Google Web', 'https://google.com/search?q={}'), 
            ConfigHolder.Provider('Google Translate', 'https://translate.google.com/#view=home&op=translate&sl=auto&tl=en&text={}'),
            ConfigHolder.Provider('Google Images', 'https://www.google.com/search?tbm=isch&q={}'),
            ConfigHolder.Provider('Forvo', 'https://forvo.com/search/{}/'),
            ConfigHolder.Provider('Pixabay', 'https://pixabay.com/en/photos/?q={}&image_type=all')]

        self.__writeToFile(conf)
        self._firstTime = True
        return conf


    def save(self, config):
        """
            Save a given configuration
        """

        if not config:
            return

        try:
            self.validate(config)
        except ValueError as ve:
            Feedback.showInfo(ve)
            return False
        
        Feedback.log('[INFO] Saving config file in {}'.format(currentLocation + '/' + CONFIG_FILE))
        self.__writeToFile(config)
        self._config = config
        Feedback.showInfo('Anki-Web-Browser configuration saved')
        return True


    def validate(self, config):
        """
            Checks the configuration before saving it. 
            Checks types and the URL from the providers
        """

        checkedTypes = [(config, ConfigHolder), (config.keepBrowserOpened, bool), (config.browserAlwaysOnTop, bool), (config.useSystemBrowser, bool), (config.providers, list)]
        for current, expected in checkedTypes:
            if not isinstance(current, expected):
                raise ValueError('{} should be {}'.format(current, expected))
        
        for name, url in map(lambda item: (item.name, item.url), config.providers):
            if not name or not url:
                raise ValueError('There is an illegal value for one provider (%s %s)' % (name, url))
            if not self._validURL.match(url):
                raise ValueError('Some URL is invalid. Check the URL and if it contains {} that will be replaced by the text: %s' % url)

    
    def sortProviders(self, config: ConfigHolder):
        """
            Re sorts providers based on its name
        """

        config.providers.sort(key=lambda i: i.name)

    
# ------------------------------ View Controller --------------------------

class ConfigController:
    """
        Manages the view interface for configurations
    """

    _ui = None
    _hasSelection = False
    _pendingChanges = False
    _tempCfg = None

    def __init__(self, myParent):
        self._tempCfg = service.getConfig()
        self._ui = ConfigViewAdapter(myParent)
        self.setupBinds()
        self.setupInitialState()


    def setupBinds(self):
        'Sets the relations between the UI actions and handler functions'

        self._ui.btSave.clicked.connect(lambda: self.onSaveClick())
        self._ui.btCancel.clicked.connect(lambda: self.onCancelClick())

        self._ui.btAdd.clicked.connect(lambda: self.onAddClick())
        self._ui.btRemove.clicked.connect(lambda: self.onRemoveClick())
        self._ui.btSortProvider.clicked.connect(lambda: self.onSortProviders())
        self._ui.tbProviders.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self._ui.cbSystemBrowser.stateChanged.connect(lambda: self.onUsedBrowserChange())

    def setupInitialState(self):
        self.onUsedBrowserChange()        

    def onUsedBrowserChange(self):
        useSystemBrowser = self._ui.cbSystemBrowser.isChecked()
        self._ui.browserInfo.setVisible(useSystemBrowser)
        self._ui.rbKeepOpened.setEnabled(not useSystemBrowser)
        self._ui.rbOnTop.setEnabled(not useSystemBrowser)
        

    def open(self):
        'Opens the Config window'

        self._tempCfg = service.getConfig()
        self._ui.rbKeepOpened.setChecked(bool(self._tempCfg.keepBrowserOpened))
        self._ui.rbOnTop.setChecked(bool(self._tempCfg.browserAlwaysOnTop))
        self._ui.cbSystemBrowser.setChecked(bool(self._tempCfg.useSystemBrowser))
        self._ui.teShortcutMenu.setText(self._tempCfg.menuShortcut)
        self._ui.teShortcutRepeat.setText(self._tempCfg.repeatShortcut)
        self.setupDataTable()
        self._ui.window.show()


    def setupDataTable(self):
        'Prepares the data table and loads the providers from the config'

        data = self._tempCfg.providers
        tb = self._ui.tbProviders
        tb.setColumnCount(2)
        tb.setRowCount(len(data))

        for index, item in enumerate(data):
            tb.setItem(index, 0, QtWidgets.QTableWidgetItem(item.name))
            tb.setItem(index, 1, QtWidgets.QTableWidgetItem(item.url))
        

    # ----------------------------------- View handles -------------------------------

    def onAddClick(self):
        'Handles Add button on view'

        tb = self._ui.tbProviders
        tb.insertRow(tb.rowCount())
        newUrl = QtWidgets.QTableWidgetItem('http://something/{}')
        tb.setItem(tb.rowCount() - 1, 0, QtWidgets.QTableWidgetItem('My New Provider'))
        tb.setItem(tb.rowCount() - 1, 1, newUrl)
        tb.clearSelection()
        newUrl.setSelected(True)

    def onRemoveClick(self):
        'Handles Remove button on view'

        tab = self._ui.tbProviders

        if not tab.selectedIndexes():
            Feedback.showInfo('Please select the item to be removed')
            return

        rowIndex = tab.selectedIndexes()[0].row()
        tab.removeRow(rowIndex)


    def onCancelClick(self):
        self._tempCfg = None
        self._ui.window.close()


    def onSaveClick(self):
        _tempCfg = ConfigHolder()
        _tempCfg.browserAlwaysOnTop = self._ui.rbOnTop.isChecked()
        _tempCfg.keepBrowserOpened = self._ui.rbKeepOpened.isChecked()
        _tempCfg.useSystemBrowser = self._ui.cbSystemBrowser.isChecked()
        _tempCfg.menuShortcut = self._ui.teShortcutMenu.text().strip()
        _tempCfg.repeatShortcut = self._ui.teShortcutRepeat.text().strip()

        tab = self._ui.tbProviders
        _tempCfg.providers = [None] * tab.rowCount()

        for index in range(tab.rowCount()):
            _tempCfg.providers[index] = ConfigHolder.Provider(tab.item(index, 0).text(), tab.item(index, 1).text())

        res = service.save(_tempCfg)
        if res:
            self.onCancelClick()

    def onSelectItem(self):
        self._hasSelection = True
        self._ui.btRemove.setEnabled(True)

    def onUnSelectItem(self):
        self._hasSelection = False
        self._ui.btRemove.setEnabled(False)
    
    def onChangeItem(self):
        self._pendingChanges = True

    def onSortProviders(self):
        self._ui.tbProviders.clearSelection()
        service.sortProviders(self._tempCfg)
        self.setupDataTable()

# ----------------------------------------------------------------------------
# Adjust on View

class ConfigViewAdapter(Ui_ConfigView):

    def __init__(self, myParent):
        self.window = QtWidgets.QDialog(parent=myParent)
        # self._ui = ConfigView(myParent)
        self.setupUi(self.window)

        self.verticalLayWidget.setFixedSize(480, 432)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)

        self.browserInfo.setVisible(self.cbSystemBrowser.isChecked()) #keep

        self.btRemove.setIcon(self.getIcon(QtWidgets.QStyle.SP_TrashIcon)) 
        self.btAdd.setIcon(self.getIcon(QtWidgets.QStyle.SP_DirLinkIcon))
        self.btSave.setIcon(self.getIcon(QtWidgets.QStyle.SP_DialogApplyButton))
        self.btCancel.setIcon(self.getIcon(QtWidgets.QStyle.SP_DialogCancelButton))
        self.btSortProvider.setIcon(self.getIcon(QtWidgets.QStyle.SP_ArrowDown))

    def getIcon(self, qtStyle):
        return QIcon(QtWidgets.QApplication.style().standardIcon(qtStyle))



# -----------------------------------------------------------------------------
# global instances

service = ConfigService()