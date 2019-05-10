# -*- coding: utf-8 -*-
# Handler for integration with Anki Note Fields config 

# This file is part of anki-markdown-formatter addon
# @author ricardo saturnino
# ------------------------------------------------

import re

from aqt.qt import *
from aqt.fields import FieldDialog
import anki

class NoteFieldControler:

    def __init__(self, converter):
        self._converter = converter

    def setup(self):
        FieldDialog.loadField = self._wrapLoadField(FieldDialog.loadField)
        FieldDialog.saveField = self._wrapSaveField(FieldDialog.saveField)
        FieldDialog.fillFields = self._wrapFillFields(FieldDialog.fillFields)


    def _wrapSaveField(self, fn):
        def saveField(dialog):
            idx = dialog.currentIdx

            fn(dialog)

            if not idx is None:
                fld = dialog.model['flds'][idx]
                fld['amd-enabled'] = 'y' if self.mdEnabled.isChecked() else 'n'

                # print('Field: %s' % fld['name'])
                # print(dialog.model['tmpls'])

                try:
                    fieldPattern = r"(\{\{((\w)+\:){0,2}%s\}\})" % fld['name']
                    for t in dialog.model['tmpls']:
                        self._processSaveTemplate(t, 'qfmt', fld['name'], fieldPattern, self.mdEnabled.isChecked())
                        self._processSaveTemplate(t, 'afmt', fld['name'], fieldPattern, self.mdEnabled.isChecked())
                except Exception as e:
                    print(e)
                    

        return saveField


    def _processSaveTemplate(self, template, tmpPart, fieldName, rgField, value):
        print('_3')
        
        text = template[tmpPart]
        result = self._converter.stripAmdTagForField(text, fieldName)

        if value:
            m = re.search(rgField, result)
            if not m:
                return

            result = result[:m.start()] + \
                    ("<amd>%s</amd>" % m.group(0)) + \
                    result[m.end():]

        print('result: ')
        print(result)
        template[tmpPart] = result

    
    def _wrapLoadField(self, fn):
        def loadField(dialog, idx):
            fn(dialog, idx)

            idx = dialog.currentIdx
            fld = dialog.model['flds'][idx]
            amdEnabled = (fld['amd-enabled'] == 'y') if 'amd-enabled' in fld else False

            self.mdEnabled.setChecked(amdEnabled)

        return loadField


    def _wrapFillFields(self, fn):
        def fillFields(dialog):
            res = fn(dialog)

            self.mdEnabled = QCheckBox("Enable Markdown Processing")

            container = dialog.form._2
            container.addWidget(self.mdEnabled, container.rowCount() + 1, 1)

            return res

            

        return fillFields
