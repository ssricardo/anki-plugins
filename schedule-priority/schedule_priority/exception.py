# -*- coding: utf-8 -*-
#
# This files is part of schedule-priority addon
# @author ricardo saturnino

# Contains the module exceptions / constraints

class InvalidConfiguration(Exception):
    
    def __init__(self, message):
        super().__init__(message)