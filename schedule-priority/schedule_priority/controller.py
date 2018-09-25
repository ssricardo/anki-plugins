# -*- coding: utf-8 -*-
# Main interface between Anki and this addon components

# This files is part of schedule-priority addon
# @author ricardo saturnino
# ------------------------------------------------

from schedule_priority.core import Feedback, AppHolder, Priority
from schedule_priority.prioritizer import Prioritizer
from schedule_priority.uicontrib import PriorityCardUiHandler
from schedule_priority.exception import InvalidConfiguration

class Controller:
    """
        The mediator/adapter between Anki with its components and this addon specific API
    """

    def __init__(self, mw):
        self._ankiMw = mw

    def setupHooks(self, schedulerRef, hooks):
        schedulerRef.nextIvl = hooks.wrap(schedulerRef.nextIvl, Prioritizer.getNextInterval, 'around')
        schedulerRef._updateRevIvl = hooks.wrap(schedulerRef._updateRevIvl, Prioritizer.priorityUpdateRevision, 'around')
        hooks.addHook('EditorWebView.contextMenuEvent', PriorityCardUiHandler.onEditorCtxMenu)
        hooks.addHook('AnkiWebView.contextMenuEvent', PriorityCardUiHandler.onReviewCtxMenu)
        hooks.addHook('Reviewer.contextMenuEvent', PriorityCardUiHandler.onReviewCtxMenu)


    def loadConfiguration(self):
        print('Anki Priority - Load configuration')
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

    print('Setting up schedule-priority')

    import anki
    from aqt import mw
    from aqt.editor import Editor
    from aqt.reviewer import Reviewer
    from anki.sched import Scheduler
    from aqt.qt import QAction
    from aqt.utils import showInfo, tooltip, showWarning
    
    global controller
    controller = Controller(mw)

    # global app
    AppHolder.app = mw

    Feedback.log('Setting schedule-priority controller')
    Feedback.showInfo = tooltip
    Feedback.showError = showWarning

    controller.setupHooks(Scheduler, anki.hooks)
    controller.loadConfiguration()

# singleton - holds instance
controller = None
