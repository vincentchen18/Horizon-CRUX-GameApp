suits = "♥♦♣♠"
nums = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
cardmapper = {'A':14, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8,"9":9,"10":10, "J":11,"Q":12,"K":13}
import random, time, itertools
from collections import Counter
hands = {10:"Straight Flush", 9:'Four of a Kind', 8: "Full House", 7: "Flush", 6: "Straight", 5: "Three of a Kind", 4: "Two Pair", 3: "Pair", 2:"High Card",}

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
        return [9, four, list(set(r)-{four})[0]]
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
        ev = check_set(combo)
        if ev > best:
            best = ev
    return best

def showdown(list_of_hands):
    winner = max(list_of_hands)
    distribution = [0 for i in range(len(list_of_hands))]
    win = [hand == winner for hand in list_of_hands]
    split = win.count(True)
    for i in range(5):
        if win[i]:
            distribution[i] = round(1/split, 2)
    return distribution

def print_board(action1, action2, action3, action4, action5, b1, b2, b3, b4, b5): # -> actions: CALL, FOLD, ALL IN, etc
    pass

def reset_for_new_hand(state):
    #
    for x in range(5):
        state['players'][x]['hole_cards'] = []
        state['players'][x]['current_bet'] = 0
        state['players'][x]['total_committed'] = 0
        state['players'][x]['has_folded'] = False
        state['players'][x]['is_all_in'] = False
        state['players'][x]['last_action'] = ""
    return state

def poker_play(): #hardcode player to p3
    while True:
        c = input("1) Play Poker    2) Exit    Please enter 1 or 2: ")
        if c == "1":
            break
        elif c == "2":
            return
        print("That's not a valid choice, please enter 1 or 2.")
    state = {
        "players": [
            {
                "name": "Vinnie",
                "balance": 1000,
                "hole_cards": [],
                "current_bet": 0,
                "total_committed": 0,
                "has_folded": False,
                "is_all_in": False,
                "is_human": False,
                "last_action": "",
            },
            {
                "name": "Shawn",
                "balance": 1000,
                "hole_cards": [],
                "current_bet": 0,
                "total_committed": 0,
                "has_folded": False,
                "is_all_in": False,
                "is_human": False,
                "last_action": "",
            },
            {
                "name": "You",
                "balance": 1000,
                "hole_cards": [],
                "current_bet": 0,
                "total_committed": 0,
                "has_folded": False,
                "is_all_in": False,
                "is_human": True,
                "last_action": "",
            },
            {
                "name": "Roy",
                "balance": 1000,
                "hole_cards": [],
                "current_bet": 0,
                "total_committed": 0,
                "has_folded": False,
                "is_all_in": False,
                "is_human": False,
                "last_action": "",
            },
            {
                "name": "Charles",
                "balance": 1000,
                "hole_cards": [],
                "current_bet": 0,
                "total_committed": 0,
                "has_folded": False,
                "is_all_in": False,
                "is_human": False,
                "last_action": "",
            },
        ],
        "board": [],
        "deck": [],
        "pots": [],
        "pot": 0,
        "current_bet": 0,
        "min_raise": 20,
        "dealer_pos": 2,
        "small_blind": 10,
        "big_blind": 20,
        "stage": "preflop",
        "last_raiser": None,
    }


#test
p1,p2,p3,p4,p5,river = deal(poker_shuffle())
construct = [best_hand(p1+river), best_hand(p2+river), best_hand(p3+river), best_hand(p4+river), best_hand(p5+river)]
print(river)
print(p1, hands[construct[0][0]])
print(p2, hands[construct[1][0]])
print(p3, hands[construct[2][0]])
print(p4, hands[construct[3][0]])
print(p5, hands[construct[4][0]])
print(showdown(construct))
