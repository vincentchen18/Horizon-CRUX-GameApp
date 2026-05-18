import copy
def setup():
    board = [[None for _ in range(8)] for __ in range(8)]
    for r in range(3):
        for c in range(8):
            if (r+c)%2 == 1:
                board[r][c] = "b"
    for r in range(5, 8):
        for c in range(8):
            if (r+c)%2 == 1:
                board[r][c] = "w"
    return board

def color(piece):
    return None if piece is None else piece.lower()

def in_bounds(r,c):
    return 0 <= r <= 7 and 0 <= c <= 7

def directions(piece):
    if piece == "b":
        return [(1, -1), (1, 1)]
    if piece == "w":
        return [(-1, -1), (-1, 1)]
    if piece in ["B", "W"]:
        return [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    return []

def is_promotion_row(r, piece):
    return (piece == 'b' and r == 7) or (piece == 'w' and r == 0)

def find_jumps(board, r, c, piece=None):
    # return paths
    if piece is None:
        piece = board[r][c]
    if piece is None:
        return [] # no jumps cos no unit
    owner = color(piece)

    jumps = []
    for dr, dc in directions(piece):
        over_r, over_c = r+dr, c+dc
        land_r, land_c = r+2*dr, c+2*dc
        # failcases
        if not in_bounds(land_r, land_c):
            continue
        mid = board[over_r][over_c]
        if mid is None or color(mid) == owner: # cant jump
            continue
        if board[land_r][land_c] is not None: # jump onto occupied square
            continue

        if piece in ['b', 'w'] and is_promotion_row(land_r, land_c): # no more jumps after promotion
            jumps.append([(r,c), (land_r, land_c)])

        # apply jump
        newboard = copy.deepcopy(board)
        newboard[r][c] = None
        newboard[over_r][over_c] = None
        newboard[land_r][land_c] = piece

        continuations = find_jumps(newboard, land_r, land_c, piece)
        if continuations:
            for continuation in continuations:
                jumps.append([(r,c)] + continuation)
        else:
            jumps.append([(r, c), (land_r, land_c)])
    return jumps

def find_moves(board, r, c):
    piece = board[r][c]
    if piece is None:
        return []
    moves = []
    for dr, dc in directions(piece):
        new_r, new_c = r+dr, c+dc
        if in_bounds(new_r, new_c) and board[new_r][new_c] is None:
            moves.append([(r,c), (new_r, new_c)])
    return moves
