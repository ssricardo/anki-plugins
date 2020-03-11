# -*- coding: utf-8 -*-
# Contains center components useful across this addon
# Holds Contansts

# This files is part of anki-markdown addon
# @author ricardo saturnino
# ------------------------------------------------

'Application reference. Must be bind on startup'
class AppHolder:
    app = None


class Label:
    CARD_MENU = 'Apply markdown'
    BROWSER_ASSIGN_TO = '&Assign to field'


class Style:
    'Holds custom CSS styling'

    MARKDOWN = """
<style type="text/css">
h1, h2, h3, h4 {    
    font-weight: 400;
}
h1, h2, h3, h4, h5, p {
    margin-bottom: 10px;
    padding: 0;
}
h1 {
    font-size: 42px;
}
h2 {
    font-size: 32px;
    margin: 24px 0 6px;
}
h3 {
    font-size: 22px;
}
h4 {
    font-size: 20px;
}
h5 {
    font-size: 18px;
}

blockquote {
    margin: 3px;
    border-left: 1px solid red;
    padding-left: 5px;
}

pre {
    padding: 2px 10px;
    white-space: pre-wrap;
}
code {
    font-family: Consolas, Monaco, Andale Mono, monospace;
    line-height: 1.2;
    font-size: 13px;
}
.amd {
    border-left: 2px solid #7e08ed;
    padding-left: 5px;
    display: block;
}

pre.amd {
    margin: 0px;
    padding: 0;
    border-left: 2px solid #7e08ed;
}

.amd textarea {
    resize: none;
    width:95%; 
}

.amd_edit_notice {
    float: right;
    color: orange;
}
</style>
"""

# --------------------------- Util function ----------------------------

class Feedback:
    'Responsible for messages and logs'

    @staticmethod
    def log(*args, **kargs):
        # pass
        print(args, kargs)

    @staticmethod
    def showInfo(*args):
        pass

    @staticmethod
    def showError(*args):
        pass