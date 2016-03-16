class Tile:
    def __init__(self):
        self.occupied = False
        self.neighbors = None
        self.direction = None
        self.flood_filled = False
        self.coords = None
        self.edge = False
        self.piece_name = None
        self.color = None
