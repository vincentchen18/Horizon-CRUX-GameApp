import random
def is_solved(board):
    return board[0] + board[1] + board[2] + board[3] == [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]

def scramble(board, r, c, depth):
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if depth == 0:
        return board
    while True:
        dir = random.choice(dirs)
        dirs.remove(dir)
        if 0 <= r+dir[0] <= 3 and 0 <= c+dir[1] <= 3:
            board[r][c], board[r+dir[0]][c+dir[1]] = board[r+dir[0]][c+dir[1]], board[r][c]
            return scramble(board, r+dir[0], c+dir[1], depth-1)
