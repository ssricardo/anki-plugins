# -*- coding: utf-8 -*-
# -------------------------
# Anki Web Browser
# -------------------------
# Author Ricardo Saturnino

# ==================================  Enabled ?  ==================================

# Values: True or False
ENABLED = True

# False will remove all actions from this addon, without removing it from Anki
# For configurations, please use the Config window, under Tools

if ENABLED:

    from anki_web_browser.controller import run
    run()