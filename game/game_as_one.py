#can be used not to import players

import joblib
import pandas as pd
import random

move_sequence=[]
nn_first=False

board = {"left":[11,21,31],
          "mid":[12,22,32],
          "right":[13,23,33]
          }
board = pd.DataFrame.from_dict(board)
board = pd.DataFrame(board, index=[0,1,2])

mlp_regressor = joblib.load('mlp_regressor_model_lbgs1_nodraw.joblib')

def nn_restart():
    global move_sequence
    move_sequence = []

def nn_sequence():
    global move_sequence
    return move_sequence

def nn_prev_move(move):
    move_sequence.append(move)

def transpose_and_save(move_sequence, nn_first, score, input_df, output_path):
    input_df = pd.read_csv(input_df)
    while len(move_sequence) < 9:
        move_sequence.append(0)
        if len(move_sequence) == 9:
            break

    if nn_first == True:
        x = 1
    else:
        x = 0
    move_sequence.append(score)
    move_sequence.append(x)
    if input_df[(input_df.iloc[:, :len(move_sequence)].values == move_sequence).all(axis=1)].empty == True:
        print('outcome doesnt exists:  ' + str(move_sequence[9]))
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

        df_dict = {
            0: move_sequence,
            1: [rotate1.get(item, item) for item in move_sequence],
            2: [rotate2.get(item, item) for item in move_sequence],
            3: [rotate3.get(item, item) for item in move_sequence],
            4: [axis0.get(item, item) for item in move_sequence],
            5: [axis1.get(item, item) for item in move_sequence],
            6: [axis2.get(item, item) for item in move_sequence],
            7: [axis3.get(item, item) for item in move_sequence]
        }

        df = pd.DataFrame.from_dict(df_dict).transpose()
        df.columns = [f'm{i}' for i in range(1, 10)] + ['score', 'first']
        df = pd.concat([input_df, df], ignore_index=True)
        df.to_csv(output_path, index=False)
    else:
        print('outcome already exists: ' + str(move_sequence[9]))

def nn_move(nn_first,board):
    global move_sequence
    global mlp_regressor

    flat_board=[x for x in board.values.flatten().tolist()]
    legal_moves=[x for x in flat_board if isinstance(x, int)]

    scores_dict={}
    scores=[]
    for move in legal_moves:
        move_seq=move_sequence.copy()
        move_seq.append(move)
        # print(move_sequence)
        while len(move_seq) < 9:
            move_seq.append(0)
            if len(move_sequence)==9:  #dont touch
                break
        if nn_first == True:
            move_seq.append(1)
        else:
            move_seq.append(0)
        # print(move_seq)
        move_seq = pd.DataFrame([move_seq],columns=['m1','m2','m3','m4','m5','m6','m7','m8','m9','first'])
        # print(move_seq)
        score = mlp_regressor.predict(move_seq)
        scores_dict[score.item()]=move
        scores.append(score.item())

    # print(scores_dict)
    best_score=max(scores)
    best_move=scores_dict[best_score]
    # print(best_move)
    move_sequence.append(best_move)
    return best_move

"""nn player above"""


import numpy as np

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

            x = random.randint(1,3) == 1

            win_first=filter_df(win_first, move_sequence)

            if win_first.empty == True and ((set(legal_moves) - set(win_first.iloc[:, actual_move].values.flatten())) == set(legal_moves)) and x:
                lost_first=filter_df(lost_first,move_sequence)
                if lost_first.empty:
                    draw=filter_df(draw,move_sequence)
                    if draw.empty:
                        lost_notfirst=filter_df(lost_notfirst, move_sequence)
                        if lost_notfirst.empty:
                            win_notfirst=filter_df(win_first, move_sequence)
            if x == False:
                lost_first = filter_df(lost_first, move_sequence)
                win_notfirst = filter_df(win_first, move_sequence)
                draw = filter_df(draw, move_sequence)

            #if there is a non empty data frame and there is a possibility to move at all
            if win_first.empty == False and not((set(legal_moves) - set(win_first.iloc[:, actual_move].values.flatten())) == set(legal_moves)) and x:
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
            elif lost_notfirst.empty == False and not(set(legal_moves)-set(lost_notfirst.iloc[:,actual_move].values.flatten())==set(legal_moves)) and x:
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

            x = random.randint(1,3) == 1

            win_notfirst=filter_df(win_notfirst, move_sequence)
            if win_notfirst.empty == True and (set(legal_moves) - set(win_notfirst.iloc[:, actual_move].values.flatten()) == set(legal_moves)) and x:
                lost_first=filter_df(lost_first,move_sequence)
                if lost_first.empty:
                    draw=filter_df(draw,move_sequence)
                    if draw.empty:
                        lost_notfirst=filter_df(lost_notfirst, move_sequence)
                        if lost_notfirst.empty:
                            win_first=filter_df(win_first, move_sequence)
            if x == False:
                lost_notfirst = filter_df(lost_notfirst, move_sequence)
                win_first = filter_df(win_first, move_sequence)
                draw = filter_df(draw, move_sequence)

            if win_notfirst.empty == False and not(set(legal_moves)-set(win_notfirst.iloc[:,actual_move].values.flatten())==set(legal_moves)) and x:
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

            elif lost_first.empty == False and not(set(legal_moves)-set(lost_first.iloc[:,actual_move].values.flatten())==set(legal_moves)) and x:
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

"""ai above"""

import pygame as pg

#fps cap
fps = 30

#innitiate pygame
pg.init()

#display info
info_object = pg.display.Info()
width = info_object.current_w
height = info_object.current_h
print(width,height)

width = 1600
height = 900
gui_scale = 1

#board for bots
df_board = {"left":[11,21,31],
          "mid":[12,22,32],
          "right":[13,23,33]
          }
df_board = pd.DataFrame.from_dict(df_board)
df_board = pd.DataFrame(df_board, index=[0,1,2])
restart()
nn_restart()

#to translate moves since I used other naming method for bots
board_dict = {1:11,2:12,3:13,4:21,5:22,6:23,7:31,8:32,9:33}
ai_dict =  {11:1,12:2,13:3,21:4,22:5,23:6,31:7,32:8,33:9}

#grid tiles offset
tile_px = round(gui_scale*height/9)
grid_vert = round(gui_scale*height/2.25)

#square class in grid
class Square(pg.sprite.Sprite):
    def __init__(self, x_id, y_id, number):
        super().__init__()
        self.width = tile_px
        self.height = tile_px
        self.x = x_id*self.width - self.width*2 + width/2 #center of screen
        self.y = y_id*self.height+grid_vert
        self.content = ''
        self.number = number
        self.image = blank_img
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = (self.x, self.y)

    def clicked(self, x_val, y_val):
        #what to do when player selected a square - do not touch
        global turn, won, player_first, bot_type, tie
        if self.content == '':
            if self.rect.collidepoint(x_val,y_val) and len(move_sequence) == 8 and player_first == True:
                turn = 'x'
                self.content = turn
                board[self.number] = turn
                self.image = x_img
                self.image = pg.transform.scale(self.image, (self.width, self.height))
                df_board.replace(self.number, 'P', inplace=True)
                check_winner('x')
                check_tie()
                if won == False:
                    tie = True
            elif self.rect.collidepoint(x_val,y_val) and tie == False:
                self.content = turn
                board[self.number] = turn
                if turn == 'x':
                    self.image = x_img
                    self.image = pg.transform.scale( self.image, (self.width, self.height))
                    x = board_dict[self.number]
                    df_board.replace(x, 'P', inplace=True)
                    check_winner('x')
                    x = [x for x in df_board.values.flatten() if not isinstance(x,str)]
                    if x == []:
                        tie = True
                    if won == False and tie == False:
                        turn = 'o'
                        check_winner('o')
                        check_tie()
                        if bot_type == 'ai':
                            botmove()
                        elif bot_type == 'ml':
                            prev_move(x)
                            next_move()
                            x = ai_move(not player_first, df_board)
                            df_board.replace(x, 'M', inplace=True)
                            x = ai_dict[x]
                            for s in squares:
                                if s.number == x:
                                    s.clicked(s.x, s.y)
                                    move_sequence.append(x)
                        elif bot_type == 'nn':
                            print(x)
                            # print(move_sequence[len(move_sequence)-1])
                            if not player_first:
                                nn_prev_move(x)
                                print(x)
                            y = nn_move(not player_first, df_board)
                            df_board.replace(y, 'N', inplace=True)
                            y = ai_dict[y]
                            for s in squares:
                                if s.number == y:
                                    s.clicked(s.x, s.y)
                                    move_sequence.append(y)
                if turn == 'o':
                    check_tie()
                    self.image = o_img
                    self.image = pg.transform.scale( self.image, (self.width, self.height))
                    turn = 'x'
                    check_winner('o')
                    check_tie()
                    if won == False and tie == False:
                        check_winner('x')
                        check_tie()
                print(board)
                return self.number
    def theme_update(self):
        #update grid theme
        global blank_img, x_img, o_img, theme
        if theme == 'doom':
            blank_img = blank_doom
            x_img = x_doom
            o_img = o_doom
            if self.content == '':
                self.image = blank_doom
                self.image = pg.transform.scale(self.image, (self.width, self.height))
                self.rect = self.image.get_rect()
            elif self.content == 'x':
                self.image = x_doom
                self.image = pg.transform.scale(self.image, (self.width, self.height))
                self.rect = self.image.get_rect()
            elif self.content == 'o':
                self.image = o_doom
                self.image = pg.transform.scale(self.image, (self.width, self.height))
                self.rect = self.image.get_rect()
        elif theme == 'candy':
            blank_img = blank_candy
            x_img = x_candy
            o_img = o_candy
            if self.content == '':
                self.image = blank_candy
                self.image = pg.transform.scale(self.image, (self.width, self.height))
                self.rect = self.image.get_rect()
            elif self.content == 'x':
                self.image = x_candy
                self.image = pg.transform.scale(self.image, (self.width, self.height))
                self.rect = self.image.get_rect()
            elif self.content == 'o':
                self.image = o_candy
                self.image = pg.transform.scale(self.image, (self.width, self.height))
                self.rect = self.image.get_rect()
        elif theme == 'org':
            blank_img = blank_original
            x_img = x_original
            o_img = o_original
            if self.content == '':
                self.image = blank_original
                self.image = pg.transform.scale(self.image, (self.width, self.height))
                self.rect = self.image.get_rect()
            elif self.content == 'x':
                self.image = x_original
                self.image = pg.transform.scale(self.image, (self.width, self.height))
                self.rect = self.image.get_rect()
            elif self.content == 'o':
                self.image = o_original
                self.image = pg.transform.scale(self.image, (self.width, self.height))
                self.rect = self.image.get_rect()
class button():
    #it is just a button class
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        #get mouse position
        pos = pg.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

#game screen
def Update():
    global won_animation, tie, won , won_fps, fps, win_img, click_prompt, theme, tie_prompt
    if theme == 'org':
        background = org_bg
        bg_front = org_front
        logo = org_logo
    elif theme == 'doom':
        background = doom_bg
        bg_front = doom_front
        logo = doom_logo
    elif theme == 'candy':
        background = candy_bg
        bg_front = candy_front
        logo = candy_logo

    win.blit(background, (0,0+scroll))
    win.blit(background,(0,-height+scroll))
    win.blit(background, (height*16/9, 0 + scroll))
    win.blit(background, (height*16/9, -height + scroll))
    win.blit(bg_front, (0,0+scroll2))
    win.blit(bg_front,(0,0-height+scroll2))
    win.blit(bg_front, (height*16/9, 0 + scroll2))
    win.blit(bg_front, (height*16/9, 0 - height + scroll2))
    win.blit(logo, ((width/2-16/9*height/2), 0))
    square_group.draw(win)
    square_group.update()
    menu_button.draw(win)
    quit_button.draw(win)
    if tie == True and tie_prompt == True:
        if theme == 'candy':
            win.blit(tie_scr_candy, ((width/2-16/9*height/2), 0))
        else:
            win.blit(tie_scr, ((width / 2 - 16 / 9 * height / 2), 0))
    if won == True and won_animation == True:
        win.blit(win_img, ((width/2-16/9*height/2), 0))
        won_fps += 1
        if won_fps < fps:
            draw_line(startx, starty, endx, endy)
        if won_fps > fps:
            square_group.empty()
            click_prompt = True
            won_fps = 0
            won_animation = False
    if click_prompt == True:
        if theme == 'candy':
            win.blit(click_candy, ((width/2-16/9*height/2), 0))
        else:
            win.blit(click_img, ((width / 2 - 16 / 9 * height / 2), 0))
    pg.display.update()

def display_menu():
    global theme
    if theme == 'org':
        background = org_bg
        bg_front = org_front
        logo = org_logo
    elif theme == 'doom':
        background = doom_bg
        bg_front = doom_front
        logo = doom_logo
    elif theme == 'candy':
        background = candy_bg
        bg_front = candy_front
        logo = candy_logo
    win.blit(background, (0, 0 + scroll))
    win.blit(background, (0, -height + scroll))
    win.blit(background, (height * 16 / 9, 0 + scroll))
    win.blit(background, (height * 16 / 9, -height + scroll))
    win.blit(bg_front, (0, 0 + scroll2))
    win.blit(bg_front, (0, 0 - height + scroll2))
    win.blit(bg_front, (height * 16 / 9, 0 + scroll2))
    win.blit(bg_front, (height * 16 / 9, 0 - height + scroll2))
    win.blit(logo, ((width/2-16/9*height/2), round(height/5)))
    difficulty_button.draw(win)
    about_button.draw(win)
    theme_button.draw(win)
    # quit_button.draw(win)
    pg.display.update()

def display_difficulty():
    global theme
    if theme == 'org':
        background = org_bg
        bg_front = org_front
        logo = org_logo
    elif theme == 'doom':
        background = doom_bg
        bg_front = doom_front
        logo = doom_logo
    elif theme == 'candy':
        background = candy_bg
        bg_front = candy_front
        logo = candy_logo
    win.blit(background, (0, 0 + scroll))
    win.blit(background, (0, -height + scroll))
    win.blit(background, (height * 16 / 9, 0 + scroll))
    win.blit(background, (height * 16 / 9, -height + scroll))
    win.blit(bg_front, (0, 0 + scroll2))
    win.blit(bg_front, (0, 0 - height + scroll2))
    win.blit(bg_front, (height * 16 / 9, 0 + scroll2))
    win.blit(bg_front, (height * 16 / 9, 0 - height + scroll2))
    win.blit(logo,((width/2-16/9*height/2),0))
    ai_button.draw(win)
    nn_button.draw(win)
    ml_button.draw(win)
    # quit_button.draw(win)
    pg.display.update()

def display_theme():
    global theme
    if theme == 'org':
        background = org_bg
        bg_front = org_front
        logo = org_logo
    elif theme == 'doom':
        background = doom_bg
        bg_front = doom_front
        logo = doom_logo
    elif theme == 'candy':
        background = candy_bg
        bg_front = candy_front
        logo = candy_logo
    win.blit(background, (0, 0 + scroll))
    win.blit(background, (0, -height + scroll))
    win.blit(background, (height * 16 / 9, 0 + scroll))
    win.blit(background, (height * 16 / 9, -height + scroll))
    win.blit(bg_front, (0, 0 + scroll2))
    win.blit(bg_front, (0, 0 - height + scroll2))
    win.blit(bg_front, (height * 16 / 9, 0 + scroll2))
    win.blit(bg_front, (height * 16 / 9, 0 - height + scroll2))
    win.blit(logo,((width/2-16/9*height/2),0))
    candy_button.draw(win)
    doom_button.draw(win)
    original_button.draw(win)
    # quit_button.draw(win)
    pg.display.update()

def about():
    global theme
    if theme == 'org':
        background = org_bg
        bg_front = org_front
    elif theme == 'doom':
        background = doom_bg
        bg_front = doom_front
    elif theme == 'candy':
        background = candy_bg
        bg_front = candy_front
    win.blit(background, (0, 0 + scroll))
    win.blit(background, (0, -height + scroll))
    win.blit(background, (height * 16 / 9, 0 + scroll))
    win.blit(background, (height * 16 / 9, -height + scroll))
    win.blit(bg_front, (0, 0 + scroll2))
    win.blit(bg_front, (0, 0 - height + scroll2))
    win.blit(bg_front, (height * 16 / 9, 0 + scroll2))
    win.blit(bg_front, (height * 16 / 9, 0 - height + scroll2))
    if theme == 'candy':
        win.blit(about_candy,(width/2-16/9*height/2,0))
    else:
        win.blit(about_org, (width / 2 - 16 / 9 * height / 2, 0))
    # quit_button.draw(win)
    pg.display.update()

def winner(player):
    global pcmove, move
    for i in range(8):
        if board[winners[i][0]] == player and board[winners[i][1]] == player and board[winners[i][2]] == '':
            pcmove = winners[i][2]
            move = False

        elif board[winners[i][0]] == player and board[winners[i][1]] == '' and board[winners[i][2]] == player:
            pcmove = winners[i][1]
            move = False

        elif board[winners[i][0]] == '' and board[winners[i][1]] == player and board[winners[i][2]] == player:
            pcmove = winners[i][0]
            move = False

def getpos(n1,n2):
    global startx, starty, endx, endy
    for sq in squares:
        if sq.number == n1:
            startx = sq.x
            starty = sq.y

        elif sq.number == n2:
            endx = sq.x
            endy = sq.y

def draw_line(x1,y1,x2,y2):
    pg.draw.line(win, (0, 0, 0), (x1, y1), (x2, y2), 16)
    pg.display.update()
    # time.sleep(1)

def check_winner(player):
    global background, won,startx,starty,endx,endy, won_animation, win_img, theme
    for i in range(8):
        if board[winners[i][0]] == player and board[winners[i][1]] == player and board[winners[i][2]] == player:
            if theme == 'candy':
                win_img = pg.image.load('assets' + '\\' + player.upper() + ' Wins candy.png')
                win_img = pg.transform.scale(win_img,(height*16/9, height)).convert_alpha()
            else:
                win_img = pg.image.load('assets'+'\\' + player.upper() + ' Wins.png')
                win_img = pg.transform.scale(win_img, (height * 16 / 9, height)).convert_alpha()
            won = True
            won_animation = True
            getpos(winners[i][0],winners[i][2])
            break

    if won == True:
        Update()
        # draw_line(startx,starty,endx,endy)
        # square_group.empty()

def botmove():
    global move, background, move_sequence
    move = True
    if move == True:
        winner('o')
    if move == True:
        winner('x')
    if move == True:
        check_danger()
    if move == True:
        checkcenter()
        if move == True:
            checkcorner()
            if move == True:
                checkedge()
    if move == False:
        for s in squares:
            if s.number == pcmove:
                s.clicked(s.x, s.y)
                move_sequence.append(pcmove)
                df_board.replace(pcmove,'A',inplace=True)

def check_tie():
    global tie
    is_tie = [x for x in board if x =='']
    if is_tie == []:
        tie = True
def checkcenter():
    global pcmove, move
    if board[5] == '':
        pcmove = 5
        move = False

def check_danger():
    global move, pcmove

    if board == dangerPos1:
        pcmove = 2
        move = False

    elif board == dangerPos2:
        pcmove = 4
        move = False

    elif board == dangerPos3:
        pcmove = 1
        move = False

    elif board == dangerPos4:
        pcmove = 4
        move = False

    elif board == dangerPos5:
        pcmove = 7
        move = False

    elif board == dangerPos6:
        pcmove = 9
        move = False

    elif board == dangerPos7:
        pcmove = 9
        move = False

    elif board == dangerPos8:
        pcmove = 7
        move = False

    elif board == dangerPos9:
        pcmove = 9
        move = False

def checkcorner():
    global pcmove, move
    for i in range(1,11,2):
        if i != 5:
            if board[i] == '':
                pcmove = i
                move = False
                break

def checkedge():
    global pcmove, move
    for i in range(2,10,2):
        if board[i] == '':
            pcmove = i
            move = False
            break

#diplay
win = pg.display.set_mode((width, height))
pg.display.set_caption('Tic Tac Toe')
icon = pg.image.load('assets\\icon.png')
pg.display.set_icon(icon)
clock = pg.time.Clock()

# images
org_difficulty = pg.image.load('assets\\original_difficulty.png').convert_alpha()
org_theme = pg.image.load('assets\\original_theme.png').convert_alpha()
org_about = pg.image.load('assets\\original_about.png').convert_alpha()

blank_original = pg.image.load('assets\\original_grid.png').convert_alpha()
x_original = pg.image.load('assets\\original_x.png').convert_alpha()
o_original = pg.image.load('assets\\original_o.png').convert_alpha()

blank_img = blank_original
x_img = x_original
o_img = o_original

blank_candy = pg.image.load('assets\\candy_grid.png').convert_alpha()
x_candy = pg.image.load('assets\\candy_x.png').convert_alpha()
o_candy = pg.image.load('assets\\candy_o.png').convert_alpha()

blank_doom = pg.image.load('assets\\doom_grid.png').convert_alpha()
x_doom = pg.image.load('assets\\doom_x.png').convert_alpha()
o_doom = pg.image.load('assets\\doom_o.png').convert_alpha()

doom_bg  = pg.image.load("assets\\tictactoe_doom_theme_bg.png")
doom_bg = pg.transform.scale(doom_bg, (height*16/9, height)).convert_alpha()
doom_front = pg.image.load("assets\\tictactoe_doom_theme_bgfront.png")
doom_front = pg.transform.scale(doom_front, (height*16/9, height)).convert_alpha()
doom_logo = pg.image.load('assets\\tictactoe_doom_theme_logo.png')
doom_logo = pg.transform.scale(doom_logo,(height*16/9, height)).convert_alpha()

org_bg = pg.image.load("assets\\tictactoe_original_theme_bg.png")
org_bg = pg.transform.scale(org_bg, (height*16/9, height)).convert_alpha()
org_front = pg.image.load("assets\\tictactoe_original_theme_bgfront.png")
org_front = pg.transform.scale(org_front, (height*16/9, height)).convert_alpha()
org_logo = pg.image.load('assets\\tictactoe_original_theme_logo.png')
org_logo = pg.transform.scale(org_logo,(height*16/9, height)).convert_alpha()

candy_logo = pg.image.load('assets\\tictactoe_candy_theme_logo.png')
candy_logo = pg.transform.scale(candy_logo,(height*16/9, height)).convert_alpha()
candy_bg = pg.image.load("assets\\tictactoe_candy_theme_bg.png")
candy_bg = pg.transform.scale(candy_bg, (height*16/9, height)).convert()
candy_front = pg.image.load("assets\\tictactoe_candy_theme_bgfront.png")
candy_front = pg.transform.scale(candy_front, (height*16/9, height)).convert_alpha()

tie_scr = pg.image.load('assets\\tie.png')
tie_scr = pg.transform.scale(tie_scr, (height * 16 / 9, height)).convert_alpha()
tie_scr_candy = pg.image.load('assets\\tie_candy.png')
tie_scr_candy = pg.transform.scale(tie_scr_candy, (height * 16 / 9, height)).convert_alpha()

about_org = pg.image.load('assets\\about.png')
about_org = pg.transform.scale(about_org, (height*16/9, height)).convert_alpha()

about_candy = pg.image.load('assets\\about_candy.png')
about_candy = pg.transform.scale(about_candy, (height*16/9, height)).convert_alpha()
candy_menu = pg.image.load('assets\\candy_menu.png').convert_alpha()
candy_quit = pg.image.load('assets\candy_quit.png').convert_alpha()

original_menu = pg.image.load('assets\\original_menu.png').convert_alpha()
original_quit = pg.image.load('assets\\original_quit.png').convert_alpha()

doom_menu = pg.image.load('assets\\doom_menu.png').convert_alpha()
doom_quit = pg.image.load('assets\\doom_quit.png').convert_alpha()

ai_img = pg.image.load('assets\\ai.png').convert_alpha()
nn_img = pg.image.load('assets\\nn.png').convert_alpha()
ml_img = pg.image.load('assets\\ml.png').convert_alpha()

candy_img = pg.image.load('assets\\candy.png').convert_alpha()

doom_img = pg.image.load('assets\\doom.png').convert_alpha()

original_img = pg.image.load('assets\\original.png').convert_alpha()
click_img = pg.image.load('assets\\restart.png')
click_img = pg.transform.scale(click_img, (height*16/9, height)).convert_alpha()

click_candy = pg.image.load('assets\\restart_candy.png')
click_candy = pg.transform.scale(click_candy, (height*16/9, height)).convert_alpha()

win_img = None

# buttons
menu_button = button(round(height / 50), round(height / 50), original_menu, round(0.75 * height / 1080))
difficulty_button = button(round(height/18),round(height/18),org_difficulty,round(height/1080))
theme_button = button(round(height/18),round(height/18+height/9),org_theme,round(height/1080))
about_button = button(round(height/18),round(height/18+2*height/9),org_about,round(height/1080))
quit_button = button(width - round(height / 50) - 33*round(0.75 * height / 1080), round(height / 50), original_quit, round(0.75 * height / 1080))

ai_button = button(width/2 - 0.5*round(368*round(height/1080)), round(height/2.25), ai_img, round(height/1080))
nn_button = button(width/2 - 0.5*round(368*round(height/1080)), round(height/2.25 + 2*height/6), nn_img, round(height/1080))
ml_button = button(width/2 - 0.5*round(368*round(height/1080)), round(height/2.25 + height/6), ml_img, round(height/1080))

candy_button = button(width/2 - 0.5*round(368*round(height/1080)), round(height/2.25 + 2*height/6), candy_img, round(height/1080))
doom_button = button(width/2 - 0.5*round(368*round(height/1080)), round(height/2.25 + height/6), doom_img, round(height/1080))
original_button = button(width/2 - 0.5*round(368*round(height/1080)), round(height/2.25), original_img, round(height/1080))

# grid
square_group = pg.sprite.Group()
squares = []
board = ['' for i in range(10)]
num = 1
for y in range(1,4):
    for x in range(1,4):
        sq = Square(x,y,num)
        square_group.add(sq)
        squares.append(sq)

        num+=1



# game variables - do not touch
menu_screen = False
difficulty_menu = False
theme_screen = False
about_screen = False
run = True
winners = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
dangerPos1 = ['', 'x', '', '', '', 'o', '', '', '', 'x']
dangerPos2 = ['', '', '', 'x', '', 'o', '', 'x', '', '']
dangerPos3 = ['', '', '', 'x', 'x', 'o', '', '', '', '']
dangerPos4 = ['', 'x', '', '', '', 'o', 'x', '', '', '']
dangerPos5 = ['', '', '', '', 'x', 'o', '', '', '', 'x']
dangerPos6 = ['', '', '', '', '', 'o', 'x', 'x', '', '']
dangerPos7 = ['', '', '', '', '', 'o', 'x', '', 'x', '']
dangerPos8 = ['', 'x', '', '', '', 'o', '', '', 'x', '']
dangerPos9 = ['', '', '', 'x', '', 'o', '', '', 'x', '']
startx = 0
starty = 0
endx = 0
endy = 0
won = False
move = True
pcmove = 5
speed = 1
scroll = 0
scroll2 = 0
won_fps = 0
won_animation = False
click_prompt = False
move_sequence=[]
player_first = random.randint(1,2) == 1 #decide at random who moves first
tie_delay = 0
tie_delay_go = False
tie_fps = 0
tie_fps_go = False
tie_prompt = False
paused_position_doom = 0
paused_position_candy = 0
elapsed_doom = 0
elapsed_candy = 0
theme = 'org'

if player_first:
    turn = 'x'
else:
    turn = 'o'

tie = False

bot_type = 'ai'

#game loop
while run:
    clock.tick(fps)

    #scrolling backgrounds
    scroll += speed*height*0.0005
    if abs(scroll) > height:
        scroll = 0

    scroll2 += speed*height*0.001
    if abs(scroll2) > height:
        scroll2 = 0

    if tie == False:
        tie_prompt = False
        # tie sometimes didnt work, it makes sure that when player_first == False tie can be initiated
        if len(move_sequence) == 9 and won == False:
            tie = True
    else:
        #tie screen delay
        if tie_fps_go == False:
            tie_fps += 1
            if tie_fps > fps/4:
                tie_fps = 0
                tie_fps_go = False
                tie_prompt = True

    #delay for user input after tie
    if tie_delay_go == True:
        tie_delay += 1
        if tie_delay > 1:
            tie_delay = 0
            tie_delay_go = False

    if menu_screen == True and difficulty_menu == False and theme_screen == False and about_screen == False:
        display_menu()

    if difficulty_menu == True:
        display_difficulty()

    if theme_screen == True:
        display_theme()

    if about_screen == True:
        about()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and menu_screen == False:
                menu_screen = True
            elif event.key == pg.K_ESCAPE and menu_screen == True and difficulty_menu == False and theme_screen == False and about_screen == False:
                menu_screen = False
            elif event.key == pg.K_ESCAPE and difficulty_menu == True:
                difficulty_menu = False
            elif event.key == pg.K_ESCAPE and theme_screen == True:
                theme_screen = False
            elif event.key == pg.K_ESCAPE and about_screen == True:
                about_screen = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and (won == True or tie == True):
                click_prompt = False
                tie = False
                won = False
                player_first = random.randint(1, 2) == 1
                df_board = {"left": [11, 21, 31],
                            "mid": [12, 22, 32],
                            "right": [13, 23, 33]
                            }
                df_board = pd.DataFrame.from_dict(df_board)
                df_board = pd.DataFrame(df_board, index=[0, 1, 2])
                restart()
                nn_restart()
                move_sequence = []
                square_group = pg.sprite.Group()
                squares = []
                board = ['' for i in range(10)]
                num = 1
                for y in range(1, 4):
                    for x in range(1, 4):
                        sq = Square(x, y, num)
                        square_group.add(sq)
                        squares.append(sq)

                        num += 1
                square_group.draw(win)
                square_group.update()
                Update()

        if menu_button.draw(win) == True:
            menu_screen = True

        if difficulty_menu == True:

            if ml_button.draw(win) == True:
                bot_type = 'ml'
                difficulty_menu = False
                print('ml')

            if nn_button.draw(win) == True:
                bot_type = 'nn'
                difficulty_menu = False
                print('nn')

            if ai_button.draw(win) == True:
                bot_type = 'ai'
                difficulty_menu = False
                print('ai')

        if theme_screen == True:

            if original_button.draw(win):
                theme = 'org'
                menu_button = button(round(height / 50), round(height / 50), original_menu, round(0.75 * height / 1080))
                quit_button = button(width - round(height / 50) - 33 * round(0.75 * height / 1080), round(height / 50), original_quit, round(0.75 * height / 1080))
                pg.mixer.music.pause()
                for s in squares:
                    s.theme_update()
                theme_screen = False

            if doom_button.draw(win):
                theme = 'doom'
                menu_button = button(round(height/50), round(height/50), doom_menu, round(0.75*height/1080))
                quit_button = button(width - round(height / 50) - 33 * round(0.75 * height / 1080), round(height / 50), doom_quit, round(0.75 * height / 1080))
                pg.mixer.music.load('assets\\doom_theme.mp3')
                paused_position_doom = paused_position_doom + elapsed_doom
                if paused_position_doom/1000 > 5*60: # is paused position larger than song length
                    paused_position_doom = paused_position_doom - 5*60*1000 #song length in ms
                print(paused_position_doom/1000)
                pg.mixer.music.play(start=paused_position_doom/1000,loops=-1)
                #update grid theme
                for s in squares:
                    s.theme_update()
                theme_screen = False

            if candy_button.draw(win):
                theme = 'candy'
                menu_button = button(round(height / 50), round(height / 50), candy_menu, round(0.75 * height / 1080))
                quit_button = button(width - round(height / 50) - 33*round(0.75 * height / 1080), round(height / 50), candy_quit, round(0.75 * height / 1080))
                pg.mixer.music.load('assets\\candy_theme.mp3')
                paused_position_candy = paused_position_candy + elapsed_candy
                if paused_position_candy/1000 > 146: # is paused position larger than song length
                    paused_position_candy = paused_position_candy - 146*1000 #song length in ms
                print(paused_position_candy/1000)
                pg.mixer.music.play(start=paused_position_candy/1000,loops=-1)
                #update grid theme
                for s in squares:
                    s.theme_update()
                theme_screen = False

            # update music elapsed time
            if pg.mixer.music.get_busy():
                if theme == 'doom':
                    elapsed_doom = pg.mixer.music.get_pos()
                elif theme == 'candy':
                    elapsed_candy = pg.mixer.music.get_pos()

        if theme_button.draw(win) == True:
            theme_screen = True

        if difficulty_button.draw(win) == True:
            difficulty_menu = True

        if about_button.draw(win) == True:
            about_screen = True

        if quit_button.draw(win) == True:
            run = False

        if tie == True:
            square_group.empty()

        #it works - do not touch
        if event.type == pg.MOUSEBUTTONDOWN and won == True:
            mx, my = pg.mouse.get_pos()
            if my > height - height/5:
                tie = False
                click_prompt = False
                won = False
                player_first = random.randint(1, 2) == 1
                df_board = {"left": [11, 21, 31],
                            "mid": [12, 22, 32],
                            "right": [13, 23, 33]
                            }
                df_board = pd.DataFrame.from_dict(df_board)
                df_board = pd.DataFrame(df_board, index=[0, 1, 2])
                restart()
                nn_restart()
                move_sequence = []
                square_group = pg.sprite.Group()
                squares = []
                board = ['' for i in range(10)]
                num = 1
                for y in range(1, 4):
                    for x in range(1, 4):
                        sq = Square(x, y, num)
                        square_group.add(sq)
                        squares.append(sq)

                        num += 1
                square_group.draw(win)
                square_group.update()
                Update()

        if event.type == pg.MOUSEBUTTONDOWN and tie == True and won == False:
            mx, my = pg.mouse.get_pos()
            if my > height - 0.5 * tile_px - grid_vert:
                click_prompt = False
                won = False
                tie = False
                player_first = random.randint(1, 2) == 1
                df_board = {"left": [11, 21, 31],
                            "mid": [12, 22, 32],
                            "right": [13, 23, 33]
                            }
                df_board = pd.DataFrame.from_dict(df_board)
                df_board = pd.DataFrame(df_board, index=[0, 1, 2])
                restart()
                nn_restart()
                move_sequence = []
                square_group = pg.sprite.Group()
                squares = []
                board = ['' for i in range(10)]
                num = 1
                for y in range(1, 4):
                    for x in range(1, 4):
                        sq = Square(x, y, num)
                        square_group.add(sq)
                        squares.append(sq)

                        num += 1
                tie_delay_go = True
                square_group.draw(win)
                square_group.update()
                Update()


        if event.type == pg.MOUSEBUTTONDOWN and click_prompt == True:
            mx, my = pg.mouse.get_pos()
            if my > height - 0.5 * tile_px - grid_vert:
                click_prompt = False
                won = False
                tie = False
                player_first = random.randint(1, 2) == 1
                df_board = {"left": [11, 21, 31],
                            "mid": [12, 22, 32],
                            "right": [13, 23, 33]
                            }
                df_board = pd.DataFrame.from_dict(df_board)
                df_board = pd.DataFrame(df_board, index=[0, 1, 2])
                restart()
                nn_restart()
                move_sequence = []
                square_group = pg.sprite.Group()
                squares = []
                board = ['' for i in range(10)]
                num = 1
                for y in range(1, 4):
                    for x in range(1, 4):
                        sq = Square(x, y, num)
                        square_group.add(sq)
                        squares.append(sq)

                        num += 1
                tie_delay_go = True
                square_group.draw(win)
                square_group.update()
                Update()

        #only if the grid is reset and so on can the player start another game
        elif event.type == pg.MOUSEBUTTONDOWN and tie == False and won == False and tie_delay_go == False and menu_screen == False and theme_screen == False and difficulty_menu == False and about_screen == False:
            if player_first == True:
                mx, my = pg.mouse.get_pos()
                print(turn)
                for s in squares:
                    clicked_square = s.clicked(mx, my)
                    if clicked_square is not None:
                        move_sequence.append(clicked_square)
                        if len(move_sequence) == 9 and won == False: #just to make sure, it sometimes required another event to update without it
                            tie = True
            else:
                mx, my = pg.mouse.get_pos()
                if my > height - 0.5*tile_px - grid_vert:
                    turn = 'o'
                    if bot_type == 'ai':
                        botmove()
                    elif bot_type == 'ml':
                        x = ai_move(True,df_board)
                        df_board.replace(x,'M',inplace=True)
                        x = ai_dict[x]
                        for s in squares:
                            if s.number == x:
                                s.clicked(s.x, s.y)
                                move_sequence.append(x)
                    elif bot_type == 'nn':
                        move_sequence=[]
                        x = nn_move(True,df_board)
                        df_board.replace(x,'N',inplace=True)
                        x = ai_dict[x]
                        for s in squares:
                            if s.number == x:
                                s.clicked(s.x, s.y)
                                move_sequence.append(x)

                    player_first = True

    # print(clock.get_fps())
    if menu_screen == False and difficulty_menu == False and theme_screen == False:
        Update()
