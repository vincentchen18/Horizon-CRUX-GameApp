import random,copy
def empty_board():
    return [[0] * 4 for _ in range(4)]

def spawn_tile(board):
    empty_indices = []
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:
                empty_indices.append((r, c))
    if not empty_indices:
        return board   # no spawn possible, board full
    r, c = random.choice(empty_indices)
    if random.randint(1, 10) == 10:
        board[r][c] = 4
    else:
        board[r][c] = 2
    return board

def slide_row_left(row):
    # remove all 0s then compress
    newrow = [n for n in row if n != 0]
    merged = []
    skip_next = False
    for i in range(len(newrow)):
        if skip_next:
            skip_next = False
            continue
        if i+1 < len(newrow) and newrow[i] == newrow[i+1]:
            merged.append(newrow[i]*2)
            skip_next = True
        else:
            merged.append(newrow[i])
    while len(merged) < 4:
        merged.append(0)
    return merged

def slide_left(board):
    newboard = copy.deepcopy(board)
    for row in range(4):
        newboard[row] = slide_row_left(newboard[row])
    return newboard

def slide_right(board):
    newboard = copy.deepcopy(board)
    for row in range(4):
        newboard[row] = slide_row_left(newboard[row][::-1])[::-1]
    return newboard

def transpose_board(board):
    newboard = [[0] * 4 for _ in range(4)]
    for y in range(4):
        for x in range(4):
            newboard[x][y] = board[y][x]
    return newboard

def slide_up(board):
    newboard = transpose_board(board)
    newboard = slide_left(newboard)
    return transpose_board(newboard)

def slide_down(board):
    newboard = transpose_board(board)
    newboard = slide_right(newboard)
    return transpose_board(newboard)

def print_board(board):
    horizontal = "+" + "------+" * 4
    print()
    for row in board:
        print(horizontal)
        cells = []
        for num in row:
            if num == 0:
                cells.append("    ")
            else:
                cells.append(f"{num:^4}")
        print("|" + " | ".join(cells) + "|")
    print(horizontal)
    print()

def check_win(board):
    for row in board:
        for cell in row:
            if cell >= 2048:
                return True
    return False

def check_loss(board):
    for row in board:
        if 0 in row:
            return False
    for r in range(4):
        for c in range(4):
            if c+1 < 4 and board[r][c] == board[r][c+1]:
                return False
            if r+1 < 4 and board[r][c] == board[r+1][c]:
                return False
    return True


