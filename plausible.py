from tile import Tile

# This function checks whether a Board could plausibly be used to
# construct a solution to the puzzle. It simply checks whether
# there are any contiguous regions that are not multiples of
# 6 cells - since each tile is 6 pieces, a Board where there is
# a closed-off region 10 cells large could not plausibly be filled
# with 6 cell tiles.
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

# Does a simple flood fill. Returns the size of the area connected
# to the given tile.
# Takes:
#    board - the Board object on which to perform the flood fill.
#    t - a reference to the tile from which to start the flood fill.
# Returns:
#    the size of the unoccupied-tiles area connected to t.
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

# An efficient Python list that is not dynamically sized.
# Does no typechecking for maximum efficiency.
class null_terminated_list:
    def __init__(self,datatype,num_elements):
        self.datatype = datatype
        self.num_elements = num_elements
        self.data = [datatype()]*num_elements
        self.null_stop = 0
    
    def add(self,e):
        self.data[self.null_stop] = e
        self.null_stop += 1
    
    def extend(self,l):
        for e in l.get():
            self.add(e)
    
    def get(self):
        return self.data[:self.null_stop]
    
    def length(self):
        return self.null_stop
    
    def reset(self):
        self.__init__(self.datatype,self.num_elements)
