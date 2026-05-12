import time
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

def print_board(board):
    print('   1   2   3')
    print("A  " + " | ".join(board[:3]) + " ")
    print("  ---+---+---")
    print("B  " + " | ".join(board[3:6]) + " ")
    print("  ---+---+---")
    print("C  " + " | ".join(board[6:]) + " ")

def tictactoeplay():
    print("=== TIC TAC TOE ===")
    while True: # game loop
        mode = input("1) Play vs Vinniebot      2) Play vs Human    3) Exit     Pick 1, 2 or 3: ")
        if mode == '1':
            vs_bot = True
            break
        elif mode == '2':
            vs_bot = False
            break
        elif mode == '3':
            return
        else:
            print("Please enter either 1, 2 or 3.")
    if vs_bot:
        print("You selected: Play vs Vinniebot")
        while True:
            choice = input("Play as X or O (X goes first): ").upper()
            if choice == 'X':
                human_symbol = 'X'
                bot_symbol = 'O'
                break
            elif choice == 'O':
                human_symbol = 'O'
                bot_symbol = 'X'
                break
            print("Please enter either X or O.")
    else:
        #human vs human
        human_symbol = None
        bot_symbol = None

    board = [' '] * 9 # initialise empty
    current = 'X'
    #game loop
    while True:
        print_board(board)

        if vs_bot and current == bot_symbol: # vinniebot's turn
            print('Vinniebot is thinking', end="")
            time.sleep(0.4)
            print(".", end="")
            time.sleep(0.4)
            print(".", end="")
            time.sleep(0.4)
            print(".")
            time.sleep(0.4)
            move = bot_move(board, bot_symbol, human_symbol)
            board[move] = bot_symbol
        else:
            # human turn
            coord = input(f'Player {current}, please enter a cell to move (e.g. A1, B3, etc): ').strip().upper()
            if len(coord) != 2 or coord[0] not in ['A','B','C'] or coord[1] not in ['1','2','3']:
                print("Please enter a valid coordinate from A1 to C3.")
                continue
            row = 'ABC'.index(coord[0])
            col = '123'.index(coord[1])
            move = row*3 + col
            if board[move] != " ":
                print(f"There is already a {board[move]} there. Try again.")
                continue
            board[move] = current
        winner = check_winner(board)
        if winner is not None:
            print_board(board)
            if vs_bot:
                if winner == bot_symbol:
                    print('Vinniebot wins! 🤖')
                else:
                    print("You win! 🎉 ") # <--- this output should be impossible to obtain if i coded this right lol
            else:
                print(f'Player {winner} wins! 🎉 ')
            return
        if ' ' not in board:
            print_board(board)
            print("It's a draw!")
            return

        # if no one wins, and the game is still going:
        current = "X" if current == "O" else "O"

if __name__ == '__main__': # local testing
    tictactoeplay()

# completed