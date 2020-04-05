#!/usr/bin/python

import struct
import logging
import pandas as pd
from pathlib import Path
from .base import PGN, SPN

__all__ = ['DBCMessage', 'DBCConverter']

class DBCMessage(PGN):
    """DBCMessage extends PGN class"""

    def __init__(self, pgn):
        """Initialize new DBC Message instnace"""
        super(DBCMessage, PGN).from_pgn(pgn)


class DBCConverter():
    """DBCConverter for reading, writing and parsing DBC files"""

    def __init__(self):
        """Create new class instance"""
        self.dbc = None

    def read_dbc_file(self, filepath):
        """Read new dbc file for further processing"""
        pass

    def read_j1939da(self, filepath):
        """Read j1939 da csv definition for further processing"""
        path = Path(filepath)
        if not path.is_file():
            logging.error(
                'Failed to load local csv file %s, it does not exists' % (path.resolve()))
        df = pd.read_csv(filepath)

