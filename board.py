from board import *
from tile import *
from traverser import *
from my_exceptions import *
from plotting_helpers import *
import matplotlib.pyplot as plt

# This is the main class that constructs and contains the board.
# Each Board contains a list of Tiles that each contain references
# to all of their neighbors. The user can place Pieces on the Board;
# Pieces are uniquely shaped combinations of Tiles that outline a
# particular shape for the Tiles to be in.
class Board:
    # This class holds the board. Because it is oddly shaped, this
    # constructor must do this horrible cludgeon of code to properly
    # format and create the board in an intuitive manner. The board is
    # constructed of tiles that contain references to all of their neighbors.
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

    # a generator that yields every tile in the board.
    def tiles(self):
        for row in self.board:
            for t in row:
                yield t

    # returns a string that uniquely represents this Board.
    def to_string(self):
        ret = ""
        for t in self.tiles():
            if t.piece_name == None:
                ret += "_"
            else:
                ret += t.piece_name[0]
        return ret

    # returns whether this Board is solved.
    def is_solved(self):
        return len(self.pieces) == 12

    # a generator that yields every unoccupied tile in the Board.
    def unoccupied(self):
        for t in self.tiles():
            if not t.occupied:
                yield t

    # a generator that yields every occupied tile in the Board.
    def occupied(self):
        for t in self.tiles():
            if t.occupied:
                yield t

    def get_pieces(self):
        return self.pieces

    # a generator that yields the name of each of the Pieces placed
    # on this Board.
    def piece_names(self):
        for p in self.pieces:
            yield p.piece_name

    # The tiles that share a border with either the edge of the Board
    # or an occupied tile are labeled "edges"; this generator yields
    # all of the references to the edge tiles.
    def edges(self):
        for e in self.edges:
            yield e

    # the Board class can be accessed like lists, i.e. myboard[3,6]
    def __getitem__(self,tup):
        y = tup[0]
        x = tup[1]
        return self.board[y][x]

    # The tiles that share a border with either the edge of the Board
    # or an occupied tile are labeled "edges"; this function updates
    # the list of edges for the present board.
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

    # places a Piece at a requested position, if it can be placed there.
    # Takes:
    #    piece - the Piece object to be placed
    #    position - the position at which to try to place the Piece object
    #    min_edges - each placement of a Piece may cover a certain number of
    #        "edge tiles"; setting min_edges to a positive integer will require
    #        that the placed Piece cover at least min_edges "edge tiles".
    # Returns:
    #    nothing
    def place(self,piece,position,min_edges=None):
        
        # checks if a given piece fits on the board at the requested position.
        # does not change anything on the Board, just changes the coordinates
        # of the Tiles in the Piece, in preparation for placement on the Board.
        def fits_on_board():
            if self.__getitem__(position).direction != piece.tiles[0].direction:
                raise DirectionException("the first tile of this piece is pointing " + piece.tiles[0].direction + ", the specified position on the board is a tile pointing " + self.__getitem__(position).direction)

            if self.__getitem__(position).occupied:
                raise InitializationException("first tile is occupied")

            piece.tiles[0].coords = position
            has_unplaced_neighbors = [piece.tiles[0]]

            while(len(has_unplaced_neighbors)>0):
                has_unplaced_neighbors_copy = has_unplaced_neighbors
                has_unplaced_neighbors = []
                for p in has_unplaced_neighbors_copy:
                    just_placed = []
                    for d,n in p.neighbors.iteritems():
                        if n.coords == None:
                            self.traverser.set_current(p.coords)
                            try:
                                self.traverser.move_unoccupied(d)
                                n.coords = self.traverser.current.coords
                                just_placed.append(n)
                            except (InitializationException, DirectionException):
                                #traceback.print_exc()
                                piece.clean()
                                raise DirectionException("piece didn't fit on board")
                    has_unplaced_neighbors.extend(just_placed)
            return True

        # checks if the placed Piece will cover enough edges. Does not change anything
        # on the Board.
        def enough_edges_covered():
            if min_edges == None:
                return True
            num_edges_covered = 0
            for t in piece.tiles:
                if self.__getitem__(t.coords).edge:
                    num_edges_covered += 1
            if num_edges_covered < min_edges:
                piece.clean()
                raise EdgeException("not enough edges covered, tile not placed")
            return True

        # places the initialized Piece on the Board.
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
        piece.clean()

    # unplaces a piece from the Board.
    # Takes:
    #    piece_name - a string containing the name of the piece to be unplaced
    # Returns:
    #    nothing
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

    # Shows the board visually with matplotlib
    def print_board(self,size=(10,10)):
        ax = blank_board(size)
        colorDict = {'tie':(1,.5,0),'boat':(1,.8,.3),
                     'check':(.2,.9,.3),'line':(.9,.9,.9),
                     'v':(.7,0,0),'heart':(1,0,0),'s':(0,.6,0),
                     'hexagon':(1,1,0),'mountains':(.4,.5,1),
                     'fedex':(.7,.7,.7),'nike':(0,0,.8),'weird':(.8,.8,0)
                    }
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].piece_name is not None:
                    #print(self.board[i][j].piece)
                    addTile(ax,i,j,color=colorDict[self.board[i][j].piece_name])
        plt.show()


