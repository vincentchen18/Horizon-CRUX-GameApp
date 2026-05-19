import copy, time

from torchvision.prototype.models import depth


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
def human_move(board, label, player):
    moves = legal_moves(board, player)
    while True:
        raw = input(
            f"{label}, enter your move. "
            "Use space-separated chess coords, e.g. 'e4 d5' for a slide, "
            "or 'g3 e5 c7' for a multi-jump: "
        ).strip().lower()
        if not raw:
            print("No input received, try again.")
            continue
        try:
            path = [parse_square(s) for s in raw.split()]
        except (ValueError, IndexError):
            print("Please enter a valid set of coords like 'e4 d5'.")
            continue
        if len(path) < 2:
            print("A move needs at least a start and an end square.")
            continue
        if path not in moves:
            print("That isn't a legal move. Try again.")
            continue
        return path
# human function
# bot
regular_value = 100
king_value = 175
advanced_value = 5
backrow_value = 20
win_value = 10000000000000000000
def evaluate(board, player): # find the best outcome for player.
    score = 0
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p is None:
                continue
            sign = 1 if color(p) == player else -1
            if p.isupper():
                score += sign * king_value
            else:
                score += sign*regular_value
                advancement = r if p == 'r' else 7-r
                score += sign*advanced_value*advancement
                if (p == 'r' and r == 0) or (p == 'b' and r == 7):
                    score += sign * backrow_value
    return score

def minimax(board, player, depth, alpha, beta, maximising_for):
    winner = game_over(board, player)
    if winner is not None:
        return win_value if winner == maximising_for else -win_value
    if depth == 0:
        return evaluate(board, player)
    moves = legal_moves(board, player)
    moves.sort(key=len, reverse=True) # use the longest capture sequences first
    opponent = 'b' if player == 'r' else 'r'

    if player == maximising_for:
        best = -1*float('inf')
        for m in moves: #test each moveset
            newboard = [row[:] for row in board]
            apply_move(newboard, m)
            val = minimax(newboard, opponent, depth-1, alpha, beta, maximising_for)
            if val > best:
                best = val
            if best > alpha:
                alpha = best
            if beta <= alpha:
                break
        return best
    else:
        best = float('inf')
        for m in moves:
            newboard = [row[:] for row in board]
            apply_move(newboard, m)
            val = minimax(newboard, opponent, depth-1, alpha, beta, maximising_for)
            if val < best:
                best = val
            if beta > best:
                beta = best
            if beta <= alpha:
                break
        return best

def bot_move(board, player, depth=5): # default depth to 5
    moves = legal_moves(board, player)
    if not moves:
        return None
    moves.sort(key=len, reverse=True)
    opponent = 'b' if player == 'r' else 'r'
    best_val = -1 * float('inf')
    for m in moves:
        newboard = [row[:] for row in board]
        apply_move(newboard, m)
        val = minimax(newboard, opponent, depth-1, -1*float('inf'), float('inf'), player)
        if val > best_val:
            best_val = val
            best_move = m
    return best_move
def to_coord(pos):
    r, c = pos
    return f"{chr(ord('a')+c)}{8-r}"

def checkers_play():
    print("=== CHECKERS ===")
    while True:
        c = input('1) Play vs Vinniebot    2) Play vs Human    3) Exit    Please enter 1,2 or 3: ').strip()
        if c == '1':
            vs_bot = True
            break
        elif c == '2':
            vs_bot = False
            break
        elif c == '3':
            return
        print("That's not a valid choice, please enter 1,2 or 3.")

    if vs_bot:
        while True:
            side = input("Play as Red or Blue? Blue moves first. Enter R or B: ").strip().upper()
            if side == "B":
                human_color, bot_color, is_bot_turn = 'b', 'r', False
                break
            elif side == "R":
                human_color, bot_color, is_bot_turn = 'r', 'b', True
                break
            print("That's not a valid choice, please enter R or B.")
    #gameloop
    board = setup()
    current = 'b'
    message = None
    while True:
        print_board(board)
        if message is not None:
            print(message)

        winner = game_over(board, human_color)
        if winner is not None:
            if vs_bot:
                if winner == human_color:
                    print("You win! 🎉")
                else:
                    print("Vinniebot wins! 🤖")
            else:
                name = 'Red' if winner == 'r' else 'Blue'
                print(f'{name} wins! 🎉')
            break
        # no draws in checkers
        if vs_bot and is_bot_turn:
            print("Vinniebot is thinking",end="")
            for i in range(3):
                time.sleep(0.4)
                print(".",end="")
            time.sleep(0.4)
            print()
            move = bot_move(board, bot_color, 5)
            apply_move(board, move)
            message = f"Vinniebot plays {' → '.join(to_coord(m) for m in move)}."
        else:
            if vs_bot:
                label = "You"
            else:
                label = "Red" if current == 'r' else 'Blue'
            move = human_move(board, label, current)
            apply_move(board, move)
            message = None
        #change turn
        current = 'r' if current == 'b' else 'b'
        if vs_bot:
            is_bot_turn = not is_bot_turn

if __name__ == '__main__':
    checkers_play()