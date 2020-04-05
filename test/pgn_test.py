#!/usr/bin/python

import sys
from pathlib import Path

libpath = Path('.').joinpath('../')
sys.path.insert(0, str(libpath.resolve()))

import johnypy


if __name__ == "__main__":
    pgn = johnypy.PGN(0, 0, 255, 9)
    print(pgn)

    pgn = johnypy.PGN.from_pgn(65289)
    print(pgn)

    pgn = johnypy.PGN.from_canid(0x18ff0900)
    print(pgn)
