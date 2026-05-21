import tictactoe, puzzle15, pig, nim, lightsout, game2048, connect4, checkers, blackjack, othello

print("Welcome to my Console Gamer!")
def menu():
    print()
    print("+---------------+---------------+---------------+---------------+")
    print("| 1) TicTacToe  | 2) Connect 4  | 3) Pig        | 4) Nim        |")
    print("+---------------+---------------+---------------+---------------+")
    print("| 5) 2048       | 6) Lights Out | 7) 15 Puzzle  | 8) Blackjack  |")
    print("+---------------+---------------+---------------+---------------+")
    print("| 9) Checkers   | 10) Othello   | 11) RPS       | 12) Poker     |")
    print("+---------------+---------------+---------------+---------------+")
    print()

def main():
    menu()
    while True:
        print("Enter a number 1-16 for a game: ").strip()
        choice = input()
        try:
            choice = int(choice)
            if choice >= 1 and choice <= 16:
                pass
            else:
                raise ValueError
            if choice == 1:
                tictactoe.tictactoeplay()
        except Exception:
            print("")