#!/usr/bin/python

import re
import logging

__all__ = ['escapeDBCString']


def escapeDBCString(string):
    if string and str(string) != 'nan':
        if type(string) == str:
            return re.sub(r'\r\n?|\n', ' ', string)
        else:
            logging.debug('Received not an string, skip escape process')
    return string
