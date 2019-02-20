# -------------------------------------------------------------
# Module for anki-web-browser addon
# -------------------------------------------------------------

try:
    from .controller import run
    run()
except ImportError as ie:
    print(""" [WARNING] Anki-web-browser ::: It wasn\'t possible to resolve imports. 
        Probably anki was not found, duo to: Running In test mode !!! """)

    print(ie)