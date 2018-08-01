# Main interface between Anki and this addon components

def run(providers = {}):
    import const
    from notemenu import NoteMenuHandler
    from browser import AwBrowser

    NoteMenuHandler.options(providers)

    import anki

    anki.hooks.addHook('EditorWebView.contextMenuEvent', NoteMenuHandler.onEditorMenu)
    anki.hooks.addHook('AnkiWebView.contextMenuEvent', NoteMenuHandler.onReviewerMenu)