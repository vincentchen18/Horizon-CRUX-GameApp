# 7x6 board
def connect4_check_win(board):
    winning_lines = [(1,2,3,4),(2,3,4,5),(3,4,5,6),(4,5,6,7),(8,9,10,11),(9,10,11,12),(10,11,12,13),(11,12,13,14),(15,16,17,18),(16,17,18,19),(17,18,19,20),(18,19,20,21),(22,23,24,25),(23,24,25,26),(24,25,26,27),(25,26,27,28),(29,30,31,32),(30,31,32,33),(31,32,33,34),(32,33,34,35),(36,37,38,39),(37,38,39,40),(38,39,40,41),(39,40,41,42), # horizontal winning lines
                     (1,8,15,22),(2,9,16,23),(3,10,17,24),(4,11,18,25),(5,12,19,26),(6,13,20,27),(7,14,21,28),(8,15,22,29),(9,16,23,30),(10,17,24,31),(11,18,25,32),(12,19,26,33),(13,20,27,34),(14,21,28,35),(15,22,29,36),(16,23,30,37),(17,24,31,38),(18,25,32,39),(19,26,33,40),(20,27,34,41),(21,28,35,42), #vertical wins
                     (1,9,17,25),(2,10,18,26),(3,11,19,27),(4,12,20,28),(8,16,24,32),(9,17,25,33),(10,18,26,34),(11,19,27,35),(15,23,31,39),(16,24,32,40),(17,25,33,41),(18,26,34,42), #forward diagonals
                     (4,10,16,22),(5,11,17,23),(6,12,18,24),(7,13,19,25),(11,17,23,29),(12,18,24,30),(13,19,25,31),(14,20,26,32),(18,24,30,36),(19,25,31,37),(20,26,32,38),(21,27,33,39)] #backward diagonals
    for a,b,c,d in winning_lines:
        if board[a-1] == board[b-1] == board[c-1] == board[d-1] and board[a-1] != ' ':
            return board[a-1]
        return None

def connect4_minimax(board, is_bot_turn, bot_color, human_color):
    winner = connect4_check_win(board)
    if winner == bot_color:
        return 1
    if winner == human_color:
        return -1
    if ' ' not in board:
        return 0

    if is_bot_turn:
        best = -999
        for i in range(7):
            movecell = max([x for x in range(i, i+36, 7) if board[x] == ' '])
            board[movecell] = bot_color
            score = connect4_minimax(board, False, bot_color, human_color)
            board[movecell] = ' '
            if score > best:
                best = score
    else:
        best = 999
        for i in range(7):
            movecell = max([x for x in range(i, i+36, 7) if board[x] == ' '])
            board[movecell] = human_color
            score = connect4_minimax(board, True, bot_color, human_color)
            board[movecell] = ' '
            if score < best:
                best = score
    return best

def bot_move(board, bot_color, human_color):
    best_score, best_pos = -999, None
    for i in range(7):
        movecell = max([x for x in range(i, i+36, 7) if board[x] == ' '])
