#!/usr/bin/python
import sys
from collections import defaultdict

# a horse can move by adding these numbers to its (x,y) cordinates
horse_moves = [-2, -1, 1, 2]
possible_rows = "abcdefgh"
possible_cols = "12345678"

def successors(state, forbidden):
    moves = []
    for row in horse_moves:
        for col in horse_moves:
            if abs(row) == abs(col):
                continue
            new_row = chr(ord(state[0]) + row)
            new_col = str(int(state[1]) + col)
            if new_row in possible_rows and new_col in possible_cols and \
               (new_row + new_col) not in forbidden:
                moves.append((new_row + new_col, (row, col)))
    return dict(moves)

def is_goal(state, end):
    return True if state == end else False

def get_shortest_path(frontier):
    return sorted(frontier, key=len)[0]

def shortest_path_search(start, end, successors, forbidden, is_goal):
    if is_goal(start, end):
        return [start]
    explored = set()
    frontier = [[start]]
    while frontier:
        path = get_shortest_path(frontier)
        frontier.remove(path)
        s = path[-1]
        for (state, action) in successors(s, forbidden).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [state]
                if is_goal(state, end):
                    return path2[1:]
                else:
                    frontier.append(path2)
    return []
                
def driver():
    if len(sys.argv) < 3:
        print "Error: Please provide a start and end"
        return
    start, end, forbidden = sys.argv[1], sys.argv[2], sys.argv[3:]
    print shortest_path_search(start, end, successors, forbidden, is_goal)
    


if __name__ == "__main__":
    driver()
