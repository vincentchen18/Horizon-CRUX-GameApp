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