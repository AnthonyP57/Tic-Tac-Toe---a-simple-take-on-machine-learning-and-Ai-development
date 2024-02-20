# nn player returns moves based on a neural network output
import joblib
import pandas as pd

move_sequence=[]
nn_first=False

board = {"left":[11,21,31],
          "mid":[12,22,32],
          "right":[13,23,33]
          }
board = pd.DataFrame.from_dict(board)
board = pd.DataFrame(board, index=[0,1,2])

mlp_regressor = joblib.load('mlp_regressor_model_lbgs1_nodraw.joblib')

#functions same as in ai_moves
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

    #check for the move that will have the highest score (probability of winning
    # print(scores_dict)
    best_score=max(scores)
    best_move=scores_dict[best_score]
    # print(best_move)
    move_sequence.append(best_move)
    return best_move
