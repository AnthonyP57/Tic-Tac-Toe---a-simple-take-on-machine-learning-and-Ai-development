# here are game rules and an example game
import pandas as pd
from ai_moves import ai_move,restart,next_move,transpose_and_save,prev_move,sequence
from random_moves_player import random_move
import random
from nn_player import nn_sequence, nn_prev_move, nn_move, nn_restart #transpose_and_save
import time
from datetime import datetime

def show_time():
    current_time_ms = time.time()
    datetime_obj = datetime.utcfromtimestamp(current_time_ms)
    formatted_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return formatted_time

actual_move=0
ai_won = False
random_won = False
isboard_full = False

#define gameboard
board = {"left":[11,21,31],
          "mid":[12,22,32],
          "right":[13,23,33]
          }
board = pd.DataFrame.from_dict(board)
board = pd.DataFrame(board, index=[0,1,2])

#decide who moves first, here ai and nn play
who_moves_first = random.randint(1, 2)
who_moves_dict = {1:"A",2:"N"}
who_moves_first = who_moves_dict[who_moves_first]

def reset_board():
    global board
    board = {"left":[11,21,31],
              "mid":[12,22,32],
              "right":[13,23,33]
              }

    board = pd.DataFrame.from_dict(board)
    board = pd.DataFrame(board, index=[0,1,2])

def is_first(x):
    if x == who_moves_first:
        return True
    else:
        return False

class player:
    def __init__(self, tag, won = False, first = False):
        
        if isinstance(tag,str):
            self.tag = tag
        else:
            print('player tag has to be a string')
        self.first = is_first(tag)
        self.won = won
        
    def decide_if_won(self):
        if all(board["left"] == self.tag) or all(board["mid"] == self.tag) or all(board["right"] == self.tag):
            self.won = True
            return True
        elif board.at[0, "left"] == self.tag and board.at[1, "mid"] == self.tag and board.at[2, "right"] == self.tag or board.at[2, "left"] == self.tag and board.at[1, "mid"] == self.tag and board.at[0, "right"] == self.tag:
            self.won = True
            return True
        elif all((board.iloc[0] == self.tag).values.flatten()) or all((board.iloc[1] == self.tag).values.flatten()) or all((board.iloc[2] == self.tag).values.flatten()):
            self.won = True
            return True
        else:
            self.won = False
            return False

class ai_player(player):
    def move(self):
        return ai_move(self.first,board)

class random_player(player):
    def move(self):
        return random_move(board)

class nn_player(player):
    def move(self):
        return nn_move(self.first,board)

# define players
nn = nn_player(tag = 'N')
ai = ai_player(tag = 'A')
rnd = random_player(tag = 'R')

def is_draw():
    if ai.decide_if_won() == False and rnd.decide_if_won() == False and check_if_board_isfull() == True:
        draw = True
        return draw
    else:
        draw = False
        return draw

def check_if_board_isfull():
    all_values = board.values.flatten()
    isboard_full = not any(isinstance(item, int) for item in all_values)
    if isboard_full==True:
        return True

def score():
    if nn.won == True:
        return 1
    elif rnd.won == True:
        return -1
    elif is_draw() == True:
        return 0

def keep_score(path):
    df=pd.read_csv(path)
    row=[score(),show_time()]
    df=pd.concat([df,pd.DataFrame([row],columns=df.columns)],ignore_index=True)
    df.to_csv(path,index=False)

def game_over():
    if ai.decide_if_won() == True or rnd.decide_if_won() == True:
        return True
    elif is_draw() == True:
        return True
    elif check_if_board_isfull() == True:
        return True
    else:
        return False

restart()
nn_restart()
reset_board()

#play game - an example game of NN vs Ai
if who_moves_first=='N':
  # if statements may not look elegant but they always worked
    print(f'nn first: {nn.first}')

    x = nn.move()
    board.replace(x,rnd.tag,inplace=True)
    prev_move(x) # these two statements are fo ai to keep track of the game
    next_move()
    # print(x)

    y=rnd.move()
    board.replace(y,ai.tag,inplace=True)
    # print(y)
    nn_prev_move(y)

    x = nn.move()
    board.replace(x,rnd.tag,inplace=True)
    prev_move(x)
    next_move()
    # print(x)

    y=rnd.move()
    board.replace(y,ai.tag,inplace=True)
    # print(y)
    nn_prev_move(y)

    x = nn.move()
    board.replace(x,rnd.tag,inplace=True)
    prev_move(x)
    next_move()

    if game_over() == False:
        y = rnd.move()
        board.replace(y, ai.tag, inplace=True)
        nn_prev_move(y)

        if game_over() == False:
            x = nn.move()
            board.replace(x, rnd.tag, inplace=True)
            prev_move(x)
            next_move()

            if game_over() == False:
                y = rnd.move()
                board.replace(y, ai.tag, inplace=True)
                nn_prev_move(y)

                if game_over() == False:
                    x = nn.move()
                    board.replace(x, rnd.tag, inplace=True)
                    prev_move(x)
                    next_move()

elif who_moves_first=='R':
    print(f'ai first:{ai.first}')

    y = rnd.move()
    board.replace(y, ai.tag, inplace=True)
    nn_prev_move(y)
    # print(y)

    x = nn.move()
    board.replace(x, rnd.tag, inplace=True)
    prev_move(x)
    next_move()
    # print(x)

    y = rnd.move()
    board.replace(y, ai.tag, inplace=True)
    nn_prev_move(y)
    # print(y)

    x = nn.move()
    board.replace(x, rnd.tag, inplace=True)
    prev_move(x)
    next_move()

    if game_over() == False:
        y = rnd.move()
        board.replace(y, ai.tag, inplace=True)
        nn_prev_move(y)

        if game_over() == False:
            x = nn.move()
            board.replace(x, rnd.tag, inplace=True)
            prev_move(x)
            next_move()

            if game_over() == False:
                y = rnd.move()
                board.replace(y, ai.tag, inplace=True)
                nn_prev_move(y)

                if game_over() == False:
                    x = nn.move()
                    board.replace(x, rnd.tag, inplace=True)
                    prev_move(x)
                    next_move()

                    if game_over() == False:
                        y = rnd.move()
                        board.replace(y, ai.tag, inplace=True)
                        nn_prev_move(y)

ai.decide_if_won()
rnd.decide_if_won()
check_if_board_isfull()
is_draw()
score()

transpose_and_save(sequence(), ai.first, score(), 'outcomes.csv', 'outcomes.csv')
print(score())
print(show_time())

keep_score('score.csv')
