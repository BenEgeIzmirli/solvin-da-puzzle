from board import *
from tile import *
from traverser import *
from my_exceptions import *
from plotting_helpers import *
import matplotlib.pyplot as plt
from Queue import Queue

class Board:
    def __init__(self):
        self.board = list(range(8))
        self.edges = []
        self.pieces = []
        self.num_occupied = 0
        self.board[0] = list(range(11))
        self.board[1] = list(range(13))
        for i in range(6):
            self.board[i+2] = list(range(13-2*i))
        for i in range(len(self.board)):
            if i<2:
                direction = "up"
            else:
                direction = "down"
            for j in self.board[i]:
                new_t = Tile()
                new_t.direction = direction
                new_t.coords = [i,j]
                self.board[i][j] = new_t
                #direction = (direction == "down" ? "up" : "down")
                if direction == "down":
                    direction = "up"
                elif direction == "up":
                    direction = "down"
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                t = self.board[i][j]
                this_n = {}
                horiz_index_left = j-1
                horiz_index_right = j+1
                if t.direction == "up":
                    vert_index = i+1
                elif t.direction == "down":
                    vert_index = i-1
                
                if horiz_index_left>=0:
                    temp_tile = self.board[i][horiz_index_left]
                    if t.direction == "up":
                        this_n["B"] = temp_tile
                    else:
                        this_n["-C"] = temp_tile
                if horiz_index_right<len(self.board[i]):
                    temp_tile = self.board[i][horiz_index_right]
                    if t.direction == "up":
                        this_n["C"] = temp_tile
                    else:
                        this_n["-B"] = temp_tile
                
                if vert_index in list(range(len(self.board))):
                    if i==0 and t.direction == "up":
                        this_n["A"] = self.board[vert_index][j+1]
                    if i==1 and t.direction == "up":
                        this_n["A"] = self.board[vert_index][j]
                    if i==1 and t.direction == "down":
                        this_n["-A"] = self.board[vert_index][j-1]
                    if i==2 and t.direction == "up":
                        this_n["A"] = self.board[vert_index][j-1]
                    if i==2 and t.direction == "down":
                        this_n["-A"] = self.board[vert_index][j]
                    for k in range(5):
                        if i==k+3 and t.direction == "up":
                            this_n["A"] = self.board[vert_index][j-1]
                        if i==k+3 and t.direction == "down":
                            this_n["-A"] = self.board[vert_index][j+1]
                self.board[i][j].neighbors = this_n
        self.update_edges()
        self.traverser = Traverser(self)
    
    def get_board(self):
        return self.board
    
    def tiles(self):
        for row in self.board:
            for t in row:
                yield t
    
    def to_string(self):
        ret = ""
        for t in self.tiles():
            if t.piece_name == None:
                ret += "_"
            else:
                ret += t.piece_name[0]
        return ret
    
    def is_solved(self):
        return len(self.pieces) == 12
    
    def unoccupied(self):
        for t in self.tiles():
            if not t.occupied:
                yield t
    
    def occupied(self):
        for t in self.tiles():
            if t.occupied:
                yield t
    
    def get_pieces(self):
        return self.pieces
    
    def piece_names(self):
        for p in self.pieces:
            yield p.piece_name
    
    def edges(self):
        for e in self.edges:
            yield e
    
    def __getitem__(self,tup):
        y = tup[0]
        x = tup[1]
        return self.board[y][x]

    def update_edges(self):
        # will be assigned to self.edges at the end
        new_edges = []

        for t in self.tiles():
            # can't be an edge if it's occupied
            if t.occupied:
                t.edge = False
            else:
                # assume it's not an edge
                t.edge = False
                # if it has less than three neighbors, it's an edge 
                if len(t.neighbors)<3:
                    t.edge = True
                else:
                    # if any of its neighbors are occupied, it's an edge
                    for n in t.neighbors.values():
                        if n.occupied:
                            t.edge = True
                if t.edge:
                    t.edge = True
                    new_edges.append(t)
        self.edges = new_edges
    
    def place(self,piece,position,min_edges=None):
        
        def fits_on_board():
            if self.__getitem__(position).direction != piece.tiles[0].direction:
                return False
                #raise DirectionException("the first tile of this piece is pointing " + piece.tiles[0].direction + ", the specified position on the board is a tile pointing " + self.__getitem__(position).direction)
            
            if self.__getitem__(position).occupied:
                return False
                #raise InitializationException("first tile is occupied")
            piece.tiles[0].coords = position
            piece.tiles[0].placed = True
            hun = Queue(6)
            hun.put(piece.tiles[0])
            while not hun.empty():
                t = hun.get()
                for d,n in t.neighbors.iteritems():
                    if n.coords is not None:
                        continue
                    self.traverser.set_current(t.coords)
                    if self.traverser.move_unoccupied(d):
                        n.coords = self.traverser.current.coords
                        hun.put(n)
                    else:
                        piece.clean()
                        return False
                        #raise DirectionException("piece didn't fit on board")
            return True
        
        def enough_edges_covered():
            if min_edges == None:
                return True
            num_edges_covered = 0
            for t in piece.tiles:
                if self.__getitem__(t.coords).edge:
                    num_edges_covered += 1
            if num_edges_covered < min_edges:
                piece.clean()
                return False
                #raise EdgeException("not enough edges covered, tile not placed")
            return True
        
        def place_piece():
            self.pieces.append(piece)
            self.num_occupied += 6
            for t in piece.tiles:
                board_t = self.__getitem__(t.coords)
                board_t.occupied = True
                board_t.piece_name = piece.piece_name
        
        if fits_on_board() and enough_edges_covered():
            place_piece()
            self.update_edges()
        else:
            return False
        piece.clean()
        return True
    
    def unplace(self,piece_name):
        for t in self.occupied():
            if t.piece_name == piece_name:
                t.occupied = False
                t.piece_name = None
        for p in self.get_pieces():
            if p.piece_name == piece_name:
                self.pieces.remove(p)
        self.update_edges()
        self.num_occupied -= 1
    
    def print_board(self,size=(10,10)):
        ax = blank_board(size)
        colorDict = {'tie':(1,.5,1),'boat':(0,0,0),
                     'check':(.5,1,1),'line':(1,1,.5),
                     'v':(.5,.5,.5),'heart':(.5,.5,1),'s':(.5,1,.5),
                     'hexagon':(.2,.2,.2),'mountains':(.7,.2,.7),
                     'fedex':(.2,.7,.2),'nike':(.2,.4,.7),'weird':(0,.3,.7)
                    }
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].piece_name is not None:
                    #print(self.board[i][j].piece)
                    addTile(ax,i,j,color=colorDict[self.board[i][j].piece_name])
        plt.show()


