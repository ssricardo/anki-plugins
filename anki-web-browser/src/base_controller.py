# ---------------------------------- ================ ---------------------------------
# ---------------------------------- Base Controller -----------------------------------
# ---------------------------------- ================ ---------------------------------

from .config import service as cfg
from .core import Feedback
from .exception_handler import exceptionHandler
from .browser import AwBrowser
from .no_selection import NoSelectionController, NoSelectionResult
from .provider_selection import ProviderSelectionController

from aqt.utils import openLink      # TODO remove

class BaseController:
    "Concentrates common operations between both concrete controllers"

    browser = None
    _lastProvider = None
    _currentNote = None
    _ankiMw = None    

    def __init__(self, ankiMw):
        super().__init__()
        self._ankiMw = ankiMw
        self.browser = AwBrowser.singleton(ankiMw)
        self._noSelectionHandler = NoSelectionController(ankiMw)
        self._providerSelection = ProviderSelectionController()
    
    @exceptionHandler
    def _repeatProviderOrShowMenu(self, webView):
        query = self._getQueryValue(webView)
        if not query:
            return
        self.openInBrowser(query)

    def _filterQueryValue(self, query: str):
        "Remove words defined on filteredWords from config"

        filteredWords = cfg.getConfig().filteredWords
        if not filteredWords:
            return query
        querywords = query.split()
        resultwords  = [word for word in querywords if word.lower() not in filteredWords]
        return ' '.join(resultwords)

    def _getQueryValue(self, input):
        raise Exception('Must be overriden')

    def openInBrowser(self, query):
        """
            Setup enviroment for web browser and invoke it
        """

        Feedback.log('OpenInBrowser: {}'.format(self._currentNote))
        website = self._lastProvider

        if cfg.getConfig().useSystemBrowser:
            target = self.browser.formatTargetURL(website, query)
            # openLink(target)
            self.openExternalLink(target)
            return
        
        self.beforeOpenBrowser()
        # self.browser.setFields(None)   # clear fields
        # self.browser.infoList = ['No action available on Reviewer mode']
        self.browser.open(website, query)

    def beforeOpenBrowser(self):
        raise Exception('Must be overriden')

    def openExternalLink(self, target):
        raise Exception('Must be overriden')

