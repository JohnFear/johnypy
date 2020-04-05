#!/usr/bin/python

import struct
import logging
import pandas as pd
from pathlib import Path
from .base import PGN, SPN, Stringify
from .utils import escapeDBCString

__all__ = ['DBCMessage', 'DBCConverter']


class DBC(Stringify):
    """DBC file internal class"""

    __slots__ = ['name', 'msgs']

    STRINIFY = __slots__

    def __init__(self, name):
        """Create new DBC file/project instance"""
        self.name = name
        self.msgs = []


class DBCMessage(PGN):
    """DBCMessage extends PGN class"""

    __slots__ = ['abbr', 'info', 'signals']

    STRINGIFY = __slots__ + PGN.STRINGIFY

    def __init__(self, pgn, abbr, info=''):
        """Initialize new DBC Message instance"""
        super().__init__(**PGN.parse_pgn(pgn))
        self.abbr = abbr
        self.info = info
        self.signals = []


class DBCConverter():
    """DBCConverter for reading, writing and parsing DBC files"""

    def __init__(self):
        """Create new class instance"""
        self.config = {
            'csvMap': {
                'pgn': 'PGN#',
                'abbr': 'Acronym',
                'info': 'PGNDescription'
            }
        }

    def read_dbc_file(self, filepath):
        """Read new dbc file for further processing"""
        pass

    def parse_dbc_msg(self, row):
        """Parse row into cls class, this method uses stupid as it is the __init__ method"""
        pgn_map = self.config['csvMap']
        return DBCMessage(row[pgn_map['pgn']], row[pgn_map['abbr']], escapeDBCString(row[pgn_map['info']]))

    def read_j1939da(self, jfile):
        """Read j1939 da csv definition for further processing"""
        path = Path(jfile)
        logging.info('Start to read j1939da file %s' % path.resolve())

        if not path.is_file():
            logging.error(
                'Failed to load local csv file %s, it does not exists' % (path.resolve()))

        dbc_file = DBC(jfile.name)

        field_map = self.config['csvMap']
        df = pd.read_csv(path.resolve(), sep='|', na_filter=True)
        pgns = df[field_map['pgn']].unique()
        groups = df.groupby(field_map['pgn'])
        for key in pgns:
            logging.debug('Start to process msg/pgn: %s' % key)
            group = groups.get_group(key)
            msg = self.parse_dbc_msg(group.iloc[0])
            dbc_file.msgs.append(msg)
            
            for row in group.index:
                # TODO: parse all spns
                
                pass
        
        return dbc_file
