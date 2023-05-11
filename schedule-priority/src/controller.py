# -*- coding: utf-8 -*-
# Main interface between Anki and this addon components
from anki.cards import Card

# This files is part of schedule-priority addon
# @author ricardo saturnino
# ------------------------------------------------

from .core import Feedback, AppHolder, Priority, InvalidConfiguration
from .prioritizer import get_prioritized_time, get_card_multiplier, PrioInterface
from .uicontrib import PriorityCardUiHandler
from .schedv3_interface import set_card_priority

import anki
from aqt import mw, gui_hooks

try:
    from anki.scheduler.v2 import Scheduler
except ImportError:
    from anki.schedv2 import Scheduler

from aqt.utils import showInfo, tooltip
from aqt.reviewer import Reviewer

PrioInterface.priority_list = lambda: Priority.priorityList
PrioInterface.showInfo = Feedback.showInfo
PrioInterface.showError = Feedback.showError


class Controller:
    """
        The mediator/adapter between Anki with its components and this addon specific API
    """

    def __init__(self, mw):
        self._ankiMw = mw

    def setupHooks(self, schedulerRef: Scheduler, reviewer: Reviewer):
        hooks = anki.hooks
        reviewer._initWeb = hooks.wrap(reviewer._initWeb, Controller.initWebAddon)
        hooks.addHook('EditorWebView.contextMenuEvent', PriorityCardUiHandler.onEditorCtxMenu)
        hooks.addHook('AnkiWebView.contextMenuEvent', PriorityCardUiHandler.onReviewCtxMenu)
        hooks.addHook('Reviewer.contextMenuEvent', PriorityCardUiHandler.onReviewCtxMenu)

        hooks.addHook('showQuestion', PriorityCardUiHandler.onShowQA)
        hooks.addHook('showAnswer', PriorityCardUiHandler.onShowQA)

        schedulerRef._nextRevIvl = hooks.wrap(schedulerRef._nextRevIvl, Controller.get_next_review_interval, 'around')

    @staticmethod
    def initWebAddon():
        PriorityCardUiHandler.prepareWebview()

    @staticmethod
    def get_next_review_interval(scheduleInstance, card, ease: int, fuzz: bool, **kargs) -> int:
        f = kargs['_old']

        res = f(scheduleInstance, card, ease, fuzz)
        return get_prioritized_time(card, res)

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


def prepare_v3():
    gui_hooks.card_will_show.append(set_card_priority)


def setup():
    global controller
    controller = Controller(mw)

    # global app
    AppHolder.app = mw

    Feedback.log('Setting schedule-priority controller')
    Feedback.showInfo = tooltip
    Feedback.showError = showInfo

    controller.setupHooks(Scheduler, mw.reviewer)
    controller.loadConfiguration()

    prepare_v3()


# singleton - holds instance
controller = None
