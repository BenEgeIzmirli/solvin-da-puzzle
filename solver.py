from board import *
from timing import *
from piece import *
import copy
from my_exceptions import *
import sys
import __builtin__
from plausible import *
import multiprocessing as mp
import threading
import Queue

def yield_all_fits(board,piece):
    for p in piece.rotations():
        for t in board.edges:
            if board.place(piece,t.coords,2):
                pl = plausible(board)
                if not pl:
                    piece.clean()
                    board.unplace(piece.piece_name)
                    continue
                yield board
                board.unplace(piece.piece_name)
                piece.clean()

def yield_all_fits_mp_helper(board,piece,t_coords):
    #board,piece,t_coords = tup
    return board.fits_on_board(piece,t_coords)


class myThread(threading.Thread):
    def __init__(self,board,pieces_q,locks):
        threading.Thread.__init__(self)
        self.board = board
        self.pieces_q = pieces_q
        self.piece = None
        self.results = None
        self.locks = locks
        self.active = False
    
    def run(self):
        self.active = True
        def empty():
            self.locks["queue"].acquire()
            empty = self.pieces_q.empty()
            self.locks["queue"].release()
            return empty
        def get_piece():
            self.locks["queue"].acquire()
            out = self.pieces_q.get()
            self.piece = out[0]
            self.results = out[1]
            self.locks["queue"].release()
        def set_result(result):
            self.locks["results"].acquire()
            self.results.append(result)
            self.locks["results"].release()
        def place(piece):
            self.locks["board"].acquire()
            self.board.place(piece)
            self.locks["board"].release()
        def unplace(piece):
            self.locks["board"].acquire()
            self.board.unplace(piece.piece_name)
            self.locks["board"].release()
        
        while not empty():
            get_piece()
            for e in self.board.edges:
                if self.board.fits_on_board(self.piece,e.coords):
                    self.results.append([t.coords for t in self.piece.tiles])
                else:
                    self.results.append(None)
        self.active = False

def printme(this,wait=0.1):
    print this
    time.sleep(wait)

def yield_all_fits_mp(board,piece,num_threads):
    locks = {
        "board" : threading.Lock(),
        "queue" : threading.Lock(),
        "results" : threading.Lock()
        }
    pieces_and_fits = [(copy.deepcopy(pr),[]) for pr in piece.rotations()]
    
    #printme('a')
    
    q = Queue.Queue()
    locks["queue"].acquire()
    for r in pieces_and_fits:
        q.put(r)
    locks["queue"].release()
    
    threads = []
    for i in range(num_threads):
        thread = myThread(board,q,locks)
        thread.start()
        threads.append(thread)
    
    #printme('b')
    
    for t in threads:
        t.join()
    
#    keep_trying = True
#    while keep_trying:
#        keep_trying = False
#        for t in threads:
#            if t.active:
#                keep_trying = True
#        #time.sleep(0.001)
    
    #printme('c')
    
    for pf in pieces_and_fits:
        p,f = pf
        #printme('---starting new piece '+str(p.piece_name))
        for i in range(len(board.edges)):
            this_fit = f[i]
            #printme('this_fit '+str(this_fit))
            if this_fit is not None:
                for c in range(len(this_fit)):
                    coord = this_fit[c]
                    #printme('-coord ' + str(coord))
                    p.tiles[c].coords = coord
                board.place(p)
                if plausible(board):
                    #printme("was plausible")
                    yield copy.deepcopy(board)
                #printme("wasn't plausible")
                board.unplace(p.piece_name)
    

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
    #print '--------'
    for p in board.pieces:
        #print p.piece_name
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

def depth_first_search_mp(previous_solution,num_threads=1):
    ps = copy.deepcopy(previous_solution)
    ps.print_board()
    global sh
    pieces = unplaced_pieces(ps)
    sh.add_entry(ps)
    if len(pieces)==0:
        yield ps
    for pn in pieces:
        p = Piece(pn)
        for ns in yield_all_fits_mp(ps,p,num_threads):
            if sh.already_searched(ns):
                continue
            printme('doing a depth first search with this')
            for sol in depth_first_search_mp(ns,num_threads):
                yield sol
            #print_progress(ns)


def solve(board=Board(),num_threads=1):
    global sh
    sh = Search_History()
    if num_threads>1:
        for sol in depth_first_search_mp(board,num_threads):
            yield copy.deepcopy(sol)
    else:
        for sol in depth_first_search(board):
            yield copy.deepcopy(sol)




