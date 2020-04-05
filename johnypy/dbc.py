#!/usr/bin/python

import struct
import logging
import pandas as pd
from pathlib import Path
from .base import PGN, Stringify
from .utils import escapeDBCString

__all__ = ['DBCMessage', 'DBCConverter', 'DBCMessage', 'DBC']


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

    __slots__ = ['abbr', 'info', 'length', 'signals']

    STRINGIFY = __slots__ + PGN.STRINGIFY

    def __init__(self, pgn, abbr, length=8, info=''):
        """Initialize new DBC Message instance"""
        super().__init__(**PGN.parse_pgn(pgn))
        self.abbr = abbr
        self.info = info
        self.length = length
        self.signals = []

    @classmethod
    def from_dict(cls, vdict):
        """Initiated via dict"""
        return cls(**vdict)


class DBCSignal(Stringify):
    """DBCSignal class"""

    __slots__ = ['spn', 'pos', 'info', 'length',
                 'res', 'off', 'drange', 'orange', 'unit']

    STRINGIFY = __slots__

    def __init__(self, spn, pos, info, length, res, off, drange, orange, unit):
        """Initialize new PGN from canId"""
        super().__init__()
        self.spn = spn
        self.pos = pos
        self.info = info
        self.length = length
        self.res = res
        self.off = off
        self.drange = drange
        self.orange = orange
        self.unit = unit

    @classmethod
    def from_dict(cls, vdict):
        """Initialize new pgn instance from dict"""
        cls.__init__(**vdict)


class DBCConverter():
    """DBCConverter for reading, writing and parsing DBC files"""

    def __init__(self):
        """Create new class instance, please verify existency from each vmap key in the PGN class"""
        self.vmap = {
            'msgMap': {
                'pgn': 'PGN#',
                'abbr': 'Acronym',
                'length': 'PGNLength',
                'info': 'PGNLabel'
            },
            'sigMap': {
                'spn': 'SPN',
                'pos': 'SPNPos',
                'info': 'SPNName',
                'length': 'SPNLength',
                'res': 'Resolution',
                'off': 'Offset',
                'drange': 'DataRange',
                'orange': 'OperationalRange',
                'unit': 'Units'
            }
        }

    def read_dbc_file(self, filepath):
        """Read new dbc file for further processing"""
        pass

    def _parse_df_row(self, row, vmap):
        """Parse all values defined in vmap and store it into a dictonary"""
        result = {}
        for key, value in vmap.items():
            result[key] = row[value]
        return result

    def parse_dbc_msg(self, row):
        """Parse row into cls class, this method uses stupid as it is the __init__ method"""
        return DBCMessage(**self._parse_df_row(row, self.vmap['msgMap']))

    def parse_dbc_signal(self, msg, row):
        """Parse all dbc signal values and store them into msg instance"""
        a = DBCSignal(**self._parse_df_row(row, self.vmap['sigMap'])) 
        msg.signals.append(a)

    def read_j1939da(self, jfile):
        """Read j1939 da csv definition for further processing"""
        path = Path(jfile)
        logging.info('Start to read j1939da file %s' % path.resolve())

        if not path.is_file():
            logging.error(
                'Failed to load local csv file %s, it does not exists' % (path.resolve()))

        dbc_file = DBC(jfile.name)

        field_map = self.vmap['msgMap']
        df = pd.read_csv(path.resolve(), sep='|', na_filter=True)
        pgns = df[field_map['pgn']].unique()
        groups = df.groupby(field_map['pgn'])
        for key in pgns:
            logging.debug('Start to process msg/pgn: %s' % key)
            group = groups.get_group(key)
            msg = self.parse_dbc_msg(group.iloc[0])
            dbc_file.msgs.append(msg)

            for idx in range(group.shape[0]):
                self.parse_dbc_signal(msg, group.iloc[idx])

        return dbc_file
