#!/usr/bin/python

import re
import struct
import logging
import pandas as pd
from pathlib import Path
from .base import PGN, Stringify
from .utils import escapeDBCString
from .const import dbcconst

__all__ = ['DBCMessage', 'DBCConverter', 'DBCMessage', 'DBC']


class DBC(Stringify):
    """DBC file internal class"""

    __slots__ = ['name', 'msgs']

    STRINIFY = __slots__

    def __init__(self, name):
        """Create new DBC file/project instance"""
        self.name = name
        self.msgs = []

    def dump_dbc(self, filepath, force=False):
        """Dump instance as dbc file locally, uses instance name attribute for the name"""
        dst_file = Path(filepath)
        if dst_file.exists() and not force:
            logging.error(
                'Does not support overwrite mode, please remove existing file %s ' % dst_file.resolve())

        with open(dst_file, 'w', encoding='utf-8') as fd:
            payload_parts = {
                'value': '\n',
                'comment': '\n',
                'atrribute': '\n'
            }

            for msg in self.msgs:
                mvalue, mcomment, _ = msg.dbcfy()
                payload_parts['value'] += mvalue
                payload_parts['comment'] += mcomment
                for sig in msg.signals:
                    svalue, scomment, sattribute = sig.dbcfy()
                    payload_parts['value'] += svalue
                    payload_parts['comment'] += scomment
                    payload_parts['atrribute'] += sattribute

            fd.write(dbcconst['header'])
            fd.write(payload_parts['value'])
            fd.write(payload_parts['comment'])
            fd.write(dbcconst['attributeDef'])
            fd.write(payload_parts['atrribute'])
            fd.write('BA_ "DBName" "johnFear";')
            fd.write(dbcconst['footer'])

        return dst_file

    def pretty(self):
        logging.info('DBCFile[%s]' % self.name)
        for msg in self.msgs:
            #['edp', 'dp', 'pgnf', 'pgne', 'pgn']
            logging.info('  message:')
            logging.info('    pgn: %s' % msg.pgn)
            logging.info('    edp: %s' % msg.edp)
            logging.info('    dp: %s' % msg.dp)
            logging.info('    pgne: %s' % msg.pgne)
            logging.info('    prio: %s' % msg.prio)
            logging.info('    abbr: %s' % msg.abbr)
            logging.info('    info: %s' % msg.info)
            logging.info('    length: %s' % msg.length)
            for sig in msg.signals:
                logging.info('      Signal')
                logging.info('        spn: %s' % sig.spn)
                logging.info('        pos: %s' % sig.pos)
                logging.info('        name: %s' % sig.name)
                logging.info('        info: %s' % sig.info)
                logging.info('        slotid: %s' % sig.slot.idx)
                logging.info('        slotname: %s' % sig.slot.name)
                logging.info('        slotgroup: %s' % sig.slot.group)
                logging.info('        slotoffset: %s' % sig.slot.offset)
                logging.info('        slotlength: %s' % sig.slot.length)
                logging.info('        slotmin: %s' % sig.slot.min)
                logging.info('        slotmax: %s' % sig.slot.max)
                logging.info('        slotunit: %s' % sig.slot.unit)
                logging.info('        slotscale: %s' % sig.slot.scale)


class DBCMessage(PGN):
    """DBCMessage extends PGN class"""

    __slots__ = ['prio', 'abbr', 'name', 'length', 'signals']

    STRINGIFY = __slots__ + PGN.STRINGIFY

    def __init__(self, pgn, name, abbr, prio, length=8):
        """Initialize new DBC Message instance"""
        super().__init__(**PGN.parse_pgn(pgn))
        self.name = name
        self.abbr = DBCConverter.escape_name(abbr)
        self.prio = DBCMessage.parse_prio(prio)
        self.length = DBCMessage.parse_length(length)
        self.signals = []

    @classmethod
    def from_dict(cls, vdict):
        """Initiated via dict"""
        return cls(**vdict)

    def calc_canid(self, src=0xFE):
        """Generate canid for current DBCMessage"""
        bcan = bytearray(self.pgn.to_bytes(3, byteorder='big'))
        bcan.append(src)
        bcan[0] |= (int(self.prio)) << 2
        return int.from_bytes(bcan, byteorder='big')

    def dbcfy(self):
        """Generate dbc format string from this instance"""
        canid = self.calc_canid()
        value = 'BO_ %d %s: %d %s\n' % (
            canid, self.abbr, self.length, dbcconst['msgType'])
        comment = 'CM_ BO_ %d "%s";\n' % (canid, self.name)
        attribute = ''
        return value, comment, attribute

    @staticmethod
    def parse_length(length):
        """Parse message lenght"""
        length = length.lower()
        if length == 'nan':
            return 1
        elif 'variable' in length:
            return 1
        else:
            return int(length.split(' ')[0])

    @staticmethod
    def parse_prio(prio):
        """Parse message prio"""
        prio = prio.lower()
        if prio == 'nan':
            return 0
        else:
            return int(prio.split(' ')[0])


class DBCSignal(Stringify):
    """DBCSignal class"""

    __slots__ = ['spn', 'pos', 'name', 'info', 'slot', 'msg']

    STRINGIFY = __slots__

    def __init__(self, spn, pos, name, info, slot, msg=None):
        """Initialize new PGN from canId"""
        super().__init__()
        self.spn = int(spn)
        self.pos = DBCSignal.parse_position(pos)
        self.name = DBCConverter.escape_name(name)
        self.info = DBCConverter.escape_name(info[:10])
        self.slot = slot
        self.msg = msg

    @classmethod
    def from_dict(cls, vdict):
        """Initialize new pgn instance from dict"""
        cls.__init__(**vdict)

    @staticmethod
    def parse_position(pos):
        """Parse start position of dbc signal"""
        idx = pos.split(',')[0].split('-')[0].strip()
        if '.' in idx:
            values = idx.split('.')
            return (int(values[0]) - 1) * 8 + int(values[1]) - 1
        else:
            return (int(idx) - 1) * 8

    def dbcfy(self):
        """Generate dbc format string from this instance"""
        canid = self.msg.calc_canid()
        value = ' SG_ %s: %d|%d@1+ (%0.4f,%0.4f) [%0.4f|%0.4f] "%s" Vector__XXX\n' % (
            self.name, self.pos, self.slot.length, self.slot.scale, self.slot.offset, self.slot.min, self.slot.max, self.slot.unit)
        comment = 'CM_ SG_ %d %s "%s";\n' % (canid, self.name, self.info)
        attribute = 'BA_ "SPN" SG_ %d %s %d;\n' % (canid, self.name, self.spn)
        return value, comment, attribute


class DBCSlot(Stringify):
    """SPN slot class"""
    __slots__ = ['idx', 'name', 'group', 'scale', 'min', 'max', 'unit',
                 'offset', 'length']

    STRINGIFY = __slots__

    def __init__(self, idx, name, group, scale, limits, offset, length):
        """Initialize new slot"""
        super().__init__()
        self.idx = idx
        self.name = DBCSlot.escape_string(name)
        self.group = DBCSlot.escape_string(group)
        self.offset = DBCSlot.parse_offset(offset)
        self.length = DBCSlot.parse_length(length)
        self.min, self.max, self.unit = DBCSlot.parse_range(limits)
        self.scale = DBCSlot.parse_scale(scale)

    @classmethod
    def from_dict(cls, vdict):
        """Initialize new slot instance from dict"""
        cls.__init__(**vdict)

    @staticmethod
    def escape_string(string):
        """Escape string values"""
        return re.sub(r'[ ,]', '_', re.sub(r'\r\n?|\n', ' ', string)) if type(string) == str else string

    @staticmethod
    def parse_length(length):
        """Parse length and return value defined in bits"""
        if type(length) == str:
            length = length.lower()
            if re.match(r'^[0-9]+ bytes?$', length):
                return int(re.sub(r'bytes?', '', length).strip()) * 8
            elif re.match(r'^[0-9]+ bits?$', length):
                return int(re.sub(r'bits?', '', length).strip())
            else:
                return 1
        return int(length)

    @staticmethod
    def parse_offset(offset):
        """Parse offset and return"""
        if type(offset) == str:
            if re.match(r'[\-0-9\.,]+ [\S]+', offset):
                return DBCSlot.parse_float(offset.split(' ')[0])
            elif re.match(r'[\-0-9\.,]+', offset):
                return DBCSlot.parse_float(offset)
            return 0
        return float(offset)

    @staticmethod
    def parse_float(value):
        """Try to parse variabel into float"""
        return float(value.replace(',', '')) if type(value) == str else float(value)

    @staticmethod
    def parse_range(value):
        value = re.sub(r'\(.*?\)', '', value.strip())
        if re.match(r'^-?[0-9.]+ to -?[0-9.]+ [\S]+$', value):
            v = value.split(' ')
            return DBCSlot.parse_float(v[0]), DBCSlot.parse_float(v[2]), v[3]
        elif re.match(r'^[0-9]+ to [0-9]+( per byte)?$', value):
            v = value.split(' ')
            return DBCSlot.parse_float(v[0]), DBCSlot.parse_float(v[2]), 'steps'
        else:
            return 0, 0, value

    @staticmethod
    def parse_scale(scale):
        scale = re.sub(r'\(.*?\)', '', scale.strip())
        if re.match(r'^1/[0-9.]+ .*bit$', scale):
            return float(1/DBCSlot.parse_float(scale.split(' ')[0].split('/')[1]))
        elif re.match(r'^-?[0-9.]+ .*bit$', scale):
            return float(DBCSlot.parse_float(scale.split(' ')[0]))
        elif re.match(r'^-?[0-9.]+/bit$', scale):
            return float(DBCSlot.parse_float(scale.split('/')[0]))
        else:
            return 1


class DBCConverter():
    """DBCConverter for reading, writing and parsing DBC files"""

    def __init__(self):
        """Create new class instance, please verify existency from each vmap key in the PGN class"""
        self.vmap = {
            'msgMap': {
                'pgn': 'PGN',
                'abbr': 'PGNAccro',
                'prio': 'PGNPrio',
                'length': 'PGNLength',
                'name': 'PGNName'
            },
            'sigMap': {
                'spn': 'SPN',
                'pos': 'SPNPos',
                'name': 'SPNName',
                'info': 'SPNInfo',
                'slot': 'SPNSlot'
            },
            'slotMap': {
                'idx': 'SLOT Identifier',
                'name': 'SLOT Name',
                'group': 'SLOT Type',
                'scale': 'Scaling',
                'limits': 'Range',
                'offset': 'Offset',
                'length': 'Length'
            }
        }
        self.slots = {}

    @staticmethod
    def escape_name(name, num=True):
        """Prepare dbc signal name to work in dbc file later"""
        return re.sub(r'\(.*?\)|[^a-zA-Z0-9]', '', name) if num else re.sub(r'\(.*?\)|[^a-zA-Z]', '', name)

    def read_dbc_file(self, filepath):
        """Read new dbc file for further processing"""
        pass

    def _parse_df_row(self, row, vmap):
        """Parse all values defined in vmap and store it into a dictonary"""
        return {key: str(row[value]) for key, value in vmap.items()}

    def parse_dbc_msg(self, row):
        """Parse row into cls class, this method uses stupid as it is the __init__ method"""
        return DBCMessage(**self._parse_df_row(row, self.vmap['msgMap']))

    def parse_dbc_signal(self, msg, row):
        """Parse all dbc signal values and store them into msg instance"""
        sig_values = self._parse_df_row(row, self.vmap['sigMap'])
        sig_values['slot'] = self.slots[int(sig_values['slot'])]
        msg.signals.append(DBCSignal(**sig_values, msg=msg))

    def _parse_slot(self, row):
        """Parse slot row into class object"""
        return DBCSlot(**self._parse_df_row(row, self.vmap['slotMap']))

    def _read_slots(self, sfile, sep='|'):
        """Read slots for futher converstion"""
        df = pd.read_csv(sfile, sep=sep, na_filter=True)
        for _, row in df.iterrows():
            key = row[self.vmap['slotMap']['idx']]
            self.slots[key] = self._parse_slot(row)

    def _prepare_slots(self, sfile):
        """Prepare slots attribute from this instance for spn stuff"""
        spath = Path(sfile)

        if not spath.is_file():
            logging.error(
                'Failed to load local csv file %s, it does not exists' % (spath.resolve()))
            raise FileNotFoundError('No Slot file found')

        if self.slots:
            self._remove_slots()
        self._read_slots(spath)

    def _remove_slots(self):
        """"Remove already parsed slots"""
        self.slots = {}

    def read_j1939da(self, jfile, sfile):
        """Read j1939 da csv definition for further processing"""
        jpath = Path(jfile)

        logging.info('Start to read j1939da definition %s' % jpath.resolve())
        if not jpath.is_file():
            logging.error(
                'Failed to load local csv file %s, it does not exists' % (jpath.resolve()))

        self._prepare_slots(sfile)

        # start dbc stuff
        dbc_file = DBC(jfile.name)

        df = pd.read_csv(jpath.resolve(), sep='|', na_filter=True, dtype=str)
        pgns = df[self.vmap['msgMap']['pgn']].unique()
        groups = df.groupby(self.vmap['msgMap']['pgn'])
        for key in pgns:
            logging.debug('Start to process msg/pgn: %s' % key)
            group = groups.get_group(key)
            msg = self.parse_dbc_msg(group.iloc[0])
            dbc_file.msgs.append(msg)
            for idx in range(group.shape[0]):
                self.parse_dbc_signal(msg, group.iloc[idx])

        return dbc_file
