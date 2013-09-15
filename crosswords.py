#!/usr/bin/python
import sys

def word_len(index, row):
    """Return the length of the word, 0 if none."""
    length = 0
    for i in range(index, len(row)):
        if row[i] == 'X':
            return length
        length += 1
    return length

def is_start(index, row):
    if not index:
        return True
    return True if row[index - 1] == 'X' else False

def create_number_layout(grid):
    """Go from left to right, top to bottom assigning
    numbers."""
    number_layout = [[0] * len(grid[i]) for i in range(len(grid))]
    number = 1
    vert_grid = map(list, zip(*grid))
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'X':
                continue
            # new horizontal word 2 letters or more
            if is_start(col, grid[row]) and word_len(col, grid[row]) > 1:
                number_layout[row][col] = number
                number += 1
            elif is_start(row, vert_grid[col]) and word_len(row, vert_grid[col]) > 1:
                number_layout[row][col] = number
                number += 1
    return number_layout

def is_border(row, col, grid):
    if row == 0 or row == (len(grid) - 1):
        return True
    elif col == 0 or col == (len(grid[0])- 1):
        return True
    return False

def is_neighbor_border(row, col, grid, visited):
    if is_border(row, col, grid):
        return True
    if grid[row][col] == '_' or (row, col) in visited:
        return False
    visited.append((row, col))
    w, x, y, z = False, False, False, False
    if row - 1 >= 0:
        w = is_neighbor_border(row - 1, col, grid, visited)
        if w:
            return True
    if row + 1 < len(grid):
        x = is_neighbor_border(row + 1, col , grid, visited)
        if x:
            return True
    if col - 1 >= 0:
        y = is_neighbor_border(row, col - 1, grid, visited)
        if y:
            return True
    if col + 1 < len(grid[row]):
        z = is_neighbor_border(row, col + 1, grid, visited)
        if z:
            return True
    return w or x or y or z

def display_output(grid, number_layout):
    #output = [[""] * 4 for i in range(len(grid))]
    output = []
    for row in range(len(grid) * 3 + 1):
        output.append([])
        for col in range(len(grid[0]) * 5):
            output[row].append(' ')
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'X':
                if is_border(row, col, grid) or is_neighbor_border(row, col, grid, []):
                    continue
                for i in range(4):
                    for j in range(5):
                        x = row * 3 + i
                        y = col * 4 + j
                        if output[x][y] == ' ':
                            output[x][y] = '#'
            else:
                for i in range(4):
                    for j in range(5):
                        x = row * 3 + i
                        y = col * 4 + j
                        if i == 1 and j == 1 and number_layout[row][col]:
                            # hacky
                            if number_layout[row][col] > 9:
                                output[x][y] = str(number_layout[row][col] / 10)
                                output[x][y + 1] = str(number_layout[row][col] % 10)
                                continue
                            else:
                                output[x][y] = str(number_layout[row][col])
                                continue
                        if not (i == 0 or i == 3 or j == 0 or j == 4):
                            continue
                        if output[x][y] == ' ':
                            output[x][y] = '#'
    for row in output:
        print ''.join(row)

def crosswords(filename):
    try:
        f = open(filename)
    except IOError:
        print "Error: Couldn't find the file"
        return
    grid = []
    for line in f:
        grid.append(line.split())
    number_layout = create_number_layout(grid)
    display_output(grid, number_layout)
    

def test():
    test_grid = [['X', '_', '_', '_', '_', 'X', 'X'],
                 ['_', '_', 'X', '_', '_', '_', '_'],
                 ['_', '_', '_', '_', 'X', '_', '_'],
                 ['_', 'X', '_', '_', 'X', 'X', 'X'],
                 ['_', '_', '_', 'X', '_', '_', '_'],
                 ['X', '_', '_', '_', '_', '_', 'X']]
    number_layout = [[0, 1, 0, 2, 3, 0, 0],
                     [4, 0, 0, 5, 0, 6, 7],
                     [8, 0, 9, 0, 0, 10, 0],
                     [0, 0, 11, 0, 0, 0, 0],
                     [12, 13, 0, 0, 14, 15, 0],
                     [0, 16, 0, 0, 0, 0, 0]]
    create_number_layout(test_grid) == number_layout
    display_output(test_grid, number_layout)
    print '\n\n'
    test_grid1 = [['X', '_', 'X'],
                 ['_', '_', '_']]
    display_output(test_grid1, create_number_layout(test_grid1))


def driver():
    if len(sys.argv) == 1:
        print "Error: Please provide a filename"
        return
    filename = sys.argv[1]
    crosswords(filename)

if __name__ == "__main__":
    #driver()
    test()
