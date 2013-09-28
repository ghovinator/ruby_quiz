#!/usr/bin/python
import sys
import random
import copy

xo = ['X', 'O']
turn = 0

def draw_board(board):
    result = """
   |   |  
 %s | %s | %s 
   |   |   
"""
    print result % tuple(board[0]),
    print "-----------",
    print result % tuple(board[1]),
    print "-----------",
    print result % tuple(board[2]),

def create_board():
    board = []
    for row in range(3):
        board_row = []
        for col in range(3):
            board_row.append(' ')
        board.append(board_row)
    return board

def is_winner(board):
    combos = [[board[0][0], board[1][1], board[2][2]],
              [board[2][0], board[1][1], board[0][2]]]
    for row in range(3):
        combos.append(board[row])
        for col in range(3):
            combos.append([board[0][col], board[1][col], board[2][col]])
    for combo in combos:
        if len(set(combo)) == 1 and combo[0] != ' ':
            return combo[0]
    return None

def ask_for_move(board, difficulty):
    global turn, xo
    while(True):
        move = raw_input("Please enter your move(1-9):")
        move = int(move) - 1
        if board[move / 3][move % 3] == ' ':
            board[move / 3][move % 3] = xo[turn]
            break
        print "Spot is already filled!"
    turn = 0 if turn else 1

def possible_moves(board):
    return [(row, col) for row in range(3) for col in range(3) if board[row][col] == ' ']

def can_win(board, moves, turn):
    copy_board = copy.copy(board)
    for move in possible_moves(copy_board):
        copy_board[move[0]][move[1]] = xo[turn]
        if is_winner(copy_board):
            return move
        copy_board[move[0]][move[1]] = ' '
    return None

def hard_cpu_move(board, moves, turn):
    """Don't have to deal with winning or losing moves
    as that is already dealt with."""
    past_moves = 9 - len(moves)
    if past_moves % 2:
        #didn't start
        if past_moves == 1:
            if board[1][1]!= ' ' and (2, 0) in moves:
                return (2, 0)
            else:
                return (1, 1)
        elif past_moves == 3:
            if board[1][1] == xo[0 if turn else 1] and (0, 0) in moves:
                return (0, 0)
            else:
                return (0, 1)
    else:
        #I'm starting first
        if past_moves == 0:
            return (2, 0)
        elif past_moves == 2:
            if board[1][1] != ' ' and (0, 2) in moves:
                return (0, 2)
            else:
                if board[2][1] == ' ' and (2, 2) in moves:
                    return (2, 2)
                elif board[1][0] == ' ' and (0, 0) in moves:
                    return (0, 0)
        elif past_moves == 4:
            # if opponent is in middle square at this point we either
            # won or draw. The draw will be dealt with in the
            # random.choice on the bottom and the win should be dealt
            # with the playing winning moves before this function
            if board[1][1] != xo[0 if turn else 1]:
                if board[0][2] == ' ' and board[1][2] == ' ' and (0, 2) in moves:
                    return (0, 2)
                elif board[0][0] == ' ' and board[1][0] == ' ' and (0, 0) in moves:
                    return (0, 0)
                elif (1, 1) in moves:
                    return (1, 1)
                    
    return random.choice(moves)
            
                

def cpu_move(board, difficulty):
    global turn, xo
    moves = possible_moves(board)
    move = can_win(board, moves, turn)
    if not move:
        move = can_win(board, moves, 0 if turn else 1)
    if not move and difficulty == 'hard':
        move = hard_cpu_move(board, moves, turn)
    elif not move or difficulty == 'easy':
        move = random.choice(moves)
    board[move[0]][move[1]] = xo[turn]
    turn = 0 if turn else 1
    
def play(difficulty):
    board = create_board()
    players = [ask_for_move, cpu_move if difficulty else ask_for_move]
    random.shuffle(players)
    while(True):
        for player in players:
            player(board, difficulty)
            draw_board(board)
            winner = is_winner(board)
            if winner:
                print "%s has won" %winner
                return
            if not possible_moves(board):
                print "Draw game"
                return

def tic_tac_toe(difficulty):
    while(True):
        play(difficulty)
        again = raw_input("Would you like to play again? ")
        if not again or again.strip().lower()[0] == 'n':
            break

if __name__ == "__main__":
    difficulty = sys.argv[1] if len(sys.argv) > 1 else None
    tic_tac_toe(difficulty)
