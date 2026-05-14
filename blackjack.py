suits = "♥♦♣♠"
nums = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
cardmapper = {'A':11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8,"9":9,"10":10, "J":10,"Q":10,"K":10}
import random, time

def blackjack_setup():
    deck = [nums[i] + suits[j] for i in range(13) for j in range(4)]
    random.shuffle(deck)
    return deck

def hand_value(cards):
    total = sum(cardmapper[c[:-1]] for c in cards)
    aces = sum(1 for c in cards if c[:-1] == 'A')
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

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
                if float(money) != int(money):
                    print("Wager must be an integer.")
                    continue
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

        deck = blackjack_setup()
        mycards = [deck.pop(), deck.pop()]
        dealercards = [deck.pop(),deck.pop()]
        print("Shuffling the cards", end="")
        for i in range(3):
            time.sleep(0.4)
            print(".",end="")
        time.sleep(0.4)
        print()
        print(f"Your cards are {mycards[0]} and {mycards[1]}, summing to {hand_value(mycards)}")
        print(f"Dealer drew {dealercards[0]}")
        myTotal = hand_value(mycards)
        dealerTotal = hand_value(dealercards)
        meblackjack = myTotal == 21
        dealerblackjack = dealerTotal == 21

        if meblackjack and not dealerblackjack:
            print(f"Dealer's second card was {dealercards[1]}, so his total is {dealerTotal}.")
            print(f"BLACKJACK! 🎉 You won ${int(money*2.5)}!!!")
            balance += int(money*2.5)
        elif dealerblackjack and not meblackjack:
            print(f"Dealer's second card was {dealercards[1]}, so his total is {dealerTotal}.")
            print(f"Dealer blackjacked! You lose ${money}. :(")
        elif dealerblackjack and meblackjack:
            print(f"Dealer's second card was {dealercards[1]}, so his total is {dealerTotal}.")
            print(f"TIE! You both blackjacked! You receive ${money} back.")
            balance += money
        else:
            while myTotal < 21:
                action = input("Hit or stand? ").strip().upper()
                if action == 'HIT':
                    mycards.append(deck.pop())
                    myTotal = hand_value(mycards)
                    print(f"You drew {mycards[-1]}, making your new total {myTotal}.")
                elif action == 'STAND':
                    break
                else:
                    print("That is not a valid action. Please enter either Hit or Stand.")
            skip = False
            if myTotal > 21:
                print(f"You bust! You lose ${money}. :(")
                skip = True
            if not skip:
                print(f"Dealer's second card was {dealercards[1]}, so his hand is {" and ".join(dealercards)}, totaling {dealerTotal}.")
                while dealerTotal < 17:
                    print("Dealer is drawing until his total > 16.")
                    dealercards.append(deck.pop())
                    print("Dealer is drawing a card", end="")
                    for i in range(3):
                        time.sleep(0.4)
                        print(".",end="")
                    time.sleep(0.4)
                    dealerTotal = hand_value(dealercards)
                    print(f"Dealer drew {dealercards[-1]}, so his total is now {dealerTotal}.")
                if dealerTotal > 21:
                    print(f"Dealer busts, you win ${money}!!")
                    balance += money*2
                elif myTotal > dealerTotal:
                    print(f"You are closer to 21, you win ${money}!!")
                    balance += money*2
                elif dealerTotal > myTotal:
                    print(f"Dealer are closer to 21, you lose ${money}!!")
                else:
                    print(f"Push, you and the dealer tied. You get your wager of ${money} back.")
                    balance += money
            if balance <= 0:
                print("Oh no, looks like you ran outta money. Game over.")
                return
            choice = input("Would you like to play again? (y/n): ").strip().upper()
            if choice == 'Y':
                continue
            elif choice == 'N':
                print(f"Thank you for playing, you leave with ${money}.")
                return
            else:
                print("That is not a valid choice. Please enter Y or N.")


blackjack_play()