# -*- coding: utf-8 -*-
# Handles Configuration reading, saving and the integration with the config UI
# Contains model, service and view controller for Config
#
# This files is part of anki-web-browser addon
# @author ricardo saturnino
# -------------------------------------------------------

import config_view
from core import Feedback
import os
import json
import re
import shutil
from PyQt4 import QtGui, QtCore

currentLocation = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = 'config.json'

# ---------------------------------- Model ------------------------------

class ConfigHolder:

    def __init__(self, keepBrowserOpened = False, browserAlwaysOnTop = False, providers = [], **kargs):
        self.providers = [ConfigHolder.Provider(**p) for p in providers ] #providers
        self.keepBrowserOpened = keepBrowserOpened
        self.browserAlwaysOnTop = browserAlwaysOnTop

    def toDict(self):
        res = dict({
            'keepBrowserOpened': self.keepBrowserOpened,
            'browserAlwaysOnTop': self.browserAlwaysOnTop,
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
    _validURL = re.compile('^((http|ftp){1}s{0,1}://)([\w._/?&=%#@]|-)+{}([\w._/?&=%#]|-)*$')

    def getConfig(self):
        if not self._config:
            return self.load()
        return self._config        


    def load(self, createIfNotExists = True):
        print('[INFO] Trying to read config file in {}'.format(currentLocation + '/' + CONFIG_FILE))
        try:
            with open(currentLocation + '/' + CONFIG_FILE) as f:
                obj = json.load(f)
                conf = ConfigHolder(**obj)
        except:
            conf = False        

        if not conf and createIfNotExists:
            conf = self._createConfiguration()
        self._config = conf
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
            raise e # TODO handle
        finally:
            if bkpName:
                os.remove(bkpName)


    def _createConfiguration(self):
        """
            Creates a new default configuration file. 
            A simple JSON from a dictionary. Should be called only if the file doesn't exist yet
        """

        print('[INFO] Creating a new config file in {}'.format(currentLocation + '/' + CONFIG_FILE))

        conf = ConfigHolder()    
        conf.keepBrowserOpened = True
        conf.browserAlwaysOnTop = False

        # default providers
        conf.providers = [
            ConfigHolder.Provider('Google Web', 'https://google.com/search?q={}'), 
            ConfigHolder.Provider('Google Images', 'https://www.google.com/search?tbm=isch&q={}'),
            ConfigHolder.Provider('Your Sentence', 'http://sentence.yourdictionary.com/{}?direct_search_result=yes'),
            ConfigHolder.Provider('Pixabay', 'https://pixabay.com/en/photos/?q={}&image_type=all')]

        self.__writeToFile(conf)
        return conf


    def save(self, config):
        """
            Save a given configuration
        """
        
        if not config:
            return
        self.validate(config)
        print('[INFO] Saving config file in {}'.format(currentLocation + '/' + CONFIG_FILE))
        self.__writeToFile(config)
        self._config = config


    def validate(self, config):
        """
            Checks the configuration before saving it. 
            Checks types and the URL from the providers
        """

        checkedTypes = [(config, ConfigHolder), (config.keepBrowserOpened, bool), (config.browserAlwaysOnTop, bool), (config.providers, list)]
        for current, expected in checkedTypes:
            if not isinstance(current, expected):
                raise ValueError('{} should be {}'.format(current, expected))
        
        for name, url in map(lambda item: (item.name, item.url), config.providers):
            print(name, url)
            if not name or not url:
                raise ValueError('There is an illegal value for one provider (%s %s)' % (name, url))
            if not self._validURL.match(url):
                raise ValueError('The provider URL needs {} that will be replaced by the selected text. Check the URL %s' % url)

        

# ------------------------------ View Controller --------------------------

class ConfigController:
    """
        Manages the view interface for configurations
    """

    _ui = None
    _dialog = None
    _hasSelection = False
    _pendingChanges = False
    _tempCfg = None

    def __init__(self, myParent):
        self._tempCfg = service.getConfig()
        self._dialog = QtGui.QDialog(parent=myParent)
        self._ui = config_view.Ui_ConfigView()
        self._ui.setupUi(self._dialog)
        self.setupBinds()


    def setupBinds(self):
        'Sets the relations between the UI actions and handler functions'

        self._ui.btSave.clicked.connect(lambda: self.onSaveClick())
        self._ui.btCancel.clicked.connect(lambda: self.onCancelClick())

        self._ui.btAdd.clicked.connect(lambda: self.onAddClick())
        self._ui.btRemove.clicked.connect(lambda: self.onRemoveClick())
        self._ui.tbProviders.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self._ui.tbProviders.horizontalHeader().setStretchLastSection(True)


    def open(self):
        'Opens the Config window'

        self._tempCfg = service.getConfig()
        self._ui.rbKeepOpened.setChecked(bool(self._tempCfg.keepBrowserOpened))
        self._ui.rbOnTop.setChecked(bool(self._tempCfg.browserAlwaysOnTop))
        self.setupDataTable()
        self._dialog.show()


    def setupDataTable(self):
        'Prepares the data table and loads the providers from the config'

        data = self._tempCfg.providers
        tb = self._ui.tbProviders
        tb.setColumnCount(2)
        tb.setRowCount(len(data))

        for index, item in enumerate(data):
            tb.setItem(index, 0, QtGui.QTableWidgetItem(item.name))
            tb.setItem(index, 1, QtGui.QTableWidgetItem(item.url))
        

    # ----------------------------------- View handles -------------------------------

    def onAddClick(self):
        'Handles Add button on view'

        tb = self._ui.tbProviders
        tb.insertRow(tb.rowCount())
        newUrl = QtGui.QTableWidgetItem('http://something/{}')
        tb.setItem(tb.rowCount() - 1, 0, QtGui.QTableWidgetItem('My New Provider'))
        tb.setItem(tb.rowCount() - 1, 1, newUrl)
        tb.clearSelection()
        tb.setItemSelected(newUrl, True)

    def onRemoveClick(self):
        'Handles Remove button on view'

        tab = self._ui.tbProviders

        if not tab.selectedIndexes():
            print('Nothing selected. Ignore remove click...')
            return

        rowIndex = tab.selectedIndexes()[0].row()
        tab.removeRow(rowIndex)


    def onCancelClick(self):
        self._tempCfg = None
        self._dialog.close()


    def onSaveClick(self):
        print('onSaveClick')
        _tempCfg = ConfigHolder()
        _tempCfg.browserAlwaysOnTop = self._ui.rbOnTop.isChecked()
        _tempCfg.keepBrowserOpened = self._ui.rbKeepOpened.isChecked()

        tab = self._ui.tbProviders
        _tempCfg.providers = [None] * tab.rowCount()

        for index in range(tab.rowCount()):
            _tempCfg.providers[index] = ConfigHolder.Provider(tab.item(index, 0).text(), tab.item(index, 1).text())

        service.save(_tempCfg)
        self.onCancelClick()

    def onSelectItem(self):
        self._hasSelection = True
        self._ui.btRemove.setEnabled(True)

    def onUnSelectItem(self):
        self._hasSelection = False
        self._ui.btRemove.setEnabled(False)
    
    def onChangeItem(self):
        self._pendingChanges = True

# -----------------------------------------------------------------------------
# global instances

service = ConfigService()