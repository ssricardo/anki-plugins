# -*- coding: utf-8 -*-
# This files is part of anki-web-browser addon
# @author ricardo saturnino
# ------------------------------------------------

import sys
import os
import traceback
from .core import Feedback

CWD = os.path.dirname(os.path.realpath(__file__))
RAISE_EXCEPTION = False     # Util on tests
CONFIG_FILE = '/awb-exception.log'

def exceptionHandler(fn):
    def handler(*args, **kargs):
        try:
            return fn(*args, **kargs)
        except Exception as e:
            exc_type, exc_value, _ = sys.exc_info()
            Feedback.log(exc_value)
            infoCode = tryGettingInfo()

            fileInfo = ''
            try:
                f = open(CWD + CONFIG_FILE, 'a+')
                f.write(traceback.format_exc())
                f.write('\n\n' + infoCode + '\n')
                f.close()
                fileInfo = '\nReport stores on ' + CWD + CONFIG_FILE
            except:
                pass

            Feedback.showWarn("Unexpected event: it wasn't possible to complete the operation." + fileInfo)

            if RAISE_EXCEPTION:
                raise e

    return handler

def tryGettingInfo():
    try:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        
        if (exc_tb.tb_next):
            exc_tb = exc_tb.tb_next
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[-1]

        f_locals = ''
        if exc_tb.tb_frame.f_locals:
            filteredValues = filter(cleanVargs, exc_tb.tb_frame.f_locals.items())
            f_locals = '|'.join(map(mapParameters, filteredValues) )
        return '[]'.join((str(exc_type), fname, str(exc_tb.tb_lineno), f_locals))

    except:
        return traceback.format_exc()


def cleanVargs(input):
    if not input:
        return False
    key = input[0]
    return False if key == 'self' or (key.startswith('__')) else True

def mapParameters(input):
    try:
        if not (input and input[1]):
            return ''
        if not isinstance(input[1], str):
            return '' if callable(input[1]) else str(input[1])
        return input[1]
    except:
        return ''