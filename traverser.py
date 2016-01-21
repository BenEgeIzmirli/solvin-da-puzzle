from my_exceptions import *

class Traverser:
    def __init__(self,board):
        self.board = board
        self.current = None
    
    def set_current(self,coords):
        self.current = self.board[coords[0],coords[1]]
    
    def move(self,direction):
        if self.current == None:
            return False
            #raise InitializationException("Not currently initialized to a tile.")
        if direction not in self.current.neighbors.keys():
            return False
            #raise DirectionException("Not a valid direction - this tile is pointing " + self.current.direction + " and you were trying to move in direction " + direction)
        self.current = self.current.neighbors[direction]
        return True
    
    def move_unoccupied(self,direction):
        if self.current == None:
            return False
            #raise InitializationException("Not currently initialized to a tile.")
        if direction not in self.current.neighbors.keys():
            return False
            #raise DirectionException("Not a valid direction - this tile is pointing " + self.current.direction + " and you were trying to move in direction " + direction)
        if self.current.neighbors[direction].occupied:
            return False
            #raise DirectionException("Tile in this direction is occupied")
        self.current = self.current.neighbors[direction]
        return True