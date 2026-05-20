symbols = {'B': '●', 'W': '○', None: ' '}
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
    if in_bounds(newr, newc) and board[newr][newc] == opponent:
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
        board[fr][c] = player

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
