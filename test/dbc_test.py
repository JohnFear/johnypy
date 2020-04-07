#!/usr/bin/python

import sys
import logging
from pathlib import Path

libpath = Path('.').joinpath('../')
sys.path.insert(0, str(libpath.resolve()))

import johnypy

def convert_csv_to_dbc():
    home = Path.home()
    con = johnypy.DBCConverter()
    jfile = home.joinpath('Downloads/JohnFear/dbcGeneration/pgn_spn.csv')
    sfile = home.joinpath('Downloads/JohnFear/dbcGeneration/slots.csv')
    dbc = con.read_j1939da(jfile, sfile)
    dbc.dump_dbc(home.joinpath('Downloads/JohnFear/dbcGeneration/johnFear.dbc'), True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    convert_csv_to_dbc()
    