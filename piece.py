from tile import *

# this is the class that constructs and contains Pieces.
# Each Piece contains a series of Tiles and a shape in
# which those Tiles are organized. There are twelve Pieces
# and each Piece has a different shape; the names of the
# Pieces are 'boat', 'tie', 'check', 'line', 'v', 'heart',
# 's', 'hexagon', 'mountains', 'fedex', 'nike', and 'weird'.
class Piece:

    # initializes the Piece based on the piece_name it is given.
    def __init__(self,piece_name=None):
        t = []
        if piece_name is None:
            t = None
        elif piece_name is "boat": #7
            self.rotational_symmetry = "none"
            self.mirror_symmetry = True
            for i in range(6):
                t.append(Tile())
            t[0].direction, t[2].direction, t[4].direction = ("down",)*3
            t[1].direction, t[3].direction, t[5].direction = ("up",)*3
            t[0].neighbors = {"-B":t[1]}
            t[1].neighbors = {"B":t[0],"C":t[2]}
            t[2].neighbors = {"-C":t[1],"-B":t[3],"-A":t[5]}
            t[3].neighbors = {"B":t[2],"C":t[4]}
            t[4].neighbors = {"-C":t[3]}
            t[5].neighbors = {"A":t[2]}

        elif piece_name is "tie": #4
            self.rotational_symmetry = "half"
            self.mirror_symmetry = True
            for i in range(6):
                t.append(Tile())
            t[0].direction, t[2].direction, t[3].direction, t[5].direction = ("down",)*4
            t[1].direction, t[4].direction = ("up",)*2
            t[0].neighbors = {"-B":t[1]}
            t[1].neighbors = {"A":t[4],"B":t[0],"C":t[2]}
            t[2].neighbors = {"-C":t[1]}
            t[3].neighbors = {"C":t[4]}
            t[4].neighbors = {"-C":t[3],"-A":t[1],"-B":t[5]}
            t[5].neighbors = {"B":t[4]}

        elif piece_name is "check":  #6
            self.rotational_symmetry = "none"
            self.mirror_symmetry = False
            for i in range(6):
                t.append(Tile())
            t[0].direction, t[2].direction, t[4].direction = ("up",)*3
            t[1].direction, t[3].direction, t[5].direction = ("down",)*3
            t[0].neighbors = {"C":t[1]}
            t[1].neighbors = {"-C":t[0],"-B":t[2]}
            t[2].neighbors = {"B":t[1],"A":t[3]}
            t[3].neighbors = {"-A":t[2],"-C":t[4]}
            t[4].neighbors = {"C":t[3],"A":t[5]}
            t[5].neighbors = {"-A":t[4]}

        elif piece_name is "line":  #white
            self.rotational_symmetry = "half"
            self.mirror_symmetry = True
            for i in range(6):
                t.append(Tile())
            t[0].direction, t[2].direction, t[4].direction = ("up",)*3
            t[1].direction, t[3].direction, t[5].direction = ("down",)*3
            t[0].neighbors = {"C":t[1]}
            t[1].neighbors = {"-C":t[0],"-B":t[2]}
            t[2].neighbors = {"B":t[1],"C":t[3]}
            t[3].neighbors = {"-C":t[2],"-B":t[4]}
            t[4].neighbors = {"B":t[3],"C":t[5]}
            t[5].neighbors = {"-C":t[4]}

        elif piece_name is "v":  #3
            self.rotational_symmetry = "none"
            self.mirror_symmetry = True
            for i in range(6):
                t.append(Tile())
            t[0].direction, t[2].direction, t[4].direction = ("up",)*3
            t[1].direction, t[3].direction, t[5].direction = ("down",)*3
            t[0].neighbors = {"C":t[1]}
            t[1].neighbors = {"-C":t[0],"-A":t[2]}
            t[2].neighbors = {"A":t[1],"C":t[3]}
            t[3].neighbors = {"-C":t[2],"-B":t[4]}
            t[4].neighbors = {"B":t[3],"C":t[5]}
            t[5].neighbors = {"-C":t[4]}

        elif piece_name is "heart":  #9
            self.rotational_symmetry = "none"
            self.mirror_symmetry = True
            for i in range(6):
                t.append(Tile())
            t[0].direction, t[2].direction, t[5].direction = ("up",)*3
            t[1].direction, t[3].direction, t[4].direction = ("down",)*3
            t[0].neighbors = {"C":t[1]}
            t[1].neighbors = {"-C":t[0],"-B":t[2]}
            t[2].neighbors = {"B":t[1],"C":t[3],"A":t[4]}
            t[3].neighbors = {"-C":t[2]}
            t[4].neighbors = {"-A":t[2],"-C":t[5]}
            t[5].neighbors = {"C":t[4]}

        elif piece_name is "s":  #5
            self.rotational_symmetry = "none"
            self.mirror_symmetry = False
            for i in range(6):
                t.append(Tile())
            t[0].direction, t[2].direction, t[4].direction = ("up",)*3
            t[1].direction, t[3].direction, t[5].direction = ("down",)*3
            t[0].neighbors = {"C":t[1]}
            t[1].neighbors = {"-C":t[0],"-B":t[2]}
            t[2].neighbors = {"B":t[1],"A":t[3]}
            t[3].neighbors = {"-A":t[2],"-B":t[4]}
            t[4].neighbors = {"B":t[3],"C":t[5]}
            t[5].neighbors = {"-C":t[4]}

        elif piece_name is "hexagon":  #8
            self.rotational_symmetry = "full"
            self.mirror_symmetry = True
            for i in range(6):
                t.append(Tile())
            t[0].direction, t[2].direction, t[4].direction = ("up",)*3
            t[1].direction, t[3].direction, t[5].direction = ("down",)*3
            t[0].neighbors = {"C":t[1],"A":t[3]}
            t[1].neighbors = {"-C":t[0],"-B":t[2]}
            t[2].neighbors = {"B":t[1],"A":t[5]}
            t[3].neighbors = {"-A":t[0],"-B":t[4]}
            t[4].neighbors = {"B":t[3],"C":t[5]}
            t[5].neighbors = {"-C":t[4],"-A":t[2]}

        elif piece_name is "mountains":  #10
            self.rotational_symmetry = "none"
            self.mirror_symmetry = False
            for i in range(6):
                t.append(Tile())
            t[0].direction, t[2].direction, t[4].direction, t[5].direction = ("up",)*4
            t[1].direction, t[3].direction = ("down",)*2
            t[0].neighbors = {"A":t[1]}
            t[1].neighbors = {"-A":t[0],"-B":t[2]}
            t[2].neighbors = {"B":t[1],"C":t[3]}
            t[3].neighbors = {"-C":t[2],"-B":t[4],"-A":t[5]}
            t[4].neighbors = {"B":t[3]}
            t[5].neighbors = {"A":t[3]}

        elif piece_name is "fedex":  #white
            self.rotational_symmetry = "none"
            self.mirror_symmetry = False
            for i in range(6):
                t.append(Tile())
            t[0].direction, t[3].direction, t[5].direction = ("down",)*3
            t[1].direction, t[2].direction, t[4].direction = ("up",)*3
            t[0].neighbors = {"-B":t[1]}
            t[1].neighbors = {"B":t[0],"A":t[3]}
            t[2].neighbors = {"C":t[3]}
            t[3].neighbors = {"-C":t[2],"-B":t[4],"-A":t[1]}
            t[4].neighbors = {"B":t[3],"C":t[5]}
            t[5].neighbors = {"-C":t[4]}

        elif piece_name is "nike":  #2
            self.rotational_symmetry = "none"
            self.mirror_symmetry = False
            for i in range(6):
                t.append(Tile())
            t[0].direction, t[2].direction, t[4].direction = ("down",)*3
            t[1].direction, t[3].direction, t[5].direction = ("up",)*3
            t[0].neighbors = {"-C":t[1]}
            t[1].neighbors = {"C":t[0],"A":t[2]}
            t[2].neighbors = {"-A":t[1],"-B":t[3]}
            t[3].neighbors = {"B":t[2],"A":t[4]}
            t[4].neighbors = {"-A":t[3],"-B":t[5]}
            t[5].neighbors = {"B":t[4]}

        elif piece_name is "weird":  #1
            self.rotational_symmetry = "none"
            self.mirror_symmetry = False
            for i in range(6):
                t.append(Tile())
            t[0].direction, t[2].direction, t[4].direction, t[5].direction = ("up",)*4
            t[1].direction, t[3].direction = ("down",)*2
            t[0].neighbors = {"C":t[1]}
            t[1].neighbors = {"-C":t[0],"-A":t[2]}
            t[2].neighbors = {"A":t[1],"C":t[3]}
            t[3].neighbors = {"-C":t[2],"-A":t[4],"-B":t[5]}
            t[4].neighbors = {"A":t[3]}
            t[5].neighbors = {"B":t[3]}

        else:
            raise Exception("invalid piece")
        self.piece_name = piece_name
        self.tiles = t
        self.rotate_state = 0
        self.mirror_state = 0

    # cleans the Piece so that its Tiles are no longer primed
    # to be placed in a particular instance of a Board.
    def clean(self):
        for t in self.tiles:
            t.coords = None

    # Each piece has six possible rotations; this function rotates
    # the piece "num" times (once by default).
    def rotate(self,num=1):
        if num==0:
            return
        def cycle(n):
            temp_n = {}
            if "A" in n.keys():
                temp_n["-C"] = n["A"]
            if "B" in n.keys():
                temp_n["-A"] = n["B"]
            if "C" in n.keys():
                temp_n["-B"] = n["C"]
            if "-A" in n.keys():
                temp_n["C"] = n["-A"]
            if "-B" in n.keys():
                temp_n["A"] = n["-B"]
            if "-C" in n.keys():
                temp_n["B"] = n["-C"]
            return temp_n
        for t in self.tiles:
            if t.direction == "up":
                t.direction = "down"
            elif t.direction == "down":
                t.direction = "up"
            t.neighbors = cycle(t.neighbors)
        self.rotate_state += 1
        self.rotate_state = self.rotate_state % 6
        self.rotate(num-1)

    # This function gets all possible transfigurations of
    # the Piece - rotations and mirror images.
    def rotations(self):
        def get_rotation_range():
            if self.rotational_symmetry is "none":
                return range(6)
            if self.rotational_symmetry is "half":
                return range(3)
            if self.rotational_symmetry is "full":
                return range(1)
        def reset_rotations():
            while self.rotate_state != 0:
                self.rotate()
        def reset_mirrors():
            while self.mirror_state != 0:
                self.mirror()

        reset_mirrors()
        reset_rotations()
        for r in get_rotation_range():
            yield self
            self.rotate()
        reset_rotations()

        if not self.mirror_symmetry:
            self.mirror()
            for r in get_rotation_range():
                yield self
                self.rotate()
            reset_rotations()
            reset_mirrors()

    # this function mirror image flips the Piece.
    def mirror(self):
        for t in self.tiles:
            temp_n = {}
            if "B" in t.neighbors:
                temp_n["C"] = t.neighbors["B"]
            if "C" in t.neighbors:
                temp_n["B"] = t.neighbors["C"]
            if "-B" in t.neighbors:
                temp_n["-C"] = t.neighbors["-B"]
            if "-C" in t.neighbors:
                temp_n["-B"] = t.neighbors["-C"]
            if "A" in t.neighbors:
                temp_n["A"] = t.neighbors["A"]
            if "-A" in t.neighbors:
                temp_n["-A"] = t.neighbors["-A"]
            t.neighbors = temp_n
        self.mirror_state += 1
        self.mirror_state = self.mirror_state % 2








