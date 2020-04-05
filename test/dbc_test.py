#!/usr/bin/python

import sys
from pathlib import Path

libpath = Path('.').joinpath('../')
sys.path.insert(0, str(libpath.resolve()))

import johnypy


if __name__ == "__main__":
    home = Path.home()

    mes = johnypy.DBCMessage(65289, 'TC1', 'Transmission Control 1')
    print(mes)
    print(mes.pgn)

    con = johnypy.DBCConverter()
    #jfile = home.joinpath('Downloads/JohnFear/pgnSpn/pgn_spn.csv')
    #con.read_j1939da(jfile)