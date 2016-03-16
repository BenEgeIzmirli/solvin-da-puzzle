from board import *
from piece import *
import copy
from plausible import *
from solver_helper import *


# Solves the given board. If no board is given, assumes a blank board.
# Takes:
#    board - the Board object to be solved
# Returns:
#    this function is a generator, it yields fully solved Board objects
def solve(board=Board()):
    global sh
    sh = Search_History()
    for sol in depth_first_search(board):
        yield sol


# Recursively solves the given Board object to find a solution. Should be
# run through solve(). Places one more piece, then recursively calls itself
# until all pieces are placed.
# Takes:
#    previous_solution - the Board object containing the solution on which to
#        place one more piece.
# Returns:
#    this function is a generator, it yields fully solved Board objects
def depth_first_search(previous_solution):
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


# a generator that yields all of the possible placements of a given piece
# on the specified board.
# Takes:
#    board - the Board object on which to try to place pieces
#    piece - the Piece object to try to place.
# Returns:
#    this function is a generator, it yields all the possible Board objects
#    with the given piece placed. It includes not only translations of the
#    Piece object but also rotations and mirror-image flips.
def yield_all_fits(board,piece):
    working_copy = copy.deepcopy(board)
    for p in piece.rotations():
        for t in board.unoccupied():
            try:
                working_copy.place(piece,t.coords,2)
                if not plausible(working_copy):
                    piece.clean()
                    working_copy.unplace(piece.piece_name)
                    continue
                yield copy.deepcopy(working_copy)
                working_copy.unplace(piece.piece_name)
                piece.clean()
            except (DirectionException, EdgeException, InitializationException):
                continue







