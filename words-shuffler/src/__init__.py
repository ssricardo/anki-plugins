# -------------------------------------------------------------
# Module for words-shuffler
# -------------------------------------------------------------

__version__ = "1.0"

try:
    from .controller import run
    run()
except ImportError as ie:
    print(""" [WARNING] Anki Tokenizer ::: It wasn\'t possible to resolve imports. 
        Probably anki was not found, duo to: Running In test mode !!! """)

    print(ie)