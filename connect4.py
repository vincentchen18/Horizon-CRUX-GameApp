# 7x6 board
winning_lines = [(1,2,3,4),(2,3,4,5),(3,4,5,6),(4,5,6,7),(8,9,10,11),(9,10,11,12),(10,11,12,13),(11,12,13,14),(15,16,17,18),(16,17,18,19),(17,18,19,20),(18,19,20,21),(22,23,24,25),(23,24,25,26),(24,25,26,27),(25,26,27,28),(29,30,31,32),(30,31,32,33),(31,32,33,34),(32,33,34,35),(36,37,38,39),(37,38,39,40),(38,39,40,41),(39,40,41,42), # horizontal winning lines
                     (1,8,15,22),(2,9,16,23),(3,10,17,24),(4,11,18,25),(5,12,19,26),(6,13,20,27),(7,14,21,28),(8,15,22,29),(9,16,23,30),(10,17,24,31),(11,18,25,32),(12,19,26,33),(13,20,27,34),(14,21,28,35),(15,22,29,36),(16,23,30,37),(17,24,31,38),(18,25,32,39),(19,26,33,40),(20,27,34,41),(21,28,35,42), #vertical wins
                     (1,9,17,25),(2,10,18,26),(3,11,19,27),(4,12,20,28),(8,16,24,32),(9,17,25,33),(10,18,26,34),(11,19,27,35),(15,23,31,39),(16,24,32,40),(17,25,33,41),(18,26,34,42), #forward diagonals
                     (4,10,16,22),(5,11,17,23),(6,12,18,24),(7,13,19,25),(11,17,23,29),(12,18,24,30),(13,19,25,31),(14,20,26,32),(18,24,30,36),(19,25,31,37),(20,26,32,38),(21,27,33,39)] #backward diagonals
def connect4_check_win(board):
    for a,b,c,d in winning_lines:
        if board[a-1] == board[b-1] == board[c-1] == board[d-1] and board[a-1] != ' ':
            return board[a-1]
    return None

def connect4_get_drop_cell(board, col):
    # give a column, return which cell the counter is dropped to
    column_cells = [col + 7*r for r in range(6)]
    empties = [x for x in column_cells if board[x] == ' ']
    if not empties:
        return None
    return max(empties)

def connect4_evaluate(board, bot_colour, human_colour):
    # use a heuristic. Higher score is better
    score = 0
    for a,b,c,d in winning_lines:
        window = [board[a-1],board[b-1],board[c-1],board[d-1]]
        bot_count = window.count(bot_colour)
        human_count = window.count(human_colour)
        empty_count = window.count(' ')

        if bot_count == 4: # winning position
            score += 1000
        elif bot_count == 3 and empty_count == 1: #one away
            score += 10
        elif bot_count == 2 and empty_count == 2:
            score += 2

        if human_count == 4: # enemy won
            score -= 1000
        elif human_count == 3 and empty_count == 1:
            score -= 10
        elif human_count == 2 and empty_count == 2:
            score -= 2
    #center column is better for more winning combos so make them weight more
    center_indexes = [3+7*r for r in range(6)]
    for idx in center_indexes:
        if board[idx] == bot_colour:
            score += 6
        elif board[idx] == human_colour:
            score -= 6
    return score

def connect4_minimax(board, depth, is_bot_turn, alpha, beta, bot_colour, human_colour):
    winner = connect4_check_win(board)
    if winner == bot_colour:
        return 100000
    if winner == human_colour:
        return -100000
    if ' ' not in board:
        return 0
    if depth == 0:
        return connect4_evaluate(board, bot_colour, human_colour)

    column_order = [3,2,4,1,5,0,6]
    if is_bot_turn:
        best = -999999
        for col in column_order:
            cell = connect4_get_drop_cell(board, col)
            if cell is None:
                continue
            board[cell] = bot_colour
            score = connect4_minimax(board, depth-1, False, alpha, beta, bot_colour, human_colour)
            board[cell] = ' '
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha: #prune the tree
                break
    else:
        best = 999999
        for col in column_order:
            cell = connect4_get_drop_cell(board, col)
            if cell is None:
                continue
            board[cell] = human_colour
            score = connect4_minimax(board, depth-1, True, alpha, beta, bot_colour, human_colour)
            board[cell] = ' '
            best = min(best, score)
            if beta <= alpha:
                break
    return best

def connect4_botmove(board, bot_colour, human_colour, difficulty): # determine best move by looking a few moves ahead
    best_score, best_column = -999999, None
    column_order = [3,2,4,1,5,0,6]
    for column in column_order:
        cell = connect4_get_drop_cell(board, column)
        if cell is None:
            continue
        board[cell] = bot_colour
        score = connect4_minimax(board, difficulty-1, False, -999999, 999999, bot_colour, human_colour)
        board[cell] = ' '
        if score > best_score:
            best_score, best_column = score, column
    return best_column

def connect4_print_board(board):
    print()
    print(' ' + "   ".join(list(map(str, range(1,8)))))
    for r in range(6):
        print_cells = [board[r*7+c] for c in range(7)]
        print("| " + " | ".join(print_cells) + " |")
    print()

def connect4_humanmove(board, label, color):
    while True:
        a = input(f'{label}, please select a column 1-7: ').strip()
        try:
            a = int(a)
            if a > 7 or a < 1:
                print('Please select a column 1-7.')
                continue
            if connect4_get_drop_cell(board, a) is None:
                print("That column is full!")
                continue
            else:
                return a
        except ValueError:
            print('Please select a column 1-7.')
            continue


def connect4_play():
    #1 - ask to play human or bot
    while True:
        raw = input('1) Play vs Vinniebot    2) Play vs Human    3) Exit    Please enter 1,2 or 3: ').strip()
        if raw == '1':
            vs_bot = True
            break
        elif raw == '2':
            vs_bot = False
            break
        elif raw == '3':
            return
        else:
            print("Please enter 1,2 or 3.")
    board = [' '] * 42
