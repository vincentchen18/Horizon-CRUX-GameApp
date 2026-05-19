import copy

def setup():
    board = [[None for _ in range(8)] for __ in range(8)]
    for r in range(3):
        for c in range(8):
            if (r+c)%2 == 1:
                board[r][c] = "r"
    for r in range(5, 8):
        for c in range(8):
            if (r+c)%2 == 1:
                board[r][c] = "b"
    return board

def color(piece):
    return None if piece is None else piece.lower()

def in_bounds(r,c):
    return 0 <= r <= 7 and 0 <= c <= 7

def directions(piece):
    if piece == "r":
        return [(1, -1), (1, 1)]
    if piece == "b":
        return [(-1, -1), (-1, 1)]
    if piece in ["R", "B"]:
        return [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    return []

def is_promotion_row(r, piece):
    return (piece == 'r' and r == 7) or (piece == 'b' and r == 0)

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

        if piece in ['r', 'b'] and is_promotion_row(land_r, piece): # no more jumps after promotion
            jumps.append([(r,c), (land_r, land_c)])
            continue

        # apply jump
        newboard = [row[:] for row in board]
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

def legal_moves(board, player): #note: player must be a string "b" or "r"
    jumps = []
    # scan all legal moves, if can jump, only return jumps, cos jumps forced :)))
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece is not None and color(piece) == player:
                jumps.extend(find_jumps(board, r, c))
    if jumps: #force return only the jumps
        return jumps
    # if no jumps, scan and return all legal moves
    moves = []
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece is not None and color(piece) == player:
                moves.extend(find_moves(board, r, c))
    return moves


RED = "\033[31m"
BLUE = "\033[94m"  # bright blue for 'black' pieces — readable on dark terminals
BOLD = "\033[1m"
RESET = "\033[0m"


def colorize(piece):
    if piece is None:
        return ' '
    color = RED if piece.lower() == 'r' else BLUE
    style = BOLD if piece.isupper() else ''  # kings = bold
    return f"{color}{style}{piece}{RESET}"


def print_board(board):
    print("    " + "   ".join("abcdefgh"))
    print("  +" + "---+" * 8)
    for r in range(8):
        cells = [colorize(board[r][c]) for c in range(8)]
        print(f"{8-r} | " + " | ".join(cells) + f" | {8-r}")
        print("  +" + "---+" * 8)
    print("    " + "   ".join("abcdefgh"))

def apply_move(board, path): #path should be list of coords to move
    piece = board[path[0][0]][path[0][1]] # the start coords
    startr, startc = path[0][0], path[0][1]
    for pr, pc in path[1:]:
        board[pr][pc], board[startr][startc] = piece, None
        if abs(startr-pr) == 2: #jump, clear the middle too
            board[(pr+startr)//2][(pc+startc)//2] = None
        startr, startc = pr, pc
    if piece.islower() and is_promotion_row(path[-1][0], piece):
        board[path[-1][0]][path[-1][1]] = piece.upper()

def game_over(board, move_player): #move player needs to be b or r
    if len(legal_moves(board, move_player)) == 0:
        return chr(212-ord(move_player.lower()))
    return None

# still need:
def parse_square(coord): # coord is alphanumeric, such as e4, c5 etc
    return (8-int(coord[1]), ord(coord[0])-ord('a'))
# parse squares: (8 - int(rank), ord(file) - ord('a'))
def human_move(board, label, color):
    while True:
        raw = input(f"{label}, please enter your move(s). Start with your starting coordinate, for example, e4 d5 to move from e4 to d5. If you wish to multicapture, enter the coordinates of all the squares in order space separated: ").strip()
        try:
            path = [parse_square(square) for square in raw.split()]
            if path not in legal_moves(board, color):
                print("That doesn't seem to be a valid path.")
                continue
        except Exception:
            print(f"{label}, please enter a valid coordinate path.")

# human function
# bot