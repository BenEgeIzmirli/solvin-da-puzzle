
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
