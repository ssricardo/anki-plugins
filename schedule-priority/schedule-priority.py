# Anki Schedule prioritization
# Author Ricardo Saturnino
# Version: 0.1

# ========================================  Configuration  ================================================

ENABLED = True  # True | False


# The following configurations refer to the multiplier (percent) used for getting the next interval (schedule) for a given card
# Consider, the normal card is always 100 (that is, 100% of the interval calculated by anki)

# Below, indicate the multiplier for Low and High priority:
#   * High priority: MUST be below 100 (Because: cards with higher priority should be reviewed in a shorted interval) 
#   * Low  priority: MUST be above 100 (Which is goint to result in a longer time)

low_priority_multiplier = 140
high_priority_multiplier = 70

# =========================================================================================================

if ENABLED:
    import schedule_priority.priority as pr
    import schedule_priority.uicontrib as uic
    import schedule_priority.const as const
    from aqt.utils import showInfo, tooltip

    pr.Prioritizer.setMultiplier(const.Priority.LOW, low_priority_multiplier)
    pr.Prioritizer.setMultiplier(const.Priority.HIGH, high_priority_multiplier)

    pr.init()
    uic.init()
    print('Addon Schedule-Priority Loaded')
else:
    print('Addon Schedule-Priority Disabled')
