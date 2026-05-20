import random,copy
def empty_board():
    return [[0] * 4 for _ in range(4)]

# colour
tile_colours = {
    2:    "\033[97m",     # bright white
    4:    "\033[93m",     # bright yellow
    8:    "\033[33m",     # yellow
    16:   "\033[91m",     # bright red
    32:   "\033[31m",     # red
    64:   "\033[95m",     # bright magenta
    128:  "\033[35m",     # magenta
    256:  "\033[96m",     # bright cyan
    512:  "\033[36m",     # cyan
    1024: "\033[92m",     # bright green
    2048: "\033[32m",     # green
}
reset = "\033[0m"

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
    points = 0
    for i in range(len(newrow)):
        if skip_next:
            skip_next = False
            continue
        if i+1 < len(newrow) and newrow[i] == newrow[i+1]:
            merged.append(newrow[i]*2)
            skip_next = True
            points += newrow[i]*2
        else:
            merged.append(newrow[i])
    while len(merged) < 4:
        merged.append(0)
    return merged, points

def slide_left(board):
    newboard = copy.deepcopy(board)
    tp = 0
    for row in range(4):
        newboard[row], p = slide_row_left(newboard[row])
        tp += p
    return newboard, tp

def slide_right(board):
    newboard = copy.deepcopy(board)
    tp = 0
    for row in range(4):
        newboard[row], p = slide_row_left(newboard[row][::-1])
        newboard[row] = newboard[row][::-1]
        tp += p
    return newboard, tp

def transpose_board(board):
    newboard = [[0] * 4 for _ in range(4)]
    for y in range(4):
        for x in range(4):
            newboard[x][y] = board[y][x]
    return newboard

def slide_up(board):
    newboard = transpose_board(board)
    newboard, tp = slide_left(newboard)
    return transpose_board(newboard), tp

def slide_down(board):
    newboard = transpose_board(board)
    newboard,tp = slide_right(newboard)
    return transpose_board(newboard),tp

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
                colour = tile_colours.get(num, "\033[97m")
                cells.append(f"{colour}{num:^4}{reset}")
        print("| " + " | ".join(cells) + " |")
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

def play_2048():
    print("=== 2048 ===")
    while True:
        c = input("1) Play 2048    2) Exit    Please enter 1 or 2: ").strip()
        if c == "1":
            break
        elif c == "2":
            return
        else:
            print("Please enter 1 or 2.")
    board = empty_board()
    board = spawn_tile(board)
    board = spawn_tile(board)
    won_announced = False
    score = 0
    while True:
        print_board(board)
        print(f"Score: {score}")
        if check_win(board) and not won_announced:
            print("You won! 🎉 Keep going or Q to exit.")
            won_announced = True

        if check_loss(board):
            print(f"Game over! No moves left. Final score: {score}")
            return
        while True:
            move = input("Enter a move (WASD) or Q to quit: ").strip().lower()
            if move in ['w','a','s','d','q']:
                before = copy.deepcopy(board)
                if move == 'w':
                    board, p = slide_up(board)
                elif move == 'a':
                    board, p = slide_left(board)
                elif move == 's':
                    board, p = slide_down(board)
                elif move == 'd':
                    board, p = slide_right(board)
                elif move == 'q':
                    print(f"Thank you for playing! Final score: {score}")
                    return
                if board != before:
                    spawn_tile(board)
                    score += p
                    break
                else:
                    print("That move didn't change anything, try a different one.")
                    continue
            print("Please enter a valid move or Q to quit.")

if __name__ == "__main__":
    play_2048()