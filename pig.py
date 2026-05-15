import random, time
def pig_botmove(points, roll_score):
    if roll_score + points >= 100:
        return "BANK"
    if roll_score <= 25:
        return "RISK"
    else:
        return "BANK"

def pig_play():
    print("=== PIG ===")
    while True:
        choice = input("1) Play vs Vinniebot    2) Play vs Human    3) Exit    Please enter 1,2 or 3: ").strip()
        if choice == "1":
            vs_bot = True
            break
        elif choice == "2":
            vs_bot = False
            break
        elif choice == "3":
            return
        else:
            print("Please enter either 1,2 or 3")
    if vs_bot:
        while True:
            choice = input("Go first or second? Enter 1 or 2: ").strip()
            if choice == "1":
                is_bot_turn = False
                botscore = 0
                humanscore = 0
                break
            elif choice == "2":
                is_bot_turn = True
                botscore = 0
                humanscore = 0
                break
            else:
                print("Please enter either 1 or 2.")
    else:
        p1score = 0
        p2score = 0
        current = 0
    running_score = 0
    # gameloop
    while True:
        if vs_bot:
            if botscore >= 100:
                print("Vinniebot wins! 🤖")
            elif humanscore >= 100:
                print("You win! 🎉")
        else:
            if p1score >= 100:
                print("Player 1 wins! 🎉")
            else:
                print("Player 2 wins! 🎉")

        if vs_bot:
            if is_bot_turn:
                print("Vinniebot is rolling",end="")
                for i in range(3):
                    time.sleep(0.4)
                    print(".",end="")
                time.sleep(0.4)
                roll = random.randint(1,6)
                if roll == 1:
                    print(f"Vinniebot rolls {roll}, losing his risked score of {running_score}!")
                    running_score = 0
                    is_bot_turn = False
                    continue
                else:
                    running_score += roll
                    print(f"Vinniebot rolls {roll}, so his running score is now {running_score}!")
                    botaction = pig_botmove(botscore, running_score)
                    print(f"Vinniebot {botaction}S his score of {running_score}.")
                    if botaction == "BANK":
                        botscore += running_score
                        print(f"Vinniebot's score is now {botscore}!")
                        running_score = 0
                        is_bot_turn = False
                        continue
                    else:
                        continue
            else:
                print("Your turn! Press enter to roll.", end="")
                signal = input()
                print("You are rolling",end="")
                for i in range(3):
                    time.sleep(0.4)
                    print(".",end="")
                time.sleep(0.4)

                roll = random.randint(1,6)
                if roll == 1:
                    print(f"You roll a 1, losing your risked score of {running_score}.")
                    running_score = 0
                    is_bot_turn = True
                    continue
                else:
                    running_score += roll
                    while True:

                        action = input(f"You roll a {roll} and your running score is now {running_score}. Risk or bank?").strip().upper()
                        if action not in ["RISK", "BANK"]:
                            print("Please enter either RISK or BANK")
                            continue
                        break
                    if action == "BANK":
                        humanscore += running_score
                        print(f"You banked {running_score}, your score is now {humanscore}!")
                        running_score = 0
                        is_bot_turn = True
                        continue
                    elif action == "RISK":
                        print(f"You risk {running_score}.")
                        continue
        else:
            turn = current % 2
            print(f"Player {turn+1}, please press enter to roll.", end="")
            signal = input()
            print("You are rolling",end="")
            for i in range(3):
                time.sleep(0.4)
                print(".",end="")
            time.sleep(0.4)
            roll = random.randint(1,6)
            if roll == 1:
                print(f"You roll a 1, losing your risked score of {running_score}.")
                running_score = 0
                current += 1
                continue
            else:
                running_score += roll
                while True:
                    action = input(f"You roll a {roll} and your running score is now {running_score}. Risk or bank?").strip().upper()
                    if action not in ["RISK", "BANK"]:
                        print("Please enter either RISK or BANK")
                        continue
                    break
                if action == "BANK":
                    if turn == 0:
                        p1score += running_score
                        print(f"You banked {running_score}, your score is now {p1score}!")
                    else:
                        p2score += running_score
                        print(f"You banked {running_score}, your score is now {p2score}!")
                    running_score = 0
                    current += 1
                    continue
                elif action == "RISK":
                    print(f"You risk {running_score}.")
                    continue


pig_play()