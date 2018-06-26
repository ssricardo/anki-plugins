# Constants for schedule-priority

class Tag:
    """ Priorities are marked using anki Tags. Here are the tags names """
    
    LOW = 'priority:low'
    HIGH = 'priority:high'

class Priority:
    """Refer to internal keys used in each case"""

    LOW = Tag.LOW
    NORMAL = 0
    HIGH = Tag.HIGH

class Label:
    """ Texts in the interface """

    CARD_MENU = 'Card Priority'
    MENU_LOW = 'Low'
    MENU_NORMAL = 'Normal'
    MENU_HIGH = 'High'