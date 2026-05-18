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

