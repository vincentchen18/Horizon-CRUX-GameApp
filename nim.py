import random
def nim_setup(pile_num):
    return [random.randint(1,20) for i in range(pile_num)]

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
        return piles
    for i in range(len(piles)):
        if (piles[i] ^ default) < piles[i]:
            piles[i] ^= default
            return piles

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
        piles = input("Choose how many piles: ")
        if not piles.isdigit():
            print("Please enter a number.")
            continue
        piles = int(piles)
        pile_numbers = nim_setup(piles)
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

