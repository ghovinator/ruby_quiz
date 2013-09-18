#!/usr/bin/python
import random
import itertools
import sys

def is_family(pair):
    first, second = pair
    return first.split()[1] == second.split()[1]

def choose_secret_santa(members):
    initial_pairings = itertools.permutations(members, 2)
    def helper(pairings, gifter, gifted):
        if sorted(gifter) == sorted(gifted) and sorted(gifter) == sorted(members):
            return zip(gifter, gifted)
        for pairing in pairings:
            person1, person2 = pairing
            if person1 in gifter or person2 in gifted:
                continue
            return helper([pair for pair in pairings if person1 != pair[0] and person2 != pair[1]],
                          gifter + [person1], gifted + [person2])
        return []
    # remove families
    initial_pairings = [pair for pair in initial_pairings if not is_family(pair)]
    random.shuffle(initial_pairings)
    decisions = helper(initial_pairings, [], [])
    if not decisions:
        return False
    for gifter, gifted in decisions:
        print '%s -> %s' %(gifter, gifted)
    return True

def test():
    members = ['Mr. Gray', 'Mrs. Gray', 'Mr. Thomas', 'Mrs. Thomas',
                       'Mr. Matsumoto', 'Mrs. Matsumoto', 'Mr. Fulton', 'Mrs. Fulton']
    choose_secret_santa(members)

def driver():
    if len(sys.argv) > 1:
        members = sys.argv[1:]
    else:
        members = []
        while(True):
            member = raw_input("Enter member(blank to stop): ")
            if not member:
                break
            members.append(member)
    if len(members) % 2:
        print "Error: Unable to match everyone because there is an odd number"
        return
    while(not choose_secret_santa(members)):
        pass
        
if __name__ == "__main__":
    driver()
    #test()
