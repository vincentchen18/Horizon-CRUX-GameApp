import tictactoe, puzzle15, pig, nim, lightsout, game2048, connect4, checkers, blackjack, othello

print("Welcome to my Console Gamer!")
def menu():
    print()
    print("+---------------+---------------+---------------+---------------+")
    print("| 1) TicTacToe  | 2) Pig        | 3) Nim        | 4) LightsOut  |")
    print("+---------------+---------------+---------------+---------------+")
    print("| 5) Connect 4  | 6) 15 Puzzle  | 7) 2048       | 8) Checkers   |")
    print("+---------------+---------------+---------------+---------------+")
    print("| 9) Blackjack  | 10) Othello   | 11) RPS       | 12) Poker     |")
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