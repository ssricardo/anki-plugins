
from .converter import Converter
from .core import AppHolder

class BatchService:

    def __init__(self, converter: Converter):
        self._converter = converter

    def convertNotesToMD(self, noteList: list):
        mw = AppHolder.app
        mw.checkpoint("convertNotesToMD")
        mw.progress.start()
        for nid in noteList:
            note = mw.col.getNote(nid)
            note.fields = self._processFields(note.fields, self._converter.getTextFromHtml)
            note.flush()
        mw.progress.finish()
        mw.reset()


    def convertNotesToHTML(self, noteList: list):
        mw = AppHolder.app
        mw.checkpoint("convertNotesToHTML")
        mw.progress.start()
        for nid in noteList:
            note = mw.col.getNote(nid)
            note.fields = self._processFields(note.fields, self._converter.convertMarkdown)
            note.flush()
        mw.progress.finish()
        mw.reset()

    
    def _processFields(self, fieldList:list, converterFn):
        processedFields = []

        for field in fieldList:
            processedFields.append( converterFn(field) )

        return processedFields