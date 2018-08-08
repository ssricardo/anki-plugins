# Main interface between Anki and this addon components

# Holds references so GC does kill them
controllerInstance = None


def run(providers = {}):
    global controllerInstance
    import const
    from notemenu import NoteMenuHandler
    import browser
    import anki
    from aqt import mw

    NoteMenuHandler.options(providers)
    controllerInstance = Controller(mw)
    controllerInstance.setupBindings()

    

class Controller:
    """
        The mediator/adapter between Anki with its components and this addon specific API
    """

    _browser = None
    _editorReference = None
    _currentNote = None
    _ankiMw = None    

    def __init__(self, ankiMw):
        NoteMenuHandler.setController(self)
        self._browser = browser.AwBrowser(ankiMw)
        self._ankiMw = ankiMw

    def setupBindings(self):
        # anki.hooks.addHook('afterStateChange', self.setState)
        anki.hooks.addHook('EditorWebView.contextMenuEvent', self.onEditorHandle)
        anki.hooks.addHook('AnkiWebView.contextMenuEvent', self.onReviewerHandle)

    def isEditing(self):
        'Checks anki current state. Whether is editing or not'

        return self._ankiMw and self._ankiMw.state == 'resetRequired' and self._editorReference

    def onEditorHandle(self, webView, menu):
        """
            Wrapper to the real context menu handler on the editor;
            Also holds a reference to the editor
        """

        self._editorReference = webView.editor
        NoteMenuHandler.onEditorMenu(webView, menu)        

    def onReviewerHandle(self, webView, menu):
        """
            Wrapper to the real context menu handler on the reviewer;
            Cleans up editor reference
        """

        self._editorReference = None
        NoteMenuHandler.onReviewerMenu(webView, menu)

    def openInBrowser(self, website, query, note, isEditMode = False):
        """
            Setup enviroment for web browser and invoke it
        """

        self._currentNote = note
        
        if self.isEditing():
            fieldList = note.model()['flds']
            fieldsNames = [{ind, val} for ind, val in enumerate(map(lambda i: i['name'], fieldList))] 
            self._browser.setFields(fieldsNames)
        else:
            self._browser.setFields(None)   # clear fields

        self._browser.open(website, query)

    def handleSelection(self, fieldIndex, value, isUrl = False):
        """
            Callback from the web browser. 
            Invoked when there is a selection coming from the browser. It need to be delivered to a given field
        """

        print('Received something from Web Browser: [{}] {}'.format(isUrl, value))
        newValue = self._currentNote.items()[fieldIndex] + '\n' + value
        self._currentNote.items()[fieldIndex] = newValue
        print(self._currentNote.items()[fieldIndex]) 

        #self.web.eval("setFields(%s); " % ('{1: "Teste2"}'))
