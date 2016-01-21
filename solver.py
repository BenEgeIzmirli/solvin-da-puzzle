from board import *
from timing import *
from piece import *
import copy
from my_exceptions import *
import sys
import __builtin__
from plausible import *
from hashlib import md5


stop_considering_edges = 6

def yield_all_fits(board,piece):
    for p in piece.rotations():
        for t in board.unoccupied():
            if board.place(piece,t.coords,2):
                pl = plausible(board)
                if not pl:
                    piece.clean()
                    board.unplace(piece.piece_name)
                    continue
                yield board
                board.unplace(piece.piece_name)
                piece.clean()

def all_pieces_placeable(board,pieces):
    return True
    for pn in pieces:
        p = Piece(pn)
        at_least_one_placement_of_this_piece = False
        for s in yield_all_fits(board,p):
            at_least_one_placement_of_this_piece = True
            break
        if at_least_one_placement_of_this_piece == False:
            return pn
    return True

class Search_History:
    def __init__(self):
        self.sh = {}
    
    def add_entry(self,board):
        self.sh[board.to_string()] = board.is_solved()
    
    def already_searched(self,board):
        try:
            solved = self.sh[board.to_string()]
            return True
        except KeyError:
            return False
    
    def solved_boards(self):
        for b,s in self.sh.iteritems():
            if s:
                yield b


def print_progress(board):
    #print '##########################'
    print "couldn't find any solns for board at rec_lvl",len(board.pieces)
    board.print_board()
    print '------------------------------------------------'
    print '------------------------------------------------'
    #if not already_set:
    #    almost_soln = board
    #    already_set = True


def unplaced_pieces(board):
    pieces = ['boat','tie','check','line','v','heart','s','hexagon','mountains','fedex','nike','weird']
    for p in board.pieces:
        pieces.remove(p.piece_name)
    return pieces


def depth_first_search(previous_solution=Board()):
    #previous_solution.print_board()
    global sh
    pieces = unplaced_pieces(previous_solution)
    sh.add_entry(previous_solution)
    if len(pieces)==0:
        yield previous_solution
    for pn in pieces:
        p = Piece(pn)
        for ns in yield_all_fits(previous_solution,p):
            if sh.already_searched(ns):
                continue
            for sol in depth_first_search(ns):
                yield sol
            #print_progress(ns)


def solve(board=None):
    global sh
    sh = Search_History()
    for sol in depth_first_search(board):
        yield sol






