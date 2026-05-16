import random
def empty_board():
    return [[0] * 4 for _ in range(4)]

def spawn_tile(board):
    empty_indices = []
    for y in range(4):
        for x in range(4):
            if board[y][x] == 0:
                empty_indices.append((x, y))
    spawntile = random.choice(empty_indices)
    if random.randint(1,10) == 10:
        board[spawntile[0]][spawntile[1]] = 4
    else:
        board[spawntile[0]][spawntile[1]] = 2
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
            merged.append(newrow[i])
            skip_next = True
        else:
            merged.append(newrow[i])
    while len(merged) < 4:
        merged.append(0)
    return merged

def slide_left(board):
    for row in range(4):
        board[row] = slide_row_left(board[row])
    return board

def slide_right(board):
    for row in range(4):
        board[row] = slide_row_left(board[row][::-1])[::-1]
    return board

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