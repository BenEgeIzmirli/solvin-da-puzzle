from tile import Tile
from null_terminated_list import *

def flood_fill(board,t):
    num_filled = 0
    t.flood_filled = True
    num_filled += 1
    unfilled = null_terminated_list(Tile,67)
    for n in t.neighbors.values():
        if not n.occupied:
            unfilled.add(n)
    while(unfilled.length()>0):
        unfilled_temp = null_terminated_list(Tile,67)
        for uf in unfilled.get():
            if not uf.occupied and not uf.flood_filled:
                uf.flood_filled = True
                num_filled += 1
                for n in uf.neighbors.values():
                    if n.occupied:
                        continue
                    if n.flood_filled:
                        continue
                    unfilled_temp.add(n)
        unfilled = unfilled_temp
    return num_filled

def plausible(board):
    def clean_board():
        for t in board.unoccupied():
            t.flood_filled = False
    for t in board.unoccupied():
        area = 0
        if not t.flood_filled:
            area = flood_fill(board,t)
            if area%6 != 0:
                clean_board()
                return False
    clean_board()
    return True
