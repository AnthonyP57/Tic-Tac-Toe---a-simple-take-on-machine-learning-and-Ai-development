# random player returns first available random move, without any further logic
import random

def move():
    random_integer = random.randint(1, 9)
    
    move_dict = {
        1: 11, 2: 12, 3: 13,
        4: 21, 5: 22, 6: 23,
        7: 31, 8: 32, 9: 33
    }
 
    random_move = move_dict[random_integer]
    return random_move

def random_move(board):
    flattened_board = board.values.flatten()
    legal_moves = [x for x in flattened_board if isinstance(x, int)]
    if len(legal_moves) == 1:
        return legal_moves[0]
    
    loop_end = False
    while not loop_end:
        x = move()
        if x in flattened_board:
            loop_end = True
            break
    return x
