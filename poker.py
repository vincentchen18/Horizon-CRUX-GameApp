suits = "♥♦♣♠"
nums = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
cardmapper = {'A':14, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8,"9":9,"10":10, "J":11,"Q":12,"K":13}
import random, time, itertools
from collections import Counter

def poker_shuffle():
    deck = [nums[i] + suits[j] for i in range(13) for j in range(4)]
    random.shuffle(deck)
    return deck

def deal(cards):
    p1 = [cards.pop(), cards.pop()]
    p2 = [cards.pop(), cards.pop()]
    p3 = [cards.pop(), cards.pop()]
    p4 = [cards.pop(), cards.pop()]
    p5 = [cards.pop(), cards.pop()]
    river = [cards.pop(), cards.pop(),cards.pop(),cards.pop(),cards.pop()]
    return p1, p2, p3, p4, p5, river

def ranks(cards):
    newcards = []
    for card in cards:
        newcards.append(cardmapper[card[:-1]])
    return newcards

def is_flush(cards):
    cardsuits = [card[-1] for card in cards]
    if cardsuits[0] == cardsuits[1] == cardsuits[2] == cardsuits[3] == cardsuits[4]:
        return True
    return False

def is_straight(ranks):
    newranks = sorted(ranks)
    if newranks[0]+4 == newranks[1]+3 == newranks[2]+2 == newranks[3]+1 == newranks[4]:
        return True, newranks[4]
    if newranks == [2,3,4,5,14]:
        return True, 5
    return False, None

def is_four_of_a_kind(ranks):
    newranks = sorted(ranks)
    counts = Counter(newranks)
    if max(counts.values()) == 4:
        return True, [k for k in counts.keys() if counts[k] == 4][0]
    return False, None

def is_full_house(ranks):
    newranks = sorted(ranks)
    counts = Counter(newranks)
    if len(counts.values()) == 2 and max(counts.values()) == 3 and min(counts.values()) == 2:
        return True, [k for k in counts.keys() if counts[k] == 3][0], [k for k in counts.keys() if counts[k] == 2][0]
    return False, None, None

def is_three_of_a_kind(ranks):
    newranks = sorted(ranks)
    counts = Counter(newranks)
    if max(counts.values()) == 3:
        return True, [k for k in counts.keys() if counts[k] == 3][0]
    return False, None

def is_two_pair(ranks):
    newranks = sorted(ranks)
    counts = Counter(newranks)
    if max(counts.values()) == 2 and list(counts.values()).count(2) == 2:
        return True, [k for k in counts.keys() if counts[k] == 2], [k for k in counts.keys() if counts[k] == 1][0]
    return False, None, None

def is_one_pair(ranks):
    newranks = sorted(ranks)
    counts = Counter(newranks)
    if max(counts.values()) == 2:
        return True, [k for k in counts.keys() if counts[k] == 2][0], [k for k in counts.keys() if counts[k] == 1]
    return False, None, None

def check_set(cards):
    r = ranks(cards)
    #check in order: straight flush -> four of a kind -> full house -> flush -> straight -> 3 of a kind -> 2 pair -> 1 pair -> high
    if is_flush(cards) and is_straight(r)[0]:
        if sorted(r) == [2,3,4,5,14]:
            return [10, 5]
        else:
            return [10, max(r)]
    elif is_four_of_a_kind(r)[0]:
        yes, four = is_four_of_a_kind(r)
        return [9, four, set(r)-{four}]
    elif is_full_house(r)[0]:
        yes, triple, double = is_full_house(r)
        return [8, triple, double]
    elif is_flush(cards):
        sr = sorted(r)
        return [7, sr[-1],sr[-2],sr[-3],sr[-4],sr[-5]]
    elif is_straight(r)[0]:
        yes, big = is_straight(r)
        return [6, big]
    elif is_three_of_a_kind(r)[0]:
        yes, triple = is_three_of_a_kind(r)
        kickers = sorted([n for n in r if n != triple], reverse=True)
        return [5, triple, kickers[0], kickers[1]]
    elif is_two_pair(r)[0]:
        yes, twos, kicker = is_two_pair(r)
        return [4, max(twos), min(twos), kicker]
    elif is_one_pair(r)[0]:
        yes, pair, kickers = is_one_pair(r)
        kickers.sort(reverse=True)
        return [3, pair, kickers[0], kickers[1], kickers[2]]
    else:
        # HIGH CARD LOOOL
        returnee = [2]
        returnee.extend(sorted(r, reverse=True))
        return returnee

def best_hand(cards_7):
    combos = itertools.combinations(cards_7, 5)
    best = [0,0,0]
    for combo in combos:
        if check_set(combo) > best:
            best = check_set(combo)
    return best

def showdown(h1, h2, h3, h4, h5):
    winner = max(h1, h2, h3, h4, h5)
    distribution = [0,0,0,0,0]
    win = [hand == winner for hand in [h1, h2, h3, h4, h5]]
    split = win.count(True)
    for i in range(5):
        if win[i]:
            distribution[i] = round(1/split, 2)
    return distribution

def print_board(action1, action2, action3, action4, action5, b1, b2, b3, b4, b5): # -> actions: CALL, FOLD, ALL IN, etc
    pass

def poker_play(): #hardcode player to p3
    while True:
        c = input("1) Play Poker    2) Exit    Please enter 1 or 2: ")
        if c == "1":
            break
        elif c == "2":
            return
        print("That's not a valid choice, please enter 1 or 2.")

p1,p2,p3,p4,p5,river = deal(poker_shuffle())
print(river,p1)
print(best_hand(river + p1))
