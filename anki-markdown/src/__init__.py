# -------------------------------------------------------------
# Module for anki-markdown addon
# -------------------------------------------------------------

__version__ = "3.0"

try:
    from .controller import run
    run()
except ImportError as ie:
    print(""" [WARNING] Anki-Markdown ::: It wasn\'t possible to resolve imports. 
        Probably anki was not found, duo to: Running In test mode !!! """)

    print(ie)