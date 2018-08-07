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
    _currentNote = None

    def __init__(self, ankiMw):
        NoteMenuHandler.setController(self)
        self._browser = browser.AwBrowser(ankiMw)

    def setupBindings(self):
        anki.hooks.addHook('EditorWebView.contextMenuEvent', NoteMenuHandler.onEditorMenu)
        anki.hooks.addHook('AnkiWebView.contextMenuEvent', NoteMenuHandler.onReviewerMenu)

    def openInBrowser(self, website, query, note, isEditMode = False):
        self._currentNote = note
        print(note.model()) # TODO check
        self._browser.open(website, query)

    def handleSelection(self, field, value, isUrl = false):
        print('Received something from Web Browser: [{}] {}'.format(isUrl, value))
