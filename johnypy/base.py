#!/usr/bin/python

import struct
import logging

__all__ = ['PGN', 'Stringify']


class Stringify():
    """Abstract stringify class"""

    __slots__ = []
    STRINGIFY = []

    def __init__(self):
        """Strinfiy abstract class ctor which does nothing"""

    def _get_str_values(self):
        """Generate strinified instance values"""
        return list(map(lambda x: '%s: %s' % (str(x), str(self.__getattribute__(x))), self.__slots__))

    def __str__(self):
        """Overwritten string method"""
        return '%s%s' % (self.__class__.__name__, self._get_str_values())

    def __repr__(self):
        """Overwrite repr for list strinify"""
        return self.__str__()


class PGN(Stringify):
    """PGN class"""

    __slots__ = ['edp', 'dp', 'pgnf', 'pgne', 'pgn']

    STRINGIFY = __slots__

    def __init__(self, edp, dp, pgnf, pgne):
        """Initialize new PGN from canId"""
        super().__init__()
        self.edp = edp
        self.dp = dp
        self.pgnf = pgnf
        self.pgne = pgne
        self.pgn = self.calc_pgn(edp, dp, pgnf, pgne)

    @staticmethod
    def parse_canid(canid):
        """Return pgn from given canid"""
        if type(canid) == int:
            pgn = bytearray(canid.to_bytes(4, byteorder='big')[0:3])
            pgn[0] &= 0x03
            pgn = int.from_bytes(pgn, byteorder='big')
            return PGN.parse_pgn(pgn)
        else:
            logging.warn('Please provide a canid as integer')

    @staticmethod
    def parse_pgn(pgn):
        """Parse canid into j1939 relevant data"""
        d = {}
        pgn = int(pgn) if type(pgn) != int else pgn
        pgn_bytes = pgn.to_bytes(4, byteorder='big')
        d['edp'] = int(pgn_bytes[0] & 0x02)
        d['dp'] = int(pgn_bytes[0] & 0x01)
        d['pgnf'] = int(pgn_bytes[2])
        d['pgne'] = int(pgn_bytes[3])
        return d

    @classmethod
    def from_canid(cls, canid):
        """Initialize new pgn instance from canid"""
        return cls(**PGN.parse_canid(canid))

    @classmethod
    def from_pgn(cls, pgn):
        """Initialize new pgn instance from pgnid"""
        return cls(**PGN.parse_pgn(pgn))

    @classmethod
    def from_dict(cls, vdict):
        """Initialize new pgn instance from dict"""
        cls.__init__(**vdict)

    def calc_pgn(self, edp, dp, pgnf, pgne):
        """Calculate pgn from it's componets"""
        pgn = struct.pack('<ccc', bytes(
            [dp + 2 * edp]), bytes([pgnf]), bytes([pgne]))
        return int.from_bytes(pgn, byteorder='big')