
# returns whether the two Board objects passed in are identical.
def same_board(b1,b2):
    occupied_b1 = [t.coords for t in b1.occupied()]
    occupied_b2 = [t.coords for t in b2.occupied()]
    return occupied_b1 == occupied_b2

# This class functions as a dynamic programming cache for the
# solve function.
class Search_History:
    def __init__(self):
        self.sh = {}
    
    # cache entries are added by passing in the reference to the board
    def add_entry(self,board):
        self.sh[board.to_string()] = board.is_solved()
    
    # returns True if the board has already been searched, False otherwise
    def already_searched(self,board):
        return board.to_string() in self.sh
    
    # this is a generator, it yields the string representations of all
    # boards that have been solved so far.
    def solved_boards(self):
        for b,s in self.sh.iteritems():
            if s:
                yield b

# Given a board, returns the list of pieces that remain to be placed.
def unplaced_pieces(board):
    pieces = ['boat','tie','check','line','v','heart','s','hexagon','mountains','fedex','nike','weird']
    for p in board.pieces:
        pieces.remove(p.piece_name)
    return pieces
