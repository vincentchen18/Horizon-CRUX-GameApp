suits = "♥♦♣♠"
nums = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
cardmapper = {'A':14, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8,"9":9,"10":10, "J":11,"Q":12,"K":13}
import random, time
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
    return p1, p2, p3, p4, p5

def ranks(cards):
    newcards = []
    for card in cards:
        newcards.append(cardmapper[card[:-1]])
    return newcards

def is_flush(cards):
    suits = [card[-1] for card in cards]
    if suits[0] == suits[1] == suits[2] == suits[3] == suits[4]:
        return True
    return False

def is_straight(ranks):
    newranks = sorted(ranks)
    if newranks[0]+4 == newranks[1]+3 == newranks[2]+2 == newranks[3]+1 == newranks[4]:
        return True
    if newranks == [2,3,4,5,14]:
        return True
    return False

def is_four_of_a_kind(ranks):
    newranks = sorted(ranks)
    counts = Counter(newranks)
    if max(counts.values()) == 4:
        return True
    return False

def is_full_house(ranks):
    newranks = sorted(ranks)
    counts = Counter(newranks)
    if len(counts.values()) == 2 and max(counts.values()) == 3 and min(counts.values()) == 2:
        return True
    return False

def is_three_of_a_kind(ranks):
    newranks = sorted(ranks)
    counts = Counter(newranks)
    if max(counts.values()) == 3:
        return True
    return False

def is_two_pair(ranks):
    newranks = sorted(ranks)
    counts = Counter(newranks)
    if max(counts.values()) == 2 and list(counts.values()).count(2) == 2:
        return True
    return False

def is_one_pair(ranks):
    newranks = sorted(ranks)
    counts = Counter(newranks)
    if max(counts.values()) == 2:
        return True
    return False
