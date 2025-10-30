import random


def empty_spaces(board):

    empty_coord = []

    for row in range(3):
        for column in range(3):
            if board[row][column] == 0:
                empty_coord.append((row, column))

    if len(empty_coord) == 0:
        return False
    else:
        return empty_coord


def is_winner(board, player):

    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True

    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] == player:
            return True

    if board[0][0] == board[1][1] == board[2][2] == player:
        return True

    elif board[0][2] == board[1][1] == board[2][0] == player:
        return True

    else:
        return False


def learning_move(board, explore_rate, q_table):

    possible_moves = empty_spaces(board)

    if random.random() < explore_rate or str(board) not in q_table:
        return random.choice(possible_moves)
    else:
        return max(possible_moves, key=lambda x: q_table[str(board)][x[0]][x[1]])


def table_move(board, table=None):

    possible_moves = empty_spaces(board)

    if table is None or str(board) not in table:
        return random.choice(possible_moves)
    else:
        return max(possible_moves, key=lambda x: table[str(board)][x[0]][x[1]])


def train(number_games=int(1e5), learning_rate=0.2, discount_factor=0.9, explore_rate=1.0,
explore_rate_min=0.1, explore_rate_decay=0.999, player1_table=None, player2_table=None):

    if player1_table is None:
        q_table = {}
    else:
        q_table = player1_table

    for game in range(number_games):
        current_board = [[0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]]
        first_player = 1 if random.random() < 0.5 else 2

        if first_player == 2:
            move = table_move(current_board, player2_table)
            current_board[move[0]][move[1]] = 2

        for k in range(9):
            if str(current_board) not in q_table:
                q_table[str(current_board)] = [[0, 0, 0],
                                               [0, 0, 0],
                                               [0, 0, 0]]

            move = learning_move(current_board, explore_rate, q_table)
            new_board = [x[:] for x in current_board]
            new_board[move[0]][move[1]] = 1

            if is_winner(new_board, 1):
                reward = 1
            elif empty_spaces(new_board) is False:
                reward = 0.1
            else:
                move2 = table_move(new_board, player2_table)
                new_board[move2[0]][move2[1]] = 2
                if is_winner(new_board, 2):
                    reward = -1
                elif empty_spaces(new_board) is False:
                    reward = 0.1
                else:
                    reward = 0

            if str(new_board) not in q_table:
                q_table[str(new_board)] = [[0, 0, 0],
                                           [0, 0, 0],
                                           [0, 0, 0]]

            # Update the Q-table value according to the Bellman equation
            q_table[str(current_board)][move[0]][move[1]] += learning_rate * (
                        reward +
                        discount_factor * max((max(d) for d in q_table[str(new_board)])) -
                        q_table[str(current_board)][move[0]][move[1]])

            if reward != 0:
                break

            current_board = [x[:] for x in new_board]

        explore_rate = max(explore_rate_min, explore_rate_decay * explore_rate)

    return q_table


def test(number_games=int(1e5), player1_table=None, player2_table=None):
    wins = 0
    draws = 0
    losses = 0

    for game in range(number_games):
        current_board = [[0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]]
        current_player = 1 if random.random() < 0.5 else 2

        for k in range(9):

            if current_player == 2:
                move = table_move(current_board, player2_table)
                current_board[move[0]][move[1]] = 2
                if is_winner(current_board, 2):
                    losses += 1
                    break
                elif empty_spaces(current_board) is False:
                    draws += 1
                    break
                else:
                    current_player = 1

            else:
                move = table_move(current_board, player1_table)
                current_board[move[0]][move[1]] = 1
                if is_winner(current_board, 1):
                    wins += 1
                    break
                elif empty_spaces(current_board) is False:
                    draws += 1
                    break
                else:
                    current_player = 2

    return wins, draws, losses

