import random, copy
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

def move(attempt, board):
    for r in range(4):
        if 0 in board[r]:
            r, c = r, board[r].index(0)
            break
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for x, y in dirs:
        if 0 <= r+x <= 3 and 0 <= c+y <= 3:
            if board[r+x][c+y] == attempt:
                board[r+x][c+y], board[r][c] = board[r][c], board[r+x][c+y]
                return board
    return None

def print_board(board):
    h = "+----+----+----+----+"
    print()
    print(h)
    for row in board:
        cells = []
        for num in row:
            if num == 0:
                cells.append("  ")
            else:
                cells.append(f"{num:>2}")
        print("| " + " | ".join(cells) + " |")
        print(h)
    print()


def puzzle_play():
    print("=== 15 PUZZLE ===")
    while True:
        c = input("1) Play 15 Puzzle    2) Exit    Please enter 1 or 2: ").strip()
        if c == "1":
            break
        elif c == "2":
            return
        else:
            print("That's not a valid choice, please enter 1 or 2.")
    puzzle = scramble([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]], 3, 3, 100)
    while True:
        print_board(puzzle)
        m = input("Please enter the number of the square you'd like to slide into the empty slot or Q to quit: ").strip().upper()
        if m == "Q":
            return
        try:
            att = int(m)
            b = move(att, puzzle)
            if b is None:
                print("That's not next to the empty slot, please enter a valid number or Q to quit.")
                continue
            puzzle = copy.deepcopy(b)
        except ValueError:
            print("That's not a valid choice, please enter a number 1-15 or Q to quit.")
        if is_solved(puzzle):
            print("Congrats, you solved the puzzle! 🎉")

if __name__ == "__main__":
    puzzle_play()