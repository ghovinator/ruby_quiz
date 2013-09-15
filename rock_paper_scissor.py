#!/usr/bin/python
import collections
import itertools
import random

# global record of state
state = (0, [], [])

def play_game(A, B):
    global state
    a_result = A(state)
    b_result = B((state[0] * -1, state[2], state[1]))
    winner = 0
    if a_result == b_result:
        winner = 0
    elif a_result == "rock":
        if b_result == "scissor":
            winner = 1
        else:
            winner = -1
    elif a_result == "paper":
        if b_result == "rock":
            winner = 1
        else:
            winner = -1
    elif a_result == "scissor":
        if b_result == "paper":
            winner = 1
        else:
            winner = -1
    state = (winner, state[1] + [a_result],
             state[2] + [b_result])
    if winner == 1:
        return A
    elif winner == -1:
        return B
    else:
        return None

possible_moves = ["rock", "scissor", "paper"]

def paper_always(current_state):
    return "paper"

def rock_always(current_state):
    return "rock"

def scissor_always(current_state):
    return "scissor"

def random_always(current_state):
    return random.choice(possible_moves)

def predictable_order(current_state):
    if len(current_state[1]):
        return possible_moves[(possible_moves.index(current_state[1][-1]) + 1) % len(possible_moves)]
    else:
        return "rock"

strategies = [paper_always, rock_always, scissor_always, random_always, predictable_order]

def play_tournament(strategies, series_length=500):
    global state
    result = collections.defaultdict(int)
    for A, B in itertools.combinations(strategies, 2):
        state = (0, [], [])
        for _ in range(series_length):
            winner = play_game(A, B)
            if winner == A:
                result[A, B] += 1
            elif winner == B:
                result[B, A] += 1
    result = dict(result)
    print (report_tournament(strategies, result))

def report_tournament(strategies, result):
    N = len(strategies)
    table = []
    for s in strategies:
        items = [result.get((s, t), 0) for t in strategies]
        items = ['{0:<20}'.format(s.__name__)] + map('{0:>5}'.format, items + [sum(items)])
        print ' '.join(items)


play_tournament(strategies)


def test():
    assert paper_always == play_game(paper_always, rock_always)
    assert paper_always == play_game(rock_always, paper_always)
    assert rock_always == play_game(rock_always, scissor_always)
    assert scissor_always == play_game(paper_always, scissor_always)
    assert predictable_order((0,["rock", "scissor"], [])) == "paper"
    assert predictable_order((0,["rock", "scissor", "paper"], [])) == "rock"
    assert predictable_order((0,["rock", "scissor", "rock"], [])) == "scissor"
    assert predictable_order((0, [], [])) == "rock"
    print "All tests passed."
    
test()
