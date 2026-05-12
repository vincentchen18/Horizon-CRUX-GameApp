import random, time
def nim_setup(pile_num):
    return [random.randint(1,20) for i in range(pile_num)]

def print_piles(pile_num):
    print()
    for index, number in enumerate(pile_num):
        print(f"  Pile {index+1}: {'●' * number} ({number})")
    print()

def nimbot(piles):
    # computer optimal move
    default = 0
    for i in range(len(piles)):
        default ^= piles[i]
    if default == 0:
        a = piles.index(max(piles))
        piles[a] -= 1
        if piles[a] == 0:
            piles.pop(a)
        return a, 1
    for i in range(len(piles)):
        target = piles[i] ^ default
        if target < piles[i]:
            amount = piles[i] - target
            piles[i] = target
            return i, amount
    return 0,0

def nim_humanmove(piles, player_label):
    while True:
        raw = input(f"{player_label}, please enter pile and amount (e.g. 2 3 means take 3 from the 2nd pile): ")
        parts = raw.replace(',',' ').split()
        if len(parts) != 2:
            print("Please enter pile and amount as numbers correctly.")
            continue
        try:
            pile_index = int(parts[0])-1
            amount = int(parts[1])
        except ValueError:
            print("Please enter numbers")
            continue
        if pile_index < 0 or pile_index >= len(piles):
            print(f"Pile must be between 1 and {len(piles)}")
            continue
        if amount < 1:
            print("You must take at least one counter.")
            continue
        if amount > piles[pile_index]:
            print(f"Pile {pile_index+1} only has {piles[pile_index]} counters.")
            continue
        piles[pile_index] -= amount
        return pile_index, amount
def nimplay():
    print("=== NIM ===")
    while True:
        mode = input("1) Play vs Vinniebot      2) Play vs Human    3) Exit     Pick 1, 2 or 3: ")
        if mode == "1":
            vs_bot = True
            break
        elif mode == "2":
            vs_bot = False
            break
        elif mode == "3":
            return
        else:
            print("Please enter 1, 2 or 3")
    while True:
        piles = input("Choose how many piles (1-10): ")
        if not piles.isdigit():
            print("Please enter a number.")
            continue
        piles = int(piles)
        if piles < 1 or piles > 10:
            print("Please enter a number from 1 to 10.")
            continue
        pile_num = nim_setup(piles)
        break
    turn = 0
    if vs_bot:
        while True:
            is_bot_turn = input("Go first or second? Enter 1 or 2: ")
            if is_bot_turn == "1":
                is_bot_turn = False
                break
            elif is_bot_turn == "2":
                is_bot_turn = True
                break
            else:
                print("Please enter 1 or 2")
    else:
        is_bot_turn = False
        current = 1

    # game loop
    while True:
        print_piles(pile_num)

        if vs_bot and is_bot_turn:
            print("Vinniebot is thinking", end="")
            time.sleep(0.4)
            print(".",end="")
            time.sleep(0.4)
            print(".", end="")
            time.sleep(0.4)
            print(".", end="")
            time.sleep(0.4)
            print()
            pile_index, amount = nimbot(pile_num)
            print(f"Vinniebot takes {amount} from pile {pile_index+1}.")
        else:
            if vs_bot:
                label = "You"
            else:
                label = f'Player {current}'
            nim_humanmove(pile_num, label)

        pile_num[:] = [p for p in pile_num if p != 0]

        if len(pile_num) == 0:
            if vs_bot:
                if is_bot_turn:
                    print("Vinniebot wins! 🤖")
                else:
                    print("You win! 🎉")
            else:
                print(f"Player {current} wins! 🎉")
            return

        if vs_bot:
            is_bot_turn = not is_bot_turn
        else:
            current = 3-current
if __name__ == "__main__": #localtesting
    nimplay()
