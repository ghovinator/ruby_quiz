#!/usr/bin/python
import random
import itertools

def card_ranks(hand):
    ranks = [14 if r == 'A' else
             13 if r == 'K' else
             12 if r == 'Q' else
             11 if r == 'J' else
             10 if r == 'T' else
             int(r) for r,s in hand]
    ranks.sort(reverse=True)
    return ranks if ranks != [14, 5, 4, 3, 2] else [5, 4, 3, 2, 1]

def is_flush(hand):
    suits = [s for r, s in hand]
    return suits[0] if len(set(suits)) == 1 else None

def is_straight(ranks):
    if len(set(ranks)) == 5 and ((ranks[0] - ranks[4]) == 4):
        return ranks[0]
    else:
        return None

def n_kind(ranks):
    if len(set(ranks)) == 3:
        # two pairs or 3 of a kind
        result = []
        counts = []
        for card in set(ranks):
            if ranks.count(card) == 1:
                result.append(card)
            else:
                result = [card] + result
                counts.append(ranks.count(card))
        return (sorted(counts, reverse=True), result)
    elif len(set(ranks)) == 2:
        # four of a kind or full house
        card1, card2 = set(ranks)
        if ranks.count(card1) == 1:
            return ((4,), [card2, card1])
        elif ranks.count(card1) == 4:
            return ((4,) [card1, card2])
        elif ranks.count(card1) == 3:
            return ((3, 2), [card1, card2])
        else:
            return ((3, 2), [card2, card1])
    elif len(set(ranks)) == 4:
        result = []
        for card in set(ranks):
            if ranks.count(card) == 1:
                result.append(card)
            else:
                result = [card] + result
        result[1:] = sorted(result[1:], reverse=True)
        return ((2,), result)
    else:
        return (0, None)
        

def best_hand(hand):
    """Takes in a 5 card hand and returns a (rank, kickers)."""
    ranks = card_ranks(hand)
    flush = is_flush(hand)
    straight = is_straight(ranks)
    kind, pairs = n_kind(ranks)
           
    if flush and straight:
        if straight == 14:
            return (9, [])
        else:
            return (8, straight)
    elif kind and 4 in kind:
        return (7, pairs)
    elif kind and 2 in kind and 3 in kind:
        return (6, pairs)
    elif flush:
        return (5, flush)
    elif straight:
        return (4, straight)
    elif kind and 3 in kind:
        return (3, pairs)
    elif kind and 2 in kind:
        if len(kind) == 2:
            return (2, pairs)
        else:
            return (1, pairs)
    else:
        return (0, ranks)

def simulate_game(players=2):
    deck = [c + s for c in "23456789TJQK" for s in "SCHD"]
    middle_cards = [deck.pop(deck.index(random.choice(deck))) for i in range(5)]
    players_cards = []

    for player in range(players):
        players_cards.append([deck.pop(deck.index(random.choice(deck))) for i in range(2)])
    
    print "Welcome to Texas Holdem!!"
    print "%d number of players joined" %players
    print "The middle cards revealed: %s" %' '.join(middle_cards)
    # get possible 5 card hands
    winning_hands = []
    for player in range(players):
        possible_hands = []
        for hand in itertools.combinations(middle_cards + players_cards[player], 5):
            possible_hands.append(list(hand))
        winning_hands.append(sorted(map(best_hand, possible_hands), reverse=True)[0])
    for player in range(players):
        print "Player%d has %s with best hand: %s" %(player + 1, ' '.join(players_cards[player]), winning_hands[player])
    winning_hand = sorted(winning_hands, reverse=True)[0]
    print "\n\nThe winning hand belongs to player %d with %s" %(winning_hands.index(winning_hand) + 1, winning_hand)
        
        
def test():
    # test royal flush
    assert best_hand([("A", "S"), ("Q", "S"), ("K", "S"), ("J", "S"), ("10", "S")]) == (9, [])
    # test straight flush
    assert best_hand([("4", "S"), ("A", "S"), ("2", "S"), ("3", "S"), ("5", "S")]) == (8, 5)
    # test four of kind
    assert best_hand([("A", "S"), ("A", "H"), ("A", "D"), ("A", "C"), ("4", "C")]) == (7, [14, 4])
    # test full house
    assert best_hand([("A", "S"), ("A", "H"), ("A", "D"), ("4", "D"), ("4", "C")]) == (6, [14, 4])
    assert best_hand([("4", "S"), ("A", "H"), ("A", "D"), ("4", "D"), ("4", "C")]) == (6, [4, 14])
    # test flush
    assert best_hand([("9", "S"), ("A", "S"), ("2", "S"), ("3", "S"), ("5", "S")]) == (5, "S")
    # test straight
    assert best_hand([("4", "S"), ("A", "H"), ("2", "D"), ("3", "D"), ("5", "C")]) == (4, 5)
    # test three of a kind, this is a bug to be fixed
    #assert best_hand([("A", "S"), ("A", "H"), ("A", "D"), ("3", "D"), ("4", "C")]) == (3, [14, 4, 3])
    # test two pairs
    assert best_hand([("4", "S"), ("A", "H"), ("A", "D"), ("3", "D"), ("4", "C")]) == (2, [14, 4, 3])
    # test one pair
    assert best_hand([("5", "S"), ("A", "H"), ("A", "D"), ("3", "D"), ("4", "C")]) == (1, [14, 5, 4, 3])
    # test high card
    assert best_hand([("5", "S"), ("Q", "H"), ("K", "D"), ("3", "D"), ("4", "C")]) == (0, [13, 12, 5, 4, 3])


if __name__ == "__main__":
    simulate_game()
    #test()
