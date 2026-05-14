suits = "♥♦♣♠"
nums = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
deck = [nums[i] + suits[j] for i in range(13) for j in range(4)]
cardmapper = {'A':11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8,"9":9,"10":10, "J":10,"Q":10,"K":10}
import random, time

def blackjack_setup():
    random.shuffle(deck)
    card1, card2, card3, card4 = deck[0], deck[1], deck[2], deck[3]
    return card1, card2, card3, card4


def blackjack_play():
    balance = 1000
    while True:
        a = input("1) Play Blackjack    2) Exit    Please enter 1 or 2: ").strip()
        if a == "1":
            break
        elif a == '2':
            return
        else:
            print("Invalid input. Please enter 1 or 2.")

    while True:
        while True:
            print(f"Your balance is ${balance}, how much would you like to wager? Please enter an integer.")
            money = input("$")
            try:
                money = int(money)
                if money <= 0:
                    print("Wager must be greater than zero.")
                    continue
                elif money > balance:
                    print("You don't have enough money to wager this!.")
                    continue
                else:
                    print(f"Wagering ${money}.")
                    balance -= money
                    break
            except ValueError:
                print("Please enter a number.")
                continue
    # wager

        mycard1, mycard2, dealercard1, dealercard2 = blackjack_setup()
        mycards = [mycard1, mycard2]
        print("Shuffling the cards", end="")
        for i in range(3):
            time.sleep(0.4)
            print(".",end="")
        time.sleep(0.4)
        print()
        print(f"Your cards are {mycard1} and {mycard2}")
        print(f"Dealer drew {dealercard1}")
        total = cardmapper[mycard1[:-1]] + cardmapper[mycard2[:-1]]
        if total == 21:
            print(f"Dealer's second card was {dealercard2}, so his total is {cardmapper[dealercard1[:-1]] + cardmapper[dealercard2[:-1]]}")
            if cardmapper[dealercard1[:-1]] + cardmapper[dealercard2[:-1]] == 21:
                print("Tie, no money lost, none gained.")
                balance += money
                continue
            print(f"BLACKJACK! You win ${int(money*1.5)}.")
            balance += int(2.5*money)
            continue

blackjack_play()