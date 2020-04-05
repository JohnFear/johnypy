#!/usr/bin/python

import sys
import logging
from pathlib import Path

libpath = Path('.').joinpath('../')
sys.path.insert(0, str(libpath.resolve()))

import johnypy


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    home = Path.home()

    mes = johnypy.DBCMessage(65289, 'TC1', 'Transmission Control 1')
    print(mes)

    con = johnypy.DBCConverter()
    jfile = home.joinpath('Downloads/JohnFear/pgnSpn/pgn_spn.csv')
    dbc = con.read_j1939da(jfile)
    print(dbc)