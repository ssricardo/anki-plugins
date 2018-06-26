# Anki Schedule prioritization
# Author Ricardo Saturnino
# Version: 0.1

# ========================================  Configuration  ================================================

ENABLED = True  # True | False

# =========================================================================================================

if ENABLED:
    import schedule_priority.priority as pr
    import schedule_priority.uicontrib as uic
    from aqt.utils import showInfo, tooltip

    pr.init()
    uic.init()
    print('Addon Schedule-Priority Loaded')
else:
    print('Addon Schedule-Priority Disabled')
