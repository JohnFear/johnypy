#!/usr/bin/python

import struct
import logging
import pandas as pd
from pathlib import Path
from .base import PGN, SPN

__all__ = ['DBCMessage', 'DBCConverter']


class DBCMessage(PGN):
    """DBCMessage extends PGN class"""
    
    __slots__ = ['abbr', 'info']

    STRINGIFY = __slots__

    def __init__(self, pgn, abbr, info=''):
        """Initialize new DBC Message instance"""
        super().init_from_pgn(pgn)
        self.abbr = abbr
        self.info = info


class DBCConverter():
    """DBCConverter for reading, writing and parsing DBC files"""

    def __init__(self):
        """Create new class instance"""

    def read_dbc_file(self, filepath):
        """Read new dbc file for further processing"""
        pass

    def read_j1939da(self, jfile):
        """Read j1939 da csv definition for further processing"""
        path = Path(jfile)
        if not path.is_file():
            logging.error(
                'Failed to load local csv file %s, it does not exists' % (path.resolve()))
        df = pd.read_csv(path.resolve(), sep='|', na_filter=True)

