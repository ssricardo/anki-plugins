# -------------------------------------------------------------
# Module for fill-the-blanks addon
# -------------------------------------------------------------

__version__ = "2.4"

try:
    from .controller import run
    run()
except ImportError as ie:
    print(""" [WARNING] Fill the Blanks ::: It wasn\'t possible to resolve imports. 
        Probably anki was not found, duo to: Running In test mode !!! """)

    print(ie)