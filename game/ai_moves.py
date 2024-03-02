# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 16:50:11 2024

@author: Admin
"""
import pandas as pd
import numpy as np
import random

df = pd.read_csv("outcomes - Copy.csv",engine='pyarrow').astype('int8', errors='ignore')

win_first = df[(df.iloc[:,9]==1) & (df.iloc[:,10]==1)].drop(['score','first'],axis=1).astype('int8', errors='ignore')
win_notfirst = df[(df.iloc[:,9]==1) & (df.iloc[:,10]==0)].drop(['score','first'],axis=1).astype('int8', errors='ignore')
lost_first = df[(df.iloc[:,9]==-1) & (df.iloc[:,10]==1)].drop(['score','first'],axis=1).astype('int8', errors='ignore')
lost_notfirst = df[(df.iloc[:,9]==-1) & (df.iloc[:,10]==0)].drop(['score','first'],axis=1).astype('int8', errors='ignore')
draw = df[df.iloc[:,9]==0].drop(['score','first'],axis=1).astype('int8', errors='ignore').astype('int8', errors='ignore')

move_sequence=[]
synth_board=[11,12,13,21,22,23,31,32,33]
actual_move=0

def sequence():
    global move_sequence
    return move_sequence

def prev_move(move):
    move_sequence.append(move)

def transpose_and_save(move_sequence,ai_first,score,input_df,output_path):
    input_df=pd.read_csv(input_df)
    while len(move_sequence)<9:
        move_sequence.append(0)
        if len(move_sequence)==9:
            break

    if ai_first==True:
        x=1
    else:
        x=0
    move_sequence.append(score)
    move_sequence.append(x)
    if input_df[(input_df.iloc[:, :len(move_sequence)].values == move_sequence).all(axis=1)].empty==True:
        print('outcome doesnt exists:  '+str(move_sequence[9]))
        rotate1 = {
            11: 31, 12: 21, 13: 11,
            21: 32, 22: 22, 23: 12,
            31: 33, 32: 23, 33: 13
        }

        rotate2 = {
            11: 33, 12: 32, 13: 31,
            21: 23, 22: 22, 23: 21,
            31: 13, 32: 12, 33: 11
        }

        rotate3 = {
            11: 13, 12: 23, 13: 33,
            21: 12, 22: 22, 23: 32,
            31: 11, 32: 21, 33: 31
        }

        axis0 = {
            11: 13, 12: 12, 13: 11,
            21: 23, 22: 22, 23: 21,
            31: 33, 32: 32, 33: 31
        }

        axis1 = {
            11: 33, 12: 23, 13: 13,
            21: 32, 22: 22, 23: 12,
            31: 31, 32: 21, 33: 11
        }

        axis2 = {
            11: 31, 12: 32, 13: 33,
            21: 21, 22: 22, 23: 23,
            31: 11, 32: 12, 33: 13
        }

        axis3 = {
            11: 11, 12: 21, 13: 31,
            21: 12, 22: 22, 23: 32,
            31: 13, 32: 23, 33: 33
        }

        df_dict={
        0 : move_sequence,
        1 : [rotate1.get(item, item) for item in move_sequence],
        2 : [rotate2.get(item, item) for item in move_sequence],
        3 : [rotate3.get(item, item) for item in move_sequence],
        4 : [axis0.get(item, item) for item in move_sequence],
        5 : [axis1.get(item, item) for item in move_sequence],
        6 : [axis2.get(item, item) for item in move_sequence],
        7 : [axis3.get(item, item) for item in move_sequence]
        }

        df = pd.DataFrame.from_dict(df_dict).transpose()
        df.columns = [f'm{i}' for i in range(1, 10)] + ['score', 'first']
        df=pd.concat([input_df,df],ignore_index=True)
        df.to_csv(output_path,index=False)
    else:
        print('outcome already exists: '+str(move_sequence[9]))

def restart():
    global actual_move
    global move_sequence
    global previous_move
    global win_first
    global win_notfirst
    global lost_first
    global lost_notfirst
    global draw
    actual_move=0
    move_sequence=[]
    previous_move=None
    win_first = df[(df.iloc[:,9]==1) & (df.iloc[:,10]==1)].drop(['score','first'],axis=1)
    win_notfirst = df[(df.iloc[:,9]==1) & (df.iloc[:,10]==0)].drop(['score','first'],axis=1)
    lost_first = df[(df.iloc[:,9]==-1) & (df.iloc[:,10]==1)].drop(['score','first'],axis=1)
    lost_notfirst = df[(df.iloc[:,9]==-1) & (df.iloc[:,10]==0)].drop(['score','first'],axis=1)
    draw = df[df.iloc[:,9]==0].drop(['score','first'],axis=1)

def next_move():
    global actual_move
    actual_move+=1

#sort by frequency for a column, the most frequent on top
def sort_df(df, column_index):
    values = list(set(df.iloc[:, column_index]))
    df = df.astype(int, errors='ignore') #do not remove this line
    for value in values:
        count_column_name = f'{int(value)}'
        df[count_column_name] = 0

    for index, row in df.iterrows():
        if row[column_index] == value:
            df[count_column_name] += 1
    columns = ['m1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9']
    result = pd.DataFrame(columns=columns)
    for i,value in enumerate(values):
        most_frequent = int(df.iloc[0, 9:].idxmax())
        df_i = df[df.iloc[:, column_index] == most_frequent]
        result=pd.concat([result,df_i],ignore_index=True)
        df=df.drop(columns=[str(most_frequent)])
    values = [str(int(x)) for x in values]
    result = result.drop(columns=values)
    return result

def sort_df_by_zeros(df):
    df['zeros_count'] = (df == 0).sum(axis=1)
    df_sorted = df.sort_values(by='zeros_count', ascending=False)
    df_sorted = df_sorted.drop(columns='zeros_count')
    return df_sorted

#check if there are rows matching moves sequences
def filter_df(df, move_sequence):
    # Iterate over each row
    matching_rows = []
    for i, row in df.iterrows():
        # Shorten the row to the length of move_sequence
        shortened_row = row[:len(move_sequence)].tolist()

        # Check if the shortened row matches move_sequence
        if shortened_row == move_sequence:
            matching_rows.append(row.tolist())

    # Create a DataFrame from the matching rows
    filtered_df = pd.DataFrame(matching_rows, columns=df.columns)

    return filtered_df

#sort by row length, treating 0 as nan, the shortest on top, removes 0 as nan
def sort_by_nan(df):
    df.replace(0, np.nan, inplace=True)
    df.dropna(axis=0, how='all', inplace=True)
    df['RowLength'] = df.apply(lambda row: len(row), axis=1)
    df['NaNCount'] = df.apply(lambda row: row.isna().sum(), axis=1)
    sorted_df = df.sort_values(by=['RowLength', 'NaNCount'], ascending=[False, False])
    sorted_df = sorted_df.drop(columns=['RowLength', 'NaNCount'])
    return sorted_df

#only output rows with specified length
def sort_by_length(df, specified_length):
    filtered_df = df[df.apply(lambda row: len([val for val in row if val != 0 and not pd.isna(val)]) == specified_length, axis=1)]
    return filtered_df

def ai_move(ai_first,board):
    global win_first
    global win_notfirst
    global lost_first
    global lost_notfirst
    global draw
    global synth_board
    global move_sequence
    global actual_move

    flat_board=[x for x in board.values.flatten().tolist()]
    legal_moves=[x for x in flat_board if isinstance(x, int)]

    if actual_move == 0:
        print('move0')
        if ai_first == True:
            # print('move0 ai first')
            if win_first.empty == False:
                # print('win_first exists')
                win_first=sort_df_by_zeros(win_first)
                move = win_first.iloc[0,0]
                move_sequence.append(move)
                actual_move +=1
                return move
            elif lost_notfirst.empty == False:
                # print('lost_notfirst exists')
                lost_notfirst=sort_df_by_zeros(lost_notfirst)
                move = lost_notfirst.iloc[0,0]
                move_sequence.append(move)
                actual_move+=1
                return move
            elif draw.empty == False:
                # print('draw exists')
                draw=sort_df(draw,0)
                move = draw.iloc[0,0]
                move_sequence.append(move)
                actual_move+=1
                return move
            elif lost_first.empty==False or win_notfirst.empty==False:
                # print('lost_first or win_notfirst exists')
                if lost_first.empty==True:
                    # print('case1')
                    lost_first = sort_df(lost_first,0)
                    win_notfirst = sort_df(win_notfirst,0)
                    best_moves = list(set(legal_moves)-set([win_notfirst.iloc[0,0]]))

                elif win_notfirst.empty==True:
                    # print('case2')
                    lost_first = sort_df(lost_first,0)
                    best_moves = list(set(legal_moves)-set([lost_first.iloc[0,0]]))

                else:
                    # print('case3')
                    lost_first = sort_df(lost_first,0)
                    win_notfirst = sort_df(win_notfirst,0)
                    best_moves = list(set(legal_moves)-set([lost_first.iloc[0,0]])-set([win_notfirst.iloc[0,0]]))

                    if len(best_moves)>0:
                        # print('best moves case')
                        best_move = random.randint(1,len(best_moves))
                        best_moves_dict = {i+1: move for i, move in enumerate(best_moves)}
                        best_move = best_moves_dict[best_move]
                        move_sequence.append(best_move)
                        actual_move+=1
                        print(move_sequence)
                        return best_move
                    else:
                        # print('random move')
                        best_move = random.randint(1,len(legal_moves))
                        best_moves_dict = {i+1: move for i, move in enumerate(legal_moves)}
                        best_move = best_moves_dict[best_move]
                        move_sequence.append(best_move)
                        actual_move+=1
                        return best_move
            else:
                # print('no options random move')
                best_moves = legal_moves
                best_move = random.randint(1,len(best_moves))
                best_moves_dict={i+1: move for i, move in enumerate(best_moves)}
                best_move=best_moves_dict[best_move]
                move_sequence.append(best_move)
                actual_move+=1
                return best_move

        elif ai_first==False:
            print('Ai logic error - player move sequence')
    else:
        if ai_first == True:
            # print('move>0 ai first')
            # print('move sequence: ',str(move_sequence))
            # print('actual move: '+str(actual_move))
            # print(move_sequence)
            # print(win_first)

            if len(legal_moves) == 1:
                return int(legal_moves[0])
            
            # 33% chance for blocking the opponent
            x = random.randint(1,3) == 1

            win_first=filter_df(win_first, move_sequence)

            if win_first.empty == True and ((set(legal_moves) - set(win_first.iloc[:, actual_move].values.flatten())) == set(legal_moves)) and not x:
                lost_first=filter_df(lost_first,move_sequence)
                if lost_first.empty:
                    draw=filter_df(draw,move_sequence)
                    if draw.empty:
                        lost_notfirst=filter_df(lost_notfirst, move_sequence)
                        win_notfirst=filter_df(win_first, move_sequence)
            if x == False:
                lost_first = filter_df(lost_first, move_sequence)
                win_notfirst = filter_df(win_first, move_sequence)
                draw = filter_df(draw, move_sequence)

            #if there is a non empty data frame and there is a possibility to move at all
            if win_first.empty == False and not((set(legal_moves) - set(win_first.iloc[:, actual_move].values.flatten())) == set(legal_moves)) and not x:
                print('win first')
                # print(actual_move)
                win_first=sort_df_by_zeros(win_first)
                #make a move that is possibly the fastest to win and legal
                loop_end=False
                x=-1
                while loop_end==False:
                    x+=1
                    move=win_first.iloc[x,actual_move]
                    # print(move)
                    if move in legal_moves:
                        break
                # print('loop exit: '+str(move))
                move_sequence.append(move)
                actual_move+=1
                return move

            #elif there is a non empty data frame and there is a possibility to move at all
            elif lost_notfirst.empty == False and not(set(legal_moves)-set(lost_notfirst.iloc[:,actual_move].values.flatten())==set(legal_moves)) and not x:
                print('legal move for lost not first')
                lost_notfirst = sort_df_by_zeros(lost_notfirst)
                loop_end=False
                x=-1
                while loop_end==False:
                    x+=1
                    move=lost_notfirst.iloc[x,actual_move]
                    # print(1)
                    if move in legal_moves:
                        break
                # print('loop exit: '+str(move))
                move_sequence.append(move)
                actual_move+=1
                return move

            elif lost_first.empty==False or win_notfirst.empty==False:
                lost_first = sort_df(lost_first, 0)
                win_notfirst = sort_df(win_notfirst, 0)
                print('checking for worst moves')
                combined_lost = sort_by_nan(pd.concat([lost_first,win_notfirst], ignore_index=True))

                if len(combined_lost.iloc[0])==len(move_sequence)+2:  #if there is a chance to lose in the opponent turn
                    print('blocking')
                    worst_moves=list(set(sort_by_length(combined_lost,len(move_sequence)+2).iloc[:3,actual_move+1].values.flatten())) # blocking opponent move
                    best_moves = list(x for x in worst_moves if x in legal_moves)
                    if not best_moves == []:
                        best_move = random.randint(1,len(best_moves))
                        best_moves_dict={i+1: move for i, move in enumerate(best_moves)}
                        best_move=best_moves_dict[best_move]
                        move_sequence.append(best_move)
                        actual_move+=1
                        # print('legal move from best: '+str(best_move))
                        return best_move
                    else:
                        move=random.randint(1,len(legal_moves))
                        moves_dict={i+1: move for i, move in enumerate(legal_moves)}
                        move=moves_dict[move]
                        move_sequence.append(move)
                        actual_move+=1
                        # print('random legal: '+str(move))
                        return move

                else:
                    print('general worst moves case')
                    worst_moves=set(sort_by_nan(combined_lost).iloc[:3,actual_move].values.flatten())
                    best_moves = list(set(legal_moves)-worst_moves)
                    if not best_moves == []:
                        best_move = random.randint(1,len(best_moves))
                        best_moves_dict={i+1: move for i, move in enumerate(best_moves)}
                        best_move=best_moves_dict[best_move]
                        move_sequence.append(best_move)
                        actual_move+=1
                        # print('move: '+str(best_move))
                        return best_move
                    else:
                        move=random.randint(1,len(legal_moves))
                        moves_dict={i+1: move for i, move in enumerate(legal_moves)}
                        move=moves_dict[move]
                        move_sequence.append(move)
                        actual_move+=1
                        # print('random legal: '+str(move))
                        return move


            elif not draw.empty and set(legal_moves) - set(draw.iloc[:, actual_move].values.flatten()) != set(legal_moves):
                print('draw legal move')
                draw = sort_df(draw,actual_move)
                loop_end=False
                x=-1
                while loop_end==False and x<3:
                    x+=1
                    move=draw.iloc[x,actual_move]
                    # print(1)
                    if move in legal_moves:
                        break
                # print('loop exit: '+str(move))
                move_sequence.append(move)
                actual_move+=1
                return move

            elif len(legal_moves)>0:
                print('there are no other posibilities, random move')
                # print(legal_moves)
                best_moves = legal_moves
                best_move = random.randint(1,len(best_moves))
                best_moves_dict={i+1: move for i, move in enumerate(best_moves)}
                best_move=best_moves_dict[best_move]
                move_sequence.append(best_move)
                actual_move+=1
                # print('move: '+str(best_move))
                return best_move
            else:
                return 11

        else:
            # print('move>0 ai not first')
            # print('move sequence: ',str(move_sequence))
            # print('actual move: '+str(actual_move))
            # print(filter_df(win_notfirst, move_sequence))

            if len(legal_moves)==1:
                return int(legal_moves[0])

            # 33% chance for blocking the opponent
            x = random.randint(1,3) == 1

            win_notfirst=filter_df(win_notfirst, move_sequence)
            if win_notfirst.empty == True and (set(legal_moves) - set(win_notfirst.iloc[:, actual_move].values.flatten()) == set(legal_moves)) and not x:
                lost_first=filter_df(lost_first,move_sequence)
                if lost_first.empty:
                    draw=filter_df(draw,move_sequence)
                    if draw.empty:
                        lost_notfirst=filter_df(lost_notfirst, move_sequence)
                        win_first=filter_df(win_first, move_sequence)
            if x == False:
                lost_notfirst = filter_df(lost_notfirst, move_sequence)
                win_first = filter_df(win_first, move_sequence)
                draw = filter_df(draw, move_sequence)

            if win_notfirst.empty == False and not(set(legal_moves)-set(win_notfirst.iloc[:,actual_move].values.flatten())==set(legal_moves)) and not x:
                print('win not first not empty and legal move')
                win_notfirst=sort_df_by_zeros(win_notfirst)
                loop_end=False
                x=-1
                while loop_end==False:
                    x+=1
                    move=win_notfirst.iloc[x,actual_move]
                    # print(move)
                    if move in legal_moves:
                        break
                # print('loop exit: '+str(move))
                move_sequence.append(move)
                actual_move+=1
                return move

            elif lost_first.empty == False and not(set(legal_moves)-set(lost_first.iloc[:,actual_move].values.flatten())==set(legal_moves)) and not x:
                print('legal move for lost first')
                lost_first = sort_df_by_zeros(lost_first)
                loop_end=False
                x=-1
                while loop_end==False:
                    x+=1
                    move=lost_first.iloc[x,actual_move]
                    # print(1)
                    if move in legal_moves:
                        break
                # print('loop exit: '+str(move))
                move_sequence.append(move)
                actual_move+=1
                return move

            elif lost_notfirst.empty==False or win_first.empty==False:
                print('checking for worst moves')
                combined_lost = sort_by_nan(pd.concat([lost_notfirst,win_first], ignore_index=True))

                if len(combined_lost.iloc[0])==len(move_sequence)+2:  #if there is a chance to lose in the next turn
                    print('blocking')
                    worst_moves=list(set(sort_by_length(combined_lost,len(move_sequence)+2).iloc[:3,actual_move+1].values.flatten()))
                    best_moves = list(x for x in worst_moves if x in legal_moves)
                    if not best_moves == []:
                        best_move = random.randint(1,len(best_moves))
                        best_moves_dict={i+1: move for i, move in enumerate(best_moves)}
                        best_move=best_moves_dict[best_move]
                        move_sequence.append(best_move)
                        actual_move+=1
                        # print('legal move from best: '+str(best_move))
                        return best_move
                    else:
                        move=random.randint(1,len(legal_moves))
                        moves_dict={i+1: move for i, move in enumerate(legal_moves)}
                        move=moves_dict[move]
                        move_sequence.append(move)
                        actual_move+=1
                        # print('random legal: '+str(move))
                        return move

                else:
                    print('general worst moves case')
                    worst_moves=set(sort_by_nan(combined_lost).iloc[:3,actual_move].values.flatten())
                    best_moves = list(set(legal_moves)-worst_moves)
                    if not best_moves == []:
                        best_move = random.randint(1,len(best_moves))
                        best_moves_dict={i+1: move for i, move in enumerate(best_moves)}
                        best_move=best_moves_dict[best_move]
                        move_sequence.append(best_move)
                        actual_move+=1
                        # print('move: '+str(best_move))
                        return best_move
                    else:
                        move=random.randint(1,len(legal_moves))
                        moves_dict={i+1: move for i, move in enumerate(legal_moves)}
                        move=moves_dict[move]
                        move_sequence.append(move)
                        actual_move+=1
                        # print('random legal: '+str(move))
                        return move

            elif not draw.empty and set(legal_moves) - set(draw.iloc[:, actual_move].values.flatten()) != set(legal_moves):
                print('draw legal move')
                draw = sort_df(draw,actual_move)
                loop_end=False
                x=-1
                while loop_end==False and x<3:
                    x+=1
                    move=draw.iloc[x,actual_move]
                    # print(1)
                    if move in legal_moves:
                        break
                # print('loop exit: '+str(move))
                move_sequence.append(move)
                actual_move+=1
                return move

            elif len(legal_moves)>0:
                print('there are no other possibilities, random move')
                # print(legal_moves)
                best_moves = legal_moves
                best_move = random.randint(1,len(best_moves))
                # print(best_move)
                best_moves_dict={i+1: move for i, move in enumerate(best_moves)}
                # print(best_moves_dict)
                best_move=best_moves_dict[best_move]
                move_sequence.append(best_move)
                actual_move+=1
                # print('move: '+str(best_move))
                return best_move
            else:
                return 11
