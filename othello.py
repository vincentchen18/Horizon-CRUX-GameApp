symbols = {'B': '●', 'W': '○', None: ' '}
import time
def setup():
    newboard = [[None for _ in range(8)] for __ in range(8)]
    # put 2 piece of each color in the middle.
    newboard[3][3] = "W"
    newboard[3][4] = "B"
    newboard[4][4] = "W"
    newboard[4][3] = "B"
    return newboard

dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def flips_in_direction(board, r, c, dr, dc, player): #check how many flips if we place a counter in direction dr, dc
    opponent = 'W' if player == 'B' else 'B'
    captures = []
    newr, newc = r+dr, c+dc
    while in_bounds(newr, newc) and board[newr][newc] == opponent:
        captures.append((newr, newc))
        newr += dr
        newc += dc
    if in_bounds(newr, newc) and board[newr][newc] == player and captures:
        return captures
    return []

def all_possible_flips(board, r, c, player): # calculate all captures if we place a piece at (r, c).
    if board[r][c] is not None: # cell occupied :((
        return []
    flips = []
    for dr, dc in dirs:
        flips.extend(flips_in_direction(board, r, c, dr, dc, player))
    return flips

def legal_moves(board, player):
    moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] is None and all_possible_flips(board, r, c, player):
                moves.append((r, c))
    return moves

# actual movement

def apply_move(board, move, player): # move is tuple, player is B or W
    r,c = move
    flips = all_possible_flips(board, r, c, player)
    board[r][c] = player
    for fr, fc in flips:
        board[fr][fc] = player

def game_over(board): # if no move, pass, if both side no move, game over
    if not legal_moves(board, 'B') and not legal_moves(board, 'W'):
        b_count = sum([row.count('B') for row in board])
        w_count = sum([row.count('W') for row in board])
        if b_count > w_count:
            return "B" #black win
        elif w_count > b_count:
            return "W" #white win
        return "D" #draw
    return None # game not over

def to_coord(pos):
    r, c = pos
    return f"{chr(ord('a')+c)}{8-r}"

def parse_square(coord): # coord is alphanumeric, such as e4, c5 etc
    return (8-int(coord[1]), ord(coord[0])-ord('a'))

def human_move(board, label, player):
    moves = legal_moves(board, player)
    move_strs = ", ".join(to_coord(m) for m in moves)
    print(f"{label}, your legal moves are: {move_strs}")
    while True:
        raw = input("Enter a square (e.g. d4) to place: ").strip().lower()
        try:
            move = parse_square(raw)
        except Exception:
            print("That doesn't seem to be a valid move. Please enter a coordinate properly.")
            continue
        if move not in moves:
            print("That's not a legal move! Try again.")
            continue
        return move

#bot
corner = 100
corner_diag = -40
adj_corner = -20
edge = 10
piece = 1
mobility = 5

position_weights = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [10, -5, 1, 1, 1, 1, -5, 10],
    [5, -5, 1, 1, 1, 1, -5, 5],
    [5, -5, 1, 1, 1, 1, -5, 5],
    [10, -5, 1, 1, 1, 1, -5, 10],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [100, -20, 10, 5, 5, 10, -20, 100]
]

def evaluate(board, maximising_for):
    score = 0
    opponent = 'W' if maximising_for == 'B' else 'B'
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p is None:
                continue
            sign = 1 if p == maximising_for else -1
            score += sign*position_weights[r][c]
    score += mobility * (len(legal_moves(board, maximising_for)) - len(legal_moves(board, opponent)))
    return score

def minimax(board, player, depth, alpha, beta, maximising_for):
    winner = game_over(board)
    if winner is not None:
        if winner == maximising_for:
            return float('inf')
        elif winner == "D":
            return 0
        else:
            return -1*float('inf')
    if depth == 0:
        return evaluate(board, maximising_for)
    moves = legal_moves(board, player)
    opponent = 'W' if player == 'B' else 'B'
    if not moves:
        return minimax(board, opponent, depth, alpha, beta, maximising_for)

    moves.sort(key=lambda m: position_weights[m[0]][m[1]], reverse=True)

    if player == maximising_for:
        best = -1*float('inf')
        for move in moves:
            newboard = [row[:] for row in board]
            apply_move(newboard, move, player)
            val = minimax(newboard, opponent, depth-1, alpha, beta, maximising_for)
            best = max(best, val)
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best
    else:
        best = float('inf')
        for move in moves:
            newboard = [row[:] for row in board]
            apply_move(newboard, move, player)
            val = minimax(newboard, opponent, depth-1, alpha, beta, maximising_for)
            best = min(best, val)
            beta = min(beta, best)
            if alpha >= beta:
                break
        return best

def bot_move(board, player, depth):
    moves = legal_moves(board, player)
    if not moves:
        return None
    moves.sort(key=lambda m: position_weights[m[0]][m[1]], reverse=True)
    opponent = "W" if player == 'B' else 'B'
    best_val = -1*float('inf')
    best_move = moves[0]
    for move in moves:
        newboard = [row[:] for row in board]
        apply_move(newboard, move, player)
        val = minimax(newboard, opponent, depth-1, -1*float('inf'), float('inf'), player)
        if val > best_val:
            best_val = val
            best_move = move
    return best_move

def print_board(board):
    print("    " + "   ".join("abcdefgh"))
    print("  +" + "---+" * 8)
    for r in range(8):
        cells = [symbols[i] for i in board[r]]
        print(f"{8 - r} | " + " | ".join(cells) + f" | {8 - r}")
        print("  +" + "---+" * 8)
    print("    " + "   ".join("abcdefgh"))

def othello_play():
    print("=== OTHELLO / REVERSI ===")
    while True:
        c = input("1) Play vs bot    2) Play vs Human    3) Exit    Please enter 1, 2 or 3: ").strip()
        if c == "1":
            vs_bot = True
            break
        elif c == "2":
            vs_bot = False
            break
        else:
            print("That's not a valid choice, please enter 1, 2 or 3.")
    if vs_bot:
        while True:
            raw = input("Play as Black or White? Black moves first. Enter B/W: ").strip().upper()
            if raw == "B":
                human_colour = "B"
                bot_colour = "W"
                is_bot_turn = False
                break
            elif raw == "W":
                human_colour = "W"
                bot_colour = "B"
                is_bot_turn = True
                break
            else:
                print("That's not a valid choice, please enter B/W.")
    board = setup()
    current = 'B'
    message = None
    while True:
        winner = game_over(board)
        if winner is not None:
            print_board(board)
            b_count, w_count = sum([row.count("B") for row in board]), sum([row.count("W") for row in board])
            print(f"Final scores, Black: {b_count}, White: {w_count}")
            if vs_bot:
                if winner == "D":
                    print("It's a draw!")
                elif winner == bot_colour:
                    print("Vinniebot wins! 🤖")
                elif winner == human_colour:
                    print("You win! 🎉")
            else:
                if winner == "D":
                    print("It's a draw!")
                else:
                    label = "Black" if winner == "B" else "White"
                    print(f"{label} wins!")
            return
        moves = legal_moves(board, current)
        if not moves:
            label = "Black" if winner == "B" else "White"
            print_board(board)
            print(f"{label} has no legal moves and must pass.")
            current = "W" if current == "B" else "B"
            if vs_bot:
                is_bot_turn = not is_bot_turn
            continue
        if vs_bot and is_bot_turn:
            print_board(board)
            if message is not None:
                print(message)
            print("Vinniebot is thinking", end="")
            for i in range(3):
                time.sleep(0.4)
                print(".", end="")
            time.sleep(0.4)
            print()
            move = bot_move(board, current, 5)
            apply_move(board, move, current)
            message = f"Vinniebot plays {to_coord(move)}"
        else:
            print_board(board)
            if message is not None:
                print(message)
            label = "You" if vs_bot else "Black" if current == "B" else "White"
            move = human_move(board, label, current)
            apply_move(board, move, current)
            message = None
        current = "W" if current == "B" else "B"
        if vs_bot:
            is_bot_turn = not is_bot_turn

if __name__ == "__main__":
    othello_play()