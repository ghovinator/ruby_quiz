#!/usr/bin/python
import random

sample_maze = \
"""+---+---+---+---+---+---+---+---+---+---+
|   |               |               |   |
+   +---+   +---+   +   +---+---+   +   +
|   |       |       |           |   |   |
+   +   +---+   +---+---+---+   +   +   +
|       |   |   |               |       |
+---+---+   +   +   +---+---+---+---+---+
|               |                       |
+   +---+---+---+   +---+---+---+---+   +
|   |                   |               |
+   +---+   +---+---+---+   +---+---+   +
|       |   |       |       |       |   |
+---+   +---+   +   +   +---+   +---+   +
|       |       |       |               |
+   +---+   +---+---+---+   +---+---+---+
|       |       |           |           |
+---+   +   +   +---+   +---+---+   +   +
|   |   |   |       |   |       |   |   |
+   +   +---+---+   +   +   +   +   +   +
|                   |       |       |   |   
+---+---+---+---+---+---+---+---+---+---+"""

"""
state is position in maze
successors is possible_routes
"""
WALL = 1
NO_WALL = 2
UNDECIDED = 0
class Node:
    def __init__(self, pos, height, width):
        self.pos = pos
        self.walls = {}
        self.walls['bottom'] = UNDECIDED
        self.walls['top'] = UNDECIDED
        self.walls['right'] = UNDECIDED
        self.walls['left'] = UNDECIDED
        if not pos[0]:
            self.walls['top'] = WALL
        elif pos[0] == height - 1:
            self.walls['bottom'] = WALL
        if not pos[1]:
            self.walls['left'] = WALL
        elif pos[1] == width - 1:
            self.walls['right'] = WALL
        self.height = height
        self.width = width
    
    def get_possible_routes(self):
        directions = [k for k, v in self.walls.iteritems() if v == UNDECIDED]
        state = []
        for direction in directions:
            if direction == 'left':
                state.append((self.pos[0], self.pos[1] - 1))
            elif direction == 'right':
                state.append((self.pos[0], self.pos[1] + 1))
            elif direction == 'top':
                state.append((self.pos[0] - 1, self.pos[1]))
            elif direction == 'bottom':
                state.append((self.pos[0] + 1, self.pos[1]))
        routes = zip(state, directions)
        random.shuffle(routes)
        return routes

    def is_wall(self, direction):
        return self.walls[direction] == WALL

    def is_border(self):
        result = []
        if not self.pos[0]:
            result.append('top')
        elif self.pos[0] == self.height - 1:
            result.append('bottom')
        if not self.pos[1]:
            result.append('left')
        elif self.pos[1] == self.width - 1:
            result.append('right')
        return result


def opposite(direction):
    if direction == 'left':
        return 'right'
    elif direction == 'right':
        return 'left'
    elif direction == 'top':
        return 'bottom'
    elif direction == 'bottom':
        return 'top'

def display_direction(direction):
    if direction == 'left':
        return '<- '
    elif direction == 'right':
        return ' ->'
    elif direction == 'top' or direction == 'bottom':
        return ' | '
    return None

def print_maze(maze, routes=None):
    output = []
    routes_dict = {}
    if routes:
        for i in range(1, len(routes), 2):
            routes_dict[routes[i - 1]] = display_direction(routes[i])
    for i in range(0, len(maze) * 2 + 1):
        output.append([])
    for i in range(1, len(maze) * 2 + 1, 2):
        for node in maze[i/2]:
            # print the top of the node
            output[i - 1].append('---' if node.is_wall('top') else '   ')
            # print bottom of the node if we are on the bottom row of
            # the maze
            if 'bottom' in node.is_border():
                output[i + 1].append('---')
            # print the middle of the node include the side walls and
            # maybe a route
            l_r_str = routes_dict[node] if routes and node in routes_dict else '   '
            output[i].append('|%s' %l_r_str if node.is_wall('left') else ' %s' %l_r_str)
            if 'right' in node.is_border():
                output[i].append('|')
    for i, line in enumerate(output):
        if i % 2:
            print ''.join(line)
        else:
            print '%s%s%s' %('+', '+'.join(line), '+')

def generate_maze(height, width):
    maze = []
    for row in range(height):
        maze_row = []
        for col in range(width):
            maze_row.append(Node((row,col), height, width))
        maze.append(maze_row)
    explored = set()
    frontier = [[maze[0][0]]]
    while frontier:
        if random.choice([0, 1]):
            frontier.sort(key=len, reverse=True)
        path = frontier.pop(0)
        s = path[-1]
        for state, action in s.get_possible_routes():
            state_node = maze[state[0]][state[1]]
            if state_node not in explored:
                s.walls[action] = NO_WALL
                state_node.walls[opposite(action)] = NO_WALL
                explored.add(state_node)
                frontier.append(path + [action, state_node])
            else:
                s.walls[action] = WALL
                state_node.walls[opposite(action)] = WALL
    print_maze(maze)
#generate_maze(10, 10)

def find_shortest_path(node_maze, start, end):
    explored = set()
    if start == end:
        return [start]
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for state, action in s.get_possible_routes():
            state_node = node_maze[state[0]][state[1]]
            if state_node not in explored:
                explored.add(state_node)
                if state_node == end:
                    return path + [action, state_node]
                frontier.append(path + [action, state_node])

def solve_maze(maze, start, end):
    maze_list = maze.split('\n')
    height = len(maze_list) / 2
    width = maze_list[0].count('+') - 1
    node_maze = []
    for row in range(height):
        node_row = []
        for col in range(width):
            node = Node((row, col), height, width)
            node_row.append(node)
        node_maze.append(node_row)
    # convert he maze string to a maze of nodes
    for i, line in enumerate(maze_list):
        if i / 2 == height or i == 0:
            continue
        if i % 2:
            # vertical walls
            for j in range(0, len(line), 4):
                if j / 4 >= width:
                    continue
                if line[j: j + 4] == '|   ':
                    node_maze[i / 2][j / 4].walls['left'] = WALL
                    if j / 4 - 1 >= 0:
                        node_maze[i / 2][j / 4 - 1].walls['right'] = WALL
        else:
            # horizontal walls
            for j, wall_string in enumerate(line.split('+')[1:-1]):
                if wall_string == '---':
                    node_maze[i / 2][j].walls['top'] = WALL
                    if i / 2 - 1 >= 0:
                        node_maze[i / 2 - 1][j].walls['bottom'] = WALL
    routes = find_shortest_path(node_maze, node_maze[start[0]][start[1]], node_maze[end[0]][end[1]])
    print_maze(node_maze, routes)

solve_maze(sample_maze, (0, 0), (4, 4))
