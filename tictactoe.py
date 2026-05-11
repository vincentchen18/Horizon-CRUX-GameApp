def check_winner(board):
    lines = [(0,1,2),(3,4,5),(6,7,8),    # rows
             (0,3,6),(1,4,7),(2,5,8),    # columns
             (0,4,8),(2,4,6)]             # diagonals
    for a,b,c in lines:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    return None
## minimax algo is for the bot. If human vs human, separate function for winchecking.
def minimax(board, is_bot_turn, bot_symbol, human_symbol):
    w = check_winner(board)
    if w == bot_symbol:
        return 1
    if w == human_symbol:
        return -1
    if ' ' not in board:
        return 0

    if is_bot_turn:
        best = -999
        for i in range(9):
            if board[i] == ' ':
                board[i] = bot_symbol
                score = minimax(board, False, bot_symbol, human_symbol)
                board[i] = ' '
                best = max(best, score)
        return best
    else:
        best = 999
        for i in range(9):
            if board[i] == ' ':
                board[i] = human_symbol
                score = minimax(board, True, bot_symbol, human_symbol)
                board[i] = ' '
                best = min(best, score)
        return best
# bot movements
def bot_move(board, bot_symbol, human_symbol):
    best_score, best_pos = -999, None
    for i in range(9):
        if board[i] == ' ':
            board[i] = bot_symbol
            score = minimax(board, False, bot_symbol, human_symbol)
            board[i] = ' '
            if score > best_score:
                best_score, best_pos = score, i
    return best_pos