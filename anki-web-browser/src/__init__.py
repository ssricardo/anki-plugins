# -------------------------------------------------------------
# Module for anki-web-browser addon
# -------------------------------------------------------------

__version__ = "1.2"

import sys

try:
    # if not '--test' in sys.argv:
    from .controller import run
    run()
except ImportError as ie:
    print(""" [WARNING] Anki-web-browser ::: It wasn\'t possible to resolve imports. 
        Probably anki was not found, duo to: Running In test mode !!! """)

    print(ie)
    # raise ie