# Contains a few classes that mocks anki one
# Only for testing



# def mw(self):
#     reviewer = TReviewer()


class TestNote:
        _tag = None
        fields = [{
            'form': {}
        }]

    #     def hasTag(self, str):
    #         return str == self._tag

class TestCard:
    _note = TestNote()

class TestReviewer:
    card = TestCard()

# see https://github.com/dae/anki/blob/master/aqt/editor.py
class TestEditor():
    note = TestNote()
    currentField = None

# See http://doc.qt.io/qt-5/qwebenginepage.html
class TestWebView:
    editor = TestEditor()
    reviewer = TestReviewer()

    def selectedText(self): pass
    def selectionChanged(self): pass
    def hasSelection(self): return True

class TMenu:
    pass

class AnkiMaster:
    reviewer = TestReviewer()

mw = AnkiMaster()