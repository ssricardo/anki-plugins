# -------------------------------------------------------------
# Module for anki-web-browser addon
# -------------------------------------------------------------

__version__ = "3.0"

import sys

def logToConsole(*args, **kargs):
    try:
        print(args, kargs)
    except Exception as e:
        print(e)

try:
    # if not '--test' in sys.argv:

    # Uncomment to produce more logs on console
    from .core import Feedback
    Feedback.log = logToConsole

    from .review_controller import run
    run()
except ImportError as ie:
    print(""" [WARNING] Anki-web-browser ::: It wasn\'t possible to resolve imports. 
        Probably anki was not found, duo to: Running In test mode !!! """)

    print(ie)
    # raise ie