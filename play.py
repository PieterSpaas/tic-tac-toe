from tkinter import *
import csv
import random

# Computer plays 'o', player plays 'x'

def player_turn(row, column):

    if buttons[row][column]['text'] == '' and is_winner() is False:
        buttons[row][column]['text'] = 'x'
        if is_winner() is False:
            label.config(text='Computer\'s turn')
            computer_turn()
        elif is_winner() is True:
            label.config(text='Player wins!')
            return
        elif is_winner() == 'Draw':
            label.config(text='Draw!')
            return


def computer_turn():

    global q_table

    possible_moves = empty_spaces()
    if possible_moves == []:
        return

    if q_table is None:
        move = random.choice(possible_moves)
        buttons[move[0]][move[1]]['text'] = 'o'
    else:
        board = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]
        for row in range(3):
            for column in range(3):
                if buttons[row][column]['text'] == 'o':
                    board[row][column] = 1
                elif buttons[row][column]['text'] == 'x':
                    board[row][column] = 2
                else:
                    board[row][column] = 0
        if str(board) not in q_table:
            move = random.choice(possible_moves)
        else:
            move = max(possible_moves, key=lambda x: q_table[str(board)][x[0]][x[1]])
        buttons[move[0]][move[1]]['text'] = 'o'

    if is_winner() is False:
        label.config(text='Player\'s turn')
    elif is_winner() is True:
        label.config(text='Computer wins!')
        return
    elif is_winner() == 'Draw':
        label.config(text='Draw!')
        return


def is_winner():

    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != '':
            for r in range(3):
                for column in range(3):
                    if r == row:
                        buttons[r][column].config(bg='green')
                    else:
                        buttons[r][column].config(bg='red')
            return True

    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != '':
            for row in range(3):
                for col in range(3):
                    if col == column:
                        buttons[row][col].config(bg='green')
                    else:
                        buttons[row][col].config(bg='red')
            return True

    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != '':
        for row in range(3):
            for column in range(3):
                if row == column:
                    buttons[row][column].config(bg='green')
                else:
                    buttons[row][column].config(bg='red')
        return True

    elif buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != '':
        for row in range(3):
            for column in range(3):
                if row + column == 2:
                    buttons[row][column].config(bg='green')
                else:
                    buttons[row][column].config(bg='red')
        return True

    elif empty_spaces() is False:
        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg='yellow')
        return 'Draw'

    else:
        return False


def empty_spaces():

    empty_coord = []

    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] == '':
                empty_coord.append((row, column))

    if len(empty_coord) == 0:
        return False
    else:
        return empty_coord


def new_game():

    global player

    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text='', bg='#F0F0F0')

    player = random.choice(players)

    if player == 'o':
        label.config(text='Computer\'s turn')
        computer_turn()
    else:
        label.config(text='Player\'s turn')


Q_table = {}
with (open('q_table.csv', 'r') as file):
    reader = csv.reader(file)
    for row in reader:
        board = row[0]
        values = eval(row[1])
        Q_table[board] = values


ttt = Tk()
ttt.title('Tic Tac Toe')

q_table = Q_table

players = ['x', 'o']
player = random.choice(players)

label = Label(font=('arial', 40))
label.pack(side='top')

restart_button = Button(text='Restart', font=('arial', 20), command=new_game)
restart_button.pack(side='top')

frame = Frame()
frame.pack()

buttons = [[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]]

for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(frame, text='', font=('arial', 40), width=5, height=2,
                                      command=lambda row=row, column=column: player_turn(row, column))
        buttons[row][column].grid(row=row, column=column)

if player == 'o':
    label.config(text='Computer\'s turn')
    computer_turn()
else:
    label.config(text='Player\'s turn')

ttt.mainloop()