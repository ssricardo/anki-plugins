# -*- coding: utf-8 -*-
# Main interface between Anki and this addon components

# This files is part of schedule-priority addon
# @author ricardo saturnino
# ------------------------------------------------

from .core import Feedback
from .priority import Prioritizer
from .uicontrib import PriorityCardUiHandler
from .core import AppHolder, Priority

from anki.hooks import wrap  # check

class Controller:
    """
        The mediator/adapter between Anki with its components and this addon specific API
    """

    def __init__(self, mw):
        self._ankiMw = mw

    def setupHooks(self, theScheduler, hooks):
        theScheduler.nextIvl = wrap(theScheduler.nextIvl, Prioritizer.getNextInterval, 'around')
        theScheduler._updateRevIvl = wrap(theScheduler._updateRevIvl, Prioritizer.priorityUpdateRevision, 'around')
        hooks.addHook('EditorWebView.contextMenuEvent', PriorityCardUiHandler.onEditorCtxMenu)
        hooks.addHook('AnkiWebView.contextMenuEvent', PriorityCardUiHandler.onReviewCtxMenu)


    def loadConfiguration(self):
        print('Anki Priority - Load configuration')
        Priority.load()
        Prioritizer.initMultiplier()

        try:
            config = self._ankiMw.addonManager.getConfig(__name__)

            for item in Priority.priorityList:
                if not item.configName:
                    continue

                confValue = config[item.configName]
                if not confValue:
                    continue

                Prioritizer.setMultiplier(item.configName, confValue)
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
