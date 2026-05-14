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
    # gameloop
    while True:
        if vs_bot:
            if is_bot_turn:
                print("Vinniebot is rolling",end="")
                for i in range(3):
                    time.sleep(0.4)
                    print(".",end="")
                time.sleep(0.4)
                roll = random.randint(1,6)
