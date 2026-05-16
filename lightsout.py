import copy, random
def empty_board():
    return [[False for _ in range(5)] for __ in range(5)]

def toggle(board, r, c):
    newboard = copy.deepcopy(board)
    if 0 <= r < 5 and 0 <= c < 5: # in bounds
        newboard[r][c] = not newboard[r][c]
    return newboard

def setclick(board, r, c): # we need to toggle all adjacent cells
    newboard = copy.deepcopy(board)
    newboard = toggle(newboard, r, c)
    newboard = toggle(newboard, r+1, c)
    newboard = toggle(newboard, r-1, c)
    newboard = toggle(newboard, r, c+1)
    newboard = toggle(newboard, r, c-1)
    return newboard

def generate_puzzle(clicks):
    board = empty_board()
    for _ in range(clicks):
        r, c = random.randint(0,4), random.randint(0,4)
        board = setclick(board, r, c)
    return board

def print_board(board):
    print("    1   2   3   4   5")
    for row in range(5):
        letter = "ABCDE"[row]
        cells = []
        for col in range(5):
            cells.append(["○","●"][board[row][col]])
        print(f"{letter}   " + "   ".join(cells))

def check_input(c):
    s = c.strip().upper()
    if len(s) != 2:
        return None
    if s[0] not in "ABCDE":
        return None
    if s[1] not in "12345":
        return None
    r = "ABCDE".index(s[0])
    c = int(s[1]) - 1
    return (r,c)

def is_solved(board):
    return not any(any(row) for row in board)