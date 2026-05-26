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
    for i in range(len(list_of_hands)):
        if win[i]:
            distribution[i] = round(1/split, 2)
    return distribution

def print_board(state, current_person=None): # -> actions: CALL, FOLD, ALL IN, etc
    red = "\033[91m"
    blue = "\033[94m"
    regular = "\033[0m"
    community = state["board"] + ["##"] * (5-len(state["board"]))
    c1,c2,c3,c4,c5 = community
    print("                            COMMUNITY CARDS")
    print()
    print(f"                         {c1}   {c2}   {c3}   {c4}   {c5}")
    print()
    print()
    names = []
    hole_cards = []
    balances = []
    actions = []
    committed = []
    for index, player in enumerate(state["players"]):
        # dealer button
        if index == state["dealer_pos"]:
            display_name = f"{player['name']} {blue}(D){regular}"
            visible_len = len(player['name']) + 4  # " (D)" = 4 visible chars
        else:
            display_name = player['name']
            visible_len = len(player['name'])

        # red if it's someone's current turn
        if index == current_person:
            name_str = f"{red}{display_name}{regular}"
        else:
            name_str = display_name

        # manual pad
        padding = max(12 - visible_len, 1)
        name_str = name_str + " " * padding
        names.append(name_str)

        if player["is_human"] or player["has_folded"]:
            hc = " ".join(player["hole_cards"]) if player["hole_cards"] else ""
        else:
            hc = "?? ??"
        if player["has_folded"]:
            hc = "FOLDED"
        hole_cards.append(f"{hc:<12}")
        balances.append(f"${player['balance']:<11}")
        actions.append(f"{player['last_action']:<12}")
        committed.append(f"${player['total_committed']:<11}")
    print("     ".join(committed))
    print("     ".join(hole_cards))
    print("     ".join(names))
    print("     ".join(actions))
    print("     ".join(balances))
    print()

def reset_for_new_hand(state):
    #
    for x in range(5):
        state['players'][x]['hole_cards'] = []
        state['players'][x]['current_bet'] = 0
        state['players'][x]['total_committed'] = 0
        state['players'][x]['has_folded'] = False
        state['players'][x]['is_all_in'] = False
        state['players'][x]['last_action'] = ""
    state["board"] = []
    state["deck"] = []
    state["pots"] = []
    state["pot"] = 0
    state["current_bet"] = 0
    state["min_raise"] = state["big_blind"]
    state["stage"] = "preflop"
    state["last_raiser"] = None
    return state

def collect_bets(state):
    contributors = []
    for index, player in enumerate(state["players"]):
        if player['current_bet'] > 0:
            contributors.append((index, player['current_bet'], player['has_folded']))
    if not contributors:
        return #nothing happened lol
    levels = sorted(set([contributor[1] for contributor in contributors]))
    previous_level = 0
    for level in levels:
        # pot logic: if someone all in, they can only receive max 5* their all in assuming everyone else is still in.
        slice_size = level-previous_level
        pot_amt = slice_size * len([c[1] for c in contributors if c[1] >= level])
        eligible = sorted([c[0] for c in contributors if c[1] >= level and not c[2]])
        if not eligible:
            if state['pots']:
                state['pots'][-1]['amount'] += pot_amt
            previous_level = level
            continue
        merged = False
        for existing_pot in state["pots"]:
            if sorted(existing_pot["eligible"]) == eligible:
                existing_pot['amount'] += pot_amt
                merged = True
                break
        if not merged:
            state["pots"].append({"amount":pot_amt, "eligible":eligible})
        previous_level = level

    for player in state["players"]:
        player['current_bet'] = 0 #refresh for next round
    state['pot'] = sum(player['amount'] for player in state["pots"])

def award_pots(state): #compare hands and distribute winnings. If tie and not int, give remaining chips to winner closest to the left of the dealer
    results = []
    for pot_index, pot in enumerate(state["pots"]):
        evaluations = [best_hand(state["players"][index]["hole_cards"] + state["board"] for index in pot['eligible'])]
        distribution = showdown(evaluations)
        winners = []
        total_awarded = 0
        for index, winnings_percent in enumerate(distribution):
            if winnings_percent > 0:
                player_index = pot['eligible'][index]
                winnings = int(pot['amount'] * winnings_percent)
                state['players'][player_index]['balance'] += winnings
                total_awarded += winnings
                winners.append(player_index)
        leftovers = pot['amount'] - total_awarded
        if leftovers != 0 and winners: #redistribute remainders to the winner closest on the left of the dealer
            winners_priority = sorted(winners, key=lambda i: (state['dealer_pos']-i)%5)
            step = 1
            for i in range(leftovers):
                target = winners_priority[i % len(winners_priority)]
                state['players'][target]['balance'] += step
        results.append((pot_index, winners, pot['amount']))
    state['pots'] = []
    state['pot'] = 0
    return results

def apply_action(state, player_index, action, amount):
    player = state['players'][player_index]
    if action == "fold":
        player['has_folded'] = True
        player['last_action'] = "FOLD"
        return
    if action == "check":
        player['last_action'] = "CHECK"
        return
    if action == "call":
        player['balance'] -= amount
        player['current_bet'] += amount
        player['total_committed'] += amount
        player['last_action'] = f"CALL ${amount}"
        return
    if action == "raise":
        extra_money_needed = amount - player['current_bet']
        player['balance'] -= extra_money_needed
        player['current_bet'] = amount
        player['total_committed'] += extra_money_needed
        increment = amount - state['current_bet']
        state['min_raise'] = max(state['min_raise'], increment)
        state['current_bet'] = amount
        player['last_action'] = f"RAISE TO ${amount}"
        return
    if action == 'all_in': # wow either very poor or very confident
        actual = player['balance']
        player['balance'] = 0
        player['current_bet'] += actual
        player['total_committed'] += actual
        if player['current_bet'] > state['current_bet']: # enough to match
            increment = player['current_bet'] - state['current_bet']
            state['min_raise'] = max(state['min_raise'], increment)
            state['current_bet'] = player['current_bet']
        player['last_action'] = f"ALL IN ${player['current_bet']}"
        return

def count_not_folded(state):
    return sum(1 for p in state['players'] if not p['has_folded'])

def count_able_to_act(state):
    return sum(1 for p in state['players'] if not p['has_folded'] and not p['is_all_in'])

def all_active_have_matched(state):
    # if everyone has called, then return true
    for p in state['players']:
        if p['has_folded'] or p['is_all_in']:
            continue#ignore, they can't move
        if p['current_bet'] != state['current_bet']: # under has not called or over just raised
            return False
    return True

def first_active(state, start_index): # find first nonfolded player
    index = start_index
    for i in range(5):
        player = state['players'][index]
        if not player['has_folded'] and not player['is_all_in']:
            return index
        index = (index-1)%5
    return start_index

def next_active(state, current): # find next player that can move
    index = (current-1)%5
    for i in range(5):
        player = state['players'][index]
        if not player['has_folded'] and not player['is_all_in']:
            return index
        index = (index-1)%5
    return current

def next_active_right(state, current): # find who closes round if the current player raises
    index = (current+1)%5
    for i in range(5):
        player = state['players'][index]
        if not player['has_folded'] and not player['is_all_in']:
            return index
        index = (index+1)%5
    return current

def legal_actions(state, player_index):
    p = state['players'][player_index]
    required_to_stay_in_play = state['current_bet'] - p['current_bet']
    legal = {"fold":True, "check":False, "call":False, "all_in":p['balance']>0}
    if required_to_stay_in_play == 0:
        legal["check"] = True
    elif p['balance'] >= required_to_stay_in_play:
        legal['call'] = required_to_stay_in_play
    return legal

def get_action(state, player_index, legal):
    # temporarily, since no bots, check if can, else call, else fold
    if legal.get("check"):
        return ('check', 0)
    if legal.get("call"):
        return ('call', legal['call'])
    return ('fold', 0)



def betting_round(state):
    if state['stage'] == 'preflop':
        start = (state['dealer_pos']-3)%5 #guy after big blind
        closing_player = (state['dealer_pos']-2)%5
        state['last_raiser'] = None
    else:
        start = (state['dealer_pos']-1)%5 # guy after dealer goes if not preflop
        closing_player = None
    state['last_raiser'] = None
    start = first_active(state, start)
    if count_able_to_act(state) == 0:
        return
    if count_not_folded(state) <= 1:
        return

    if state['stage'] != 'preflop' and closing_player is None:
        closing_player = start
    current = start
    iterations = 0 # --> guard against infiniteloops in testing
    while True:
        iterations += 1
        if iterations > 100:
            print("EXCEED 100, FORCE QUITTING")
            break
        player = state['players'][current]
        if player['has_folded'] or player['is_all_in']:
            current = next_active(state, closing_player)
            continue
        prev_table_bet = state['current_bet']
        #applyaction
        legal = legal_actions(state, current)
        action, amount = get_action(state, current, legal)
        apply_action(state, current, action, amount)

        if count_not_folded(state) == 1:
            return
        is_raise = action == 'raise' or (action == 'all_in' and state['current_bet'] > prev_table_bet)
        if is_raise:
            state['last_raiser'] = current
            closing_player = next_active_right(state, current)
        if all_active_have_matched(state):
            if current == closing_player:
                return
            bb_pos = (state['dealer_pos']-2)%5
            if state['stage'] == 'preflop' and state['last_raiser'] is None and current == bb_pos:
                return
        if count_able_to_act(state) == 0:
            return
        current = next_active(state, current)

def play_hand(state):
    reset_for_new_hand(state)
    state["deck"] = poker_shuffle()

    for player in state["players"]:
        player['hole_cards'] = [state["deck"].pop(), state["deck"].pop()] #deal
    state["stage"] = "preflop"
    print_board(state)
    betting_round(state)
    collect_bets(state)

    #flop
    state["board"].extend(state["deck"].pop() for i in range(3))
    state["stage"] = "flop"
    print_board(state)
    betting_round(state)
    collect_bets(state)

    #card4
    state["board"].append(state["deck"].pop())
    state["stage"] = "turn"
    print_board(state)
    betting_round(state)
    collect_bets(state)

    #river/card5
    state["board"].append(state["deck"].pop())
    state["stage"] = "river"
    print_board(state)
    betting_round(state)
    collect_bets(state)

    #showdown
    state["stage"] = "showdown"
    print("Showdown (not coded yet, (stub))")
    award_pots(state)

    state['dealer_pos'] = (state['dealer_pos']-1)%5





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
    for hand_num in range(3):
        print('testing...')
        play_hand(state)
        input("Press Enter to continue...")

#test
if __name__ == "__main__":
    #p1,p2,p3,p4,p5,river = deal(poker_shuffle())
    #construct = [best_hand(p1+river), best_hand(p2+river), best_hand(p3+river), best_hand(p4+river), best_hand(p5+river)]
    #print(river)
    #print(p1, hands[construct[0][0]])
    #print(p2, hands[construct[1][0]])
    #print(p3, hands[construct[2][0]])
    #print(p4, hands[construct[3][0]])
    #print(p5, hands[construct[4][0]])
    #print(showdown(construct))
    #state = {"players": [{"name": "Vinnie", "balance": 1000, "hole_cards": p1, "current_bet": 0, "total_committed": 0, "has_folded": False, "is_all_in": False, "is_human": False, "last_action": ""}, {"name": "Shawn", "balance": 1000, "hole_cards": p2, "current_bet": 0, "total_committed": 0, "has_folded": False, "is_all_in": False, "is_human": False, "last_action": ""}, {"name": "You", "balance": 1000, "hole_cards": p3, "current_bet": 0, "total_committed": 0, "has_folded": False, "is_all_in": False, "is_human": True, "last_action": ""}, {"name": "Roy", "balance": 1000, "hole_cards": p4, "current_bet": 0, "total_committed": 0, "has_folded": False, "is_all_in": False, "is_human": False, "last_action": ""}, {"name": "Charles", "balance": 1000, "hole_cards": p5, "current_bet": 0, "total_committed": 0, "has_folded": False, "is_all_in": False, "is_human": False, "last_action": ""}], "board": [], "deck": [], "pots": [], "pot": 0, "current_bet": 0, "min_raise": 20, "dealer_pos": 2, "small_blind": 10, "big_blind": 20, "stage": "preflop", "last_raiser": None}
    #print_board(state, 1)

    poker_play()
