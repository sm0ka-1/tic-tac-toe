from tkinter import *

TITLE_FONT = "Ink Free"
TEXT_FONT = "8514oem"
BG_COLOUR = "lawn green"
BUTTON_COLOUR = "PaleGreen1"
CELL_SIZE = 117
CANVAS_SIZE = CELL_SIZE*3


# ------------------------------------- GAME LOGIC ------------------------------------- #

board = [[None]*3 for _ in range(3)]
starting_turn = "X"
turn = starting_turn
game_active = True

def check_winner():
    global board, turn
    # Row and Columns
    for i in range(3):
        if board[i][0]==board[i][1]==board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i]==board[1][i]==board[2][i] and board[0][i] is not None:
            return board[0][i]
    # Diagonals
    if board[0][0]==board[1][1]==board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2]==board[1][1]==board[2][0] and board[0][2] is not None:
        return board[0][2]
    # Tie
    if all(all(cell is not None for cell in row) for row in board):
        return "Tie"
    return None


def canvas_click(event):
    global turn, board, game_active
    if not game_active:
        return

    x, y = event.x, event.y
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    if board[row][col] is None:
        board[row][col] = turn
        canvas.create_text(col*CELL_SIZE + CELL_SIZE//2, row*CELL_SIZE + CELL_SIZE//2, text=turn, font=(TITLE_FONT, 67, "bold"), fill="white", tags="xo")
        winner = check_winner()
        if winner:
            game_active = False
            if winner=="X":
                playerX_score.config(text=str(int(playerX_score.cget("text"))+1))
                turn_label.config(text=f"Player X wins!")
            elif winner=="O":
                playerO_score.config(text=str(int(playerO_score.cget("text"))+1))
                turn_label.config(text="Player O wins!")
            elif winner=="Tie":
                turn_label.config(text="Tie!")
        else:
            turn = "O" if turn=="X" else "X"
            turn_label.config(text=f"Turn: {turn}")



def restart_score():
    playerX_score.config(text="0")
    playerO_score.config(text="0")
    play_again()


def play_again():
    global board, starting_turn, turn, game_active
    board = [[None]*3 for _ in range(3)]
    starting_turn = "O" if starting_turn == "X" else "X"
    turn = starting_turn
    game_active = True
    canvas.delete("xo")
    turn_label.config(text=f"Turn: {turn}")



# -------------------------------------- UI SETUP -------------------------------------- #

window = Tk()
window.title("Tic Tac Toe Game")
window.config(padx=110, pady=30, bg=BG_COLOUR)

# Title
title = Label(text="Tic Tac Toe", font=(TITLE_FONT, 60, "bold"), bg=BG_COLOUR, fg="black")
title.grid(column=0, columnspan=3, row=0, pady=10)

# Board
canvas = Canvas(width=CANVAS_SIZE, height=CANVAS_SIZE, bg=BG_COLOUR, highlightthickness=0)
canvas.grid(column=0, row=1, rowspan=16, pady=30, sticky=N+W)

window.grid_columnconfigure(1, minsize=70)

# Score
score_label = Label(text="SCORE", font=(TEXT_FONT, 30, "normal"), bg=BG_COLOUR, fg="black")
score_label.grid(column=2, columnspan=2, row=1)

playerX_label = Label(text="Player X:", font=(TEXT_FONT, 20, "normal"), bg=BG_COLOUR, fg="black")
playerX_label.grid(column=2, row=2, sticky=W)

playerO_label = Label(text="Player O:", font=(TEXT_FONT, 20, "normal"), bg=BG_COLOUR, fg="black")
playerO_label.grid(column=2, row=3, sticky=W)

playerX_score = Label(text="0", font=(TEXT_FONT, 20, "normal"), bg=BG_COLOUR, fg="black")
playerX_score.grid(column=3, row=2, sticky=E)

playerO_score = Label(text="0", font=(TEXT_FONT, 20, "normal"), bg=BG_COLOUR, fg="black")
playerO_score.grid(column=3, row=3, sticky=E)

turn_label = Label(text="Turn: X", font=(TEXT_FONT, 23, "bold"), bg=BG_COLOUR, fg="white")
turn_label.grid(column=2, columnspan=2, row=8)

#Buttons
restart_score_button = Button(text="Restart Score", command=restart_score, font=(TEXT_FONT, 20, "normal"), bg=BUTTON_COLOUR)
restart_score_button.grid(column=2, columnspan=2, row=5, sticky=N+W+E)

play_again_button = Button(text="PLAY AGAIN", command=play_again, font=(TEXT_FONT, 23, "bold"), bg=BUTTON_COLOUR, height=2)
play_again_button.grid(column=2, columnspan=2, row=12, sticky=W+E)


# ------------------------------------- GAME START ------------------------------------- #

def draw_grid():
    for i in range(1,3):
        canvas.create_line(CELL_SIZE*i, 0, CELL_SIZE*i, CANVAS_SIZE, width=3, fill="black")
        canvas.create_line(0, CELL_SIZE*i, CANVAS_SIZE, CELL_SIZE*i, width=3, fill="black")

draw_grid()

canvas.bind("<Button-1>", canvas_click)

window.mainloop()