from board import *
from timing import *
from piece import *
import copy
from my_exceptions import *
import sys
import __builtin__

class null_terminated_list:
    def __init__(self,datatype,num_elements):
        self.datatype = datatype
        self.num_elements = num_elements
        self.data = [datatype()]*num_elements
        self.null_stop = 0
    
    def add(self,e):
#        if type(e) != type(self.datatype()):
#            raise TypeError("Expecting datatype "+str(self.datatype)+", received datatype "+str(type(e)))
#        if self.null_stop >= self.num_elements:
#            raise IndexError("This null terminated list is full, length="+str(self.num_elements))
#        if sys.getsizeof(self.data[self.null_stop]) != sys.getsizeof(e):
#            raise Error("This shit. the datatype size: "+str(sys.getsizeof(self.data[self.null_stop]))+", the element size: " + str(sys.getsizeof(e)))
        self.data[self.null_stop] = e
        self.null_stop += 1
    
    def extend(self,l):
#        if type(l) == type(list()):
#            for e in l:
#                self.add(e)
#        elif type(l) == type(null_terminated_list(self.datatype, self.num_elements)):
        for e in l.get():
            self.add(e)
#        else:
#            raise TypeError("did not understand input content type - should be list or null_terminated_list")
    
    def get(self):
        return self.data[:self.null_stop]
    
    def length(self):
        return self.null_stop
    
    def reset(self):
        self.__init__(self.datatype,self.num_elements)
    
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
            if area<6:
                clean_board()
                return False
    clean_board()
    return True

def find_all_fits(board,piece):
    working_copy = copy.deepcopy(board)
    solns = []
    for p in piece.rotations():
        for t in board.unoccupied():
            try:
                working_copy.place(piece,t.coords,2)
                if not plausible(working_copy):
                    piece.clean()
                    working_copy.unplace(piece.piece_name)
                    continue
                solns.append(copy.deepcopy(working_copy))
                working_copy.unplace(piece.piece_name)
                piece.clean()
            except (DirectionException, EdgeException, InitializationException):
                continue
    return solns

def breadth_first_search(previous_solutions=None):
    pieces = ['boat','tie','check','line','v','heart','s','hexagon','mountains','fedex','nike','weird']
    if previous_solutions==None:
        previous_solutions = [Board()]
    ret = []
    for ps in previous_solutions:
        for piece_name in pieces:
            if piece_name not in ps.piece_names():
                p = Piece(piece_name)
                one_more_piece = find_all_fits(ps,p)
                ret.extend(one_more_piece)
    return ret

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
                yield working_copy
                working_copy.unplace(piece.piece_name)
                piece.clean()
            except (DirectionException, EdgeException, InitializationException):
                continue

def depth_first_search(previous_solution=None,pieces=None):
    if pieces==None:
        pieces = ['boat','tie','check','line','v','heart','s','hexagon','mountains','fedex','nike','weird']
    if previous_solution==None:
        previous_solution = Board()
    if previous_solution.is_solved():
        return previous_solution
    for pn in pieces:
        print "trying", pn
        this_piece = Piece(pn)
        new_pieces = copy.deepcopy(pieces)
        new_pieces.remove(pn)
        working_copy = copy.deepcopy(previous_solution)
        for p in this_piece.rotations():
            for t in previous_solution.unoccupied():
                try:
                    working_copy.place(this_piece,t.coords,2)
                    print "managed to place",pn,"with rotation",this_piece.rotate_state,"at coords",t.coords
                    if not plausible(working_copy):
                        this_piece.clean()
                        working_copy.unplace(this_piece.piece_name)
                        continue
                    return depth_first_search(working_copy,new_pieces)
                    working_copy.unplace(this_piece.piece_name)
                    this_piece.clean()
                except (DirectionException, EdgeException, InitializationException):
                    continue


