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
    while True:
        menu()
        print("Enter a number 1-12 for a game, or Q to quit: ", end="")
        choice = input().strip()
        if choice == "Q":
            print("Thanks for playing! :)))")
            return
        try:
            choice = int(choice)
            if choice >= 1 and choice <= 12:
                pass
            else:
                raise ValueError
            if choice == 1:
                tictactoe.tictactoeplay()
            elif choice == 2:
                connect4.connect4_play()
            elif choice == 3:
                pig.pig_play()
            elif choice == 4:
                nim.nimplay()
            elif choice == 5:
                game2048.play_2048()
            elif choice == 6:
                lightsout.lightsout_play()
            elif choice == 7:
                puzzle15.puzzle_play()
            elif choice == 8:
                blackjack.blackjack_play()
            elif choice == 9:
                checkers.checkers_play()
            elif choice == 10:
                othello.othello_play()
            elif choice == 11:
                print("This game is still being built!")
            elif choice == 12:
                print("This game is still being built!")

        except Exception:
            print("That's not a valid input. Please enter a number from 1 - 12.")
main()