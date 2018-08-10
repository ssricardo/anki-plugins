# Anki Web Browser
# Author Ricardo Saturnino
# Version: 0.1

# ==================================  Configuration  ==================================

ENABLED = True  # True | False

# The list of web sites available for the searching
# Just follow the same format:
#   * First part (before the colon signal) = Name to be displayed in the menu
#   * Second part = The URL itself. MUST have the {} which will be replaced with the given (selected) text

providers = {
    'Google Web': 'https://google.com/search?q={}',
    'Google Images': 'https://www.google.com/search?tbm=isch&q={}'
}

# "keep browser opened" Option:
# By default, the Web browser is going to be closed when the current card is shifted (that is, a new card assumes the view)
# Valid values = True | False (The first letter (only) MUST be uppercase)
keep_browser_opened = False

# ===================================================================================

if ENABLED:

    from anki_web_browser.controller import run
    from anki_web_browser.config import Config


    Config.providers = providers
    Config.keepBrowserOpened = keep_browser_opened

    run()