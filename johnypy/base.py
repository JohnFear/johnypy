#!/usr/bin/python

import struct
import logging

__all__ = ['PGN', 'SPN']


class PGN():
    """PGN class"""

    __slots__ = ['edp', 'dp', 'pgnf', 'pgne', 'pgn']

    STRINGIFY = ['edp', 'dp', 'pgnf', 'pgne']

    def __init__(self, edp, dp, pgnf, pgne):
        """Initialize new PGN from canId"""
        self.edp = edp
        self.dp = dp
        self.pgnf = pgnf
        self.pgne = pgne
        self.pgn = self.calc_pgn(edp, dp, pgnf, pgne)

    @staticmethod
    def get_pgn_from_canid(canid):
        """Return pgn from given canid"""
        if type(canid) == int:
            canid = bytearray(canid.to_bytes(4, byteorder='big'))
            canid[0] &= 0x03
            return int.from_bytes(canid[0:3], byteorder='big')
        else:
            logging.warn('Please provide a canid as integer')

    @classmethod
    def from_canid(cls, canid):
        """Initialize new pgn instance from canid"""
        return cls.from_pgn(PGN.get_pgn_from_canid(canid))

    @classmethod
    def from_pgn(cls, pgn):
        """Initialize new pgn instance from pgnid"""
        if type(pgn) == int:
            pgn_bytes = pgn.to_bytes(4, byteorder='big')
            return cls(int(pgn_bytes[0] & 0x02), int(pgn_bytes[0] &
                                                     0x01), int(pgn_bytes[2]), int(pgn_bytes[3]))
        else:
            logging.error('Please provide a pgnid as integer')

    @classmethod
    def from_dict(cls, dvalues):
        """Initialize new pgn instance from dict"""
        cls.__init__(**dvalues)

    def calc_pgn(self, edp, dp, pgnf, pgne):
        """Calculate pgn from it's componets"""
        pgn = struct.pack('<ccc', bytes(
            [dp + 2 * edp]), bytes([pgnf]), bytes([pgne]))
        return int.from_bytes(pgn, byteorder='big')

    def _get_str_values(self):
        """Generate strinified instance values"""
        return list(map(lambda x: '%s: %s' % (str(x), str(self.__getattribute__(x))), self.__slots__))

    def __str__(self):
        """Overwritten string method"""
        return '%s%s' % (self.__class__.__name__, self._get_str_values())

class SPN():
    pass