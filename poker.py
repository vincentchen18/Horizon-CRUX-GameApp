suits = "♥♦♣♠"
nums = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
cardmapper = {'A':14, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8,"9":9,"10":10, "J":11,"Q":12,"K":13}
import random, time

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
