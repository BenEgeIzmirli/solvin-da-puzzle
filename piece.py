from tile import *
from board import Board
from random import random

colorDict={'r':(1,0,0), 'g':(0,1,0), 'b':(0,0,1), 'w':(1,1,1), 'o':(1,0.5,0), 'y':(1,1,0)}

class Piece:
    def __init__(self,seed=None):
        t = []
        if seed is None:
            self.tiles = None
            self.piece_name = None
            self.rotate_state = 0
            self.mirror_state = 0
            self.rotational_symmetry = None
            self.mirror_symmetry = None
        elif type(seed) == str:
            if seed is "boat": #7
                for i in range(6):
                    t.append(Tile())
                    t[i].color = colorDict['o']
                t[0].direction, t[2].direction, t[4].direction = ("down",)*3
                t[1].direction, t[3].direction, t[5].direction = ("up",)*3
                t[0].neighbors = {"-B":t[1]}
                t[1].neighbors = {"B":t[0],"C":t[2]}
                t[2].neighbors = {"-C":t[1],"-B":t[3],"-A":t[5]}
                t[3].neighbors = {"B":t[2],"C":t[4]}
                t[4].neighbors = {"-C":t[3]}
                t[5].neighbors = {"A":t[2]}

            elif seed is "tie": #4
                for i in range(6):
                    t.append(Tile())
                    t[i].color = colorDict['o']
                t[0].direction, t[2].direction, t[3].direction, t[5].direction = ("down",)*4
                t[1].direction, t[4].direction = ("up",)*2
                t[0].neighbors = {"-B":t[1]}
                t[1].neighbors = {"A":t[4],"B":t[0],"C":t[2]}
                t[2].neighbors = {"-C":t[1]}
                t[3].neighbors = {"C":t[4]}
                t[4].neighbors = {"-C":t[3],"-A":t[1],"-B":t[5]}
                t[5].neighbors = {"B":t[4]}

            elif seed is "check":  #6
                for i in range(6):
                    t.append(Tile())
                    t[i].color = colorDict['g']
                t[0].direction, t[2].direction, t[4].direction = ("up",)*3
                t[1].direction, t[3].direction, t[5].direction = ("down",)*3
                t[0].neighbors = {"C":t[1]}
                t[1].neighbors = {"-C":t[0],"-B":t[2]}
                t[2].neighbors = {"B":t[1],"A":t[3]}
                t[3].neighbors = {"-A":t[2],"-C":t[4]}
                t[4].neighbors = {"C":t[3],"A":t[5]}
                t[5].neighbors = {"-A":t[4]}

            elif seed is "line":  #white
                for i in range(6):
                    t.append(Tile())
                    t[i].color = colorDict['g']
                t[0].direction, t[2].direction, t[4].direction = ("up",)*3
                t[1].direction, t[3].direction, t[5].direction = ("down",)*3
                t[0].neighbors = {"C":t[1]}
                t[1].neighbors = {"-C":t[0],"-B":t[2]}
                t[2].neighbors = {"B":t[1],"C":t[3]}
                t[3].neighbors = {"-C":t[2],"-B":t[4]}
                t[4].neighbors = {"B":t[3],"C":t[5]}
                t[5].neighbors = {"-C":t[4]}

            elif seed is "v":  #3
                for i in range(6):
                    t.append(Tile())
                    t[i].color = colorDict['g']
                t[0].direction, t[2].direction, t[4].direction = ("up",)*3
                t[1].direction, t[3].direction, t[5].direction = ("down",)*3
                t[0].neighbors = {"C":t[1]}
                t[1].neighbors = {"-C":t[0],"-A":t[2]}
                t[2].neighbors = {"A":t[1],"C":t[3]}
                t[3].neighbors = {"-C":t[2],"-B":t[4]}
                t[4].neighbors = {"B":t[3],"C":t[5]}
                t[5].neighbors = {"-C":t[4]}

            elif seed is "heart":  #9
                for i in range(6):
                    t.append(Tile())
                    t[i].color = colorDict['g']
                t[0].direction, t[2].direction, t[5].direction = ("up",)*3
                t[1].direction, t[3].direction, t[4].direction = ("down",)*3
                t[0].neighbors = {"C":t[1]}
                t[1].neighbors = {"-C":t[0],"-B":t[2]}
                t[2].neighbors = {"B":t[1],"C":t[3],"A":t[4]}
                t[3].neighbors = {"-C":t[2]}
                t[4].neighbors = {"-A":t[2],"-C":t[5]}
                t[5].neighbors = {"C":t[4]}

            elif seed is "s":  #5
                for i in range(6):
                    t.append(Tile())
                    t[i].color = colorDict['g']
                t[0].direction, t[2].direction, t[4].direction = ("up",)*3
                t[1].direction, t[3].direction, t[5].direction = ("down",)*3
                t[0].neighbors = {"C":t[1]}
                t[1].neighbors = {"-C":t[0],"-B":t[2]}
                t[2].neighbors = {"B":t[1],"A":t[3]}
                t[3].neighbors = {"-A":t[2],"-B":t[4]}
                t[4].neighbors = {"B":t[3],"C":t[5]}
                t[5].neighbors = {"-C":t[4]}

            elif seed is "hexagon":  #8
                for i in range(6):
                    t.append(Tile())
                    t[i].color = colorDict['g']
                t[0].direction, t[2].direction, t[4].direction = ("up",)*3
                t[1].direction, t[3].direction, t[5].direction = ("down",)*3
                t[0].neighbors = {"C":t[1],"A":t[3]}
                t[1].neighbors = {"-C":t[0],"-B":t[2]}
                t[2].neighbors = {"B":t[1],"A":t[5]}
                t[3].neighbors = {"-A":t[0],"-B":t[4]}
                t[4].neighbors = {"B":t[3],"C":t[5]}
                t[5].neighbors = {"-C":t[4],"-A":t[2]}

            elif seed is "mountains":  #10
                for i in range(6):
                    t.append(Tile())
                    t[i].color = colorDict['g']
                t[0].direction, t[2].direction, t[4].direction, t[5].direction = ("up",)*4
                t[1].direction, t[3].direction = ("down",)*2
                t[0].neighbors = {"A":t[1]}
                t[1].neighbors = {"-A":t[0],"-B":t[2]}
                t[2].neighbors = {"B":t[1],"C":t[3]}
                t[3].neighbors = {"-C":t[2],"-B":t[4],"-A":t[5]}
                t[4].neighbors = {"B":t[3]}
                t[5].neighbors = {"A":t[3]}

            elif seed is "fedex":  #white
                for i in range(6):
                    t.append(Tile())
                    t[i].color = colorDict['g']
                t[0].direction, t[3].direction, t[5].direction = ("down",)*3
                t[1].direction, t[2].direction, t[4].direction = ("up",)*3
                t[0].neighbors = {"-B":t[1]}
                t[1].neighbors = {"B":t[0],"A":t[3]}
                t[2].neighbors = {"C":t[3]}
                t[3].neighbors = {"-C":t[2],"-B":t[4],"-A":t[1]}
                t[4].neighbors = {"B":t[3],"C":t[5]}
                t[5].neighbors = {"-C":t[4]}

            elif seed is "nike":  #2
                for i in range(6):
                    t.append(Tile())
                    t[i].color = colorDict['g']
                t[0].direction, t[2].direction, t[4].direction = ("down",)*3
                t[1].direction, t[3].direction, t[5].direction = ("up",)*3
                t[0].neighbors = {"-C":t[1]}
                t[1].neighbors = {"C":t[0],"A":t[2]}
                t[2].neighbors = {"-A":t[1],"-B":t[3]}
                t[3].neighbors = {"B":t[2],"A":t[4]}
                t[4].neighbors = {"-A":t[3],"-B":t[5]}
                t[5].neighbors = {"B":t[4]}

            elif seed is "weird":  #1
                for i in range(6):
                    t.append(Tile())
                    t[i].color = colorDict['g']
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
            self.piece_name = seed
            self.tiles = t
            self.rotate_state = 0
            self.mirror_state = 0
            self.rotational_symmetry = self.find_rotational_symmetry()
            self.mirror_symmetry = self.find_mirror_symmetry()
        elif type(seed) == type(Board()):
            raise NotImplementedError("haven't done this yet lel")
#            t = []
#            occupied = [t for t in seed.occupied()]
#            for otile in occupied:
#                t.append(Tile())
#                t[i].color = (random(),random(),random())
#            for otile in occupied:
#                
#            self.piece_name = self.to_string()
#            self.tiles = t
#            self.rotate_state = 0
#            self.mirror_state = 0
#            self.rotational_symmetry = self.find_rotational_symmetry()
#            self.mirror_symmetry = self.find_mirror_symmetry()
        else:
            raise TypeException("seed passed to Piece constructor must be either a string or a Board.")
            
    
    def clean(self):
        for t in self.tiles:
            t.coords = None
    
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
    
    def to_string(self):
        b = Board()
        for t in b.unoccupied():
            if b.place(self,t.coords):
                return b.to_string()
    
    def __hash__(self):
        return self.to_string()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    
    def find_rotational_symmetry(self):
        unique_strings = []
        for i in range(6):
            this_unique_string = self.to_string()
            if this_unique_string in unique_strings:
                self.reset_rotations()
                return i
            unique_strings.append(this_unique_string)
            self.rotate()
        self.reset_rotations()
        return 6
        
    def find_mirror_symmetry(self):
        unique_string = self.to_string()
        self.mirror()
        if self.to_string() == unique_string:
            self.reset_mirrors()
            return True
        else:
            self.reset_mirrors()
            return False
    
    def reset_rotations(self):
        while self.rotate_state != 0:
            self.rotate()
    
    def reset_mirrors(self):
        while self.mirror_state != 0:
            self.mirror()
    
    def rotations(self):
        self.reset_mirrors()
        self.reset_rotations()
        for r in range(self.rotational_symmetry):
            yield self
            self.rotate()
        self.reset_rotations()
        
        if not self.mirror_symmetry:
            self.mirror()
            for r in range(self.rotational_symmetry):
                yield self
                self.rotate()
            self.reset_rotations()
            self.reset_mirrors()
    
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








