# -*- coding: utf-8 -*-
# Main interface between Anki and this addon components

# This files is part of schedule-priority addon
# @author ricardo saturnino
# ------------------------------------------------

from .core import Feedback, AppHolder, Priority
from .prioritizer import Prioritizer
from .uicontrib import PriorityCardUiHandler
from .exception import InvalidConfiguration

class Controller:
    """
        The mediator/adapter between Anki with its components and this addon specific API
    """

    def __init__(self, mw):
        self._ankiMw = mw

    def setupHooks(self, schedulerRef, reviewer, hooks):
        reviewer._initWeb = self.wrapInitWeb(reviewer._initWeb)
        hooks.addHook('EditorWebView.contextMenuEvent', PriorityCardUiHandler.onEditorCtxMenu)
        hooks.addHook('AnkiWebView.contextMenuEvent', PriorityCardUiHandler.onReviewCtxMenu)
        hooks.addHook('Reviewer.contextMenuEvent', PriorityCardUiHandler.onReviewCtxMenu)

        hooks.addHook('showQuestion', PriorityCardUiHandler.onShowQA)
        hooks.addHook('showAnswer', PriorityCardUiHandler.onShowQA)

        schedulerRef._nextRevIvl = hooks.wrap(schedulerRef._nextRevIvl, Controller.handle, 'around')

    def setupLegacyHoooks(self, scheduler, hooks):
        scheduler.nextIvl = hooks.wrap(scheduler.nextIvl, Prioritizer.getNextInterval, 'around')
        scheduler._updateRevIvl = hooks.wrap(scheduler._updateRevIvl, Prioritizer.priorityUpdateRevision, 'around')

    def wrapInitWeb(self, fn):

        def _initReviewerWeb(*args):
            fn()
            PriorityCardUiHandler.prepareWebview()

        return _initReviewerWeb

    @staticmethod
    def handle(scheduleInstance, card, ease: int, fuzz: bool, **kargs) -> int:
        f = kargs['_old']

        res = f(scheduleInstance, card, ease, fuzz)
        return Prioritizer.getPrioritizedTime(card, res)

    def loadConfiguration(self):
        Priority.load()

        try:
            config = self._ankiMw.addonManager.getConfig(__name__)

            for item in Priority.priorityList:
                if not item.configName:
                    continue

                confValue = config[item.configName]
                if not confValue:
                    continue

                Priority.setValue(item.configName, confValue)
        except InvalidConfiguration as ie:
            Feedback.showInfo(ie)
            print(ie)
        except Exception as e:
            print(e)
            Feedback.showInfo('It was not possible to read customized configuration. Using defaults...')


def setup():

    import anki
    from aqt import mw
    from anki.schedv2 import Scheduler
    from aqt.utils import showInfo, tooltip
    
    global controller
    controller = Controller(mw)

    # global app
    AppHolder.app = mw

    Feedback.log('Setting schedule-priority controller')
    Feedback.showInfo = tooltip
    Feedback.showError = showInfo

    controller.setupHooks(Scheduler, mw.reviewer, anki.hooks)
    try:
        from anki.sched import Scheduler as SchedLegacy
        controller.setupLegacyHoooks(SchedLegacy, anki.hooks)
    except:
        pass
    controller.loadConfiguration()

# singleton - holds instance
controller = None
