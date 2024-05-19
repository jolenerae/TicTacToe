import tkinter as tk
import random
from playsound3 import playsound
import time

# Methods for Two Player game
def continue_game():
    global player 
    #global players
    for row in range(3):
      for column in range(3):
        buttons[row][column].config(text = "", bg = "#F0F0F0")     
    if easy_flag is True:
       players = player_initialize("Jolene", "Computer")
       player = random.choice(players).get()
       if player == players[1].get():
          ai_turn()
    elif hard_flag is True:
       players = player_initialize("Jolene", "Computer")
       player = random.choice(players).get()
       if player == players[1].get():
          hard_ai()
    label.config(text = player + "'s turn")
    continue_button.forget()

def new_game():
      global win_count_zero
      global win_count_one
      continue_game()
      win_count_zero = 0
      win_count_one = 0
      win_count_label.config(text = players[0].get() + " wins: " + str(win_count_zero) + "\n" + players[1].get() + " wins: " + str(win_count_one))

def check_win():
    # Check rows
    for row in range(3):
      if  (buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != ""):
        buttons[row][0].config(bg = "green")
        buttons[row][1].config(bg = "green")
        buttons[row][2].config(bg = "green")
        return True
    # Check columns
    for column in range(3):
      if (buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != ""):
        buttons[0][column].config(bg = "green")
        buttons[1][column].config(bg = "green")
        buttons[2][column].config(bg = "green")
        return True
    # Check diagonals
    if (buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != ""):
      buttons[0][0].config(bg = "green")
      buttons[1][1].config(bg = "green")
      buttons[2][2].config(bg = "green")
      return True
    elif (buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != ""):
      buttons[0][2].config(bg = "green")
      buttons[1][1].config(bg = "green")
      buttons[2][0].config(bg = "green")
      return True
    elif empty_spaces() == 0:
      for row in range(3):
        for column in range(3):
          buttons[row][column].config(bg = "yellow")
      return "Tie"
    else:
      return False

def empty_spaces():
    spaces = 9
    for row in range(3):
      for column in range(3):
        if buttons[row][column]['text'] != "":
          spaces -= 1
    return spaces
      
def next_turn_helper(num, row, column):
      global player
      global win_count_one
      global win_count_zero
      if player == players[num].get():
        buttons[row][column].config(text = player) 
        if check_win() is False:
          if num == 1:
            player = players[num - 1].get()
            label.config(text = players[num - 1].get() + "'s turn")
          else:
            player = players[num + 1].get()
            label.config(text = players[num + 1].get() + "'s turn")
            if easy_flag is True:
              ai_turn()
            elif hard_flag is True:
               hard_ai()
        elif check_win() is True:      
          if num == 1:
            win_count_one += 1
          else:
            win_count_zero += 1
          label.config(text = players[num].get() + " wins!")
          win_count_label.config(text = players[0].get() + " wins: " + str(win_count_zero) + "\n" + players[1].get() + " wins: " + str(win_count_one))
          continue_button.pack(side = "top")
          playsound("Kids_Cheering.mp3")
        elif check_win() == "Tie":
          label.config(text = "Tie!")
          continue_button.pack(side = "top")

def switch_to_game_screen():
    global menu_frame
    menu_frame.forget()
    frame.pack()
    button_frame.pack()

def next_turn(row, column):
      global player
      global players  
      if buttons[row][column]['text'] == "" and check_win() is False:
        if player == players[0].get():
            next_turn_helper(0, row, column)
        else:
            next_turn_helper(1, row, column)

# Methods for One Player game (easy AI)
def switch_helper():
  global difficulty_frame
  difficulty_frame.forget()
  frame.pack()
  button_frame.pack()
  players = player_initialize("Jolene", "Computer")
  # update text values
  global player
  player = random.choice(players).get()
  label.config(text = player + "'s turn")
  win_count_label.config(text = players[0].get() + " wins: " + str(win_count_zero) + "\n" + players[1].get() + " wins: " + str(win_count_one))

def switch_ai_screen():
  switch_helper()
  global easy_flag
  # update difficulty
  easy_flag = True
  if player == players[1].get():
    ai_turn()

def switch_to_diff_screen():
   global menu_frame
   menu_frame.forget()
   difficulty_frame.pack()

def ai_turn():
   success = False
   while not success:
    row = random.randrange(0, 3, 1)
    column = random.randrange(0, 3, 1)
    if buttons[row][column]['text'] == "":
      success = True
      next_turn(row, column)

def player_initialize(zero, one):
  global players
  player_0 = tk.StringVar(window, zero)
  player_1 = tk.StringVar(window, one)
  players = [player_0, player_1]
  return players

# Hard AI methods
def switch_hard_screen():
  switch_helper()
  global hard_flag
  # update difficulty
  hard_flag = True
  if player == players[1].get():
    hard_ai()

def hard_ai():  
   if empty_spaces() >= 7:
      ai_turn()
   else:
      mySet = check_two_in_row()
      # if two in row exists
      if mySet:
          (x, y) = mySet.pop()
          next_turn(x, y)
      else:
         ai_turn()

# check for two in a row so that hard ai can block
def check_two_in_row():
   two_in_row = False
   # record the number of two in a rows
   num = 0
   temp = 0
   # default values indicating no spot is open
   tempRow = 9
   tempColumn = 9
   # use a set to keep track of eligible moves
   mySet = set()
   # check each row
   for row in range(3):
     temp = 0
     two_in_row = False
     tempRow = 9
     tempColumn = 9
     for column in range(3):
       if two_in_row is False:
         if buttons[row][column]['text'] == players[0].get():
            temp += 1
         elif buttons[row][column]['text'] == players[1].get():
           continue
         else:
            # save row and column values as a possible move
            tempRow = row
            tempColumn = column
       if temp == 2 and tempRow != 9 and tempColumn != 9:
          num += 1
          mySet.add((tempRow, tempColumn))
          two_in_row = True
       else:
          two_in_row = False
   # check each column
   for column in range(3):
       temp = 0
       two_in_row = False
       tempRow = 9
       tempColumn = 9
       for row in range(3):
         if two_in_row is False:
            if buttons[row][column]['text'] == players[0].get():
              temp += 1
            elif buttons[row][column]['text'] == players[1].get():
               continue
            else:
              # save row and column values as a possible move
               tempRow = row
               tempColumn = column
         if temp == 2 and tempRow != 9 and tempColumn != 9:
              num += 1
              mySet.add((tempRow, tempColumn))
              two_in_row = True
         else:
              two_in_row = False
   # check diagonals
   x = 0
   y = 0
   temp = 0
   two_in_row = False
   tempRow = 9
   tempColumn = 9
   while x < 3 and y < 3:
       if two_in_row is False:
         if buttons[x][y]['text'] == players[0].get():
            temp += 1
         elif buttons[x][y]['text'] == players[1].get():
            x += 1
            y += 1
            continue
         else:
            # save row and column values as a possible move
            tempRow = x
            tempColumn = y
       if temp == 2 and tempRow != 9 and tempColumn != 9:
            num += 1
            mySet.add((tempRow, tempColumn))
            two_in_row = True
       else:
            two_in_row = False
       x += 1
       y += 1
   x = 2
   y = 0
   temp = 0
   two_in_row = False
   tempRow = 9
   tempColumn = 9
   while x >= 0 and y < 3:
       if two_in_row is False:
         if buttons[x][y]['text'] == players[0].get():
            temp += 1
         elif buttons[x][y]['text'] == players[1].get():
            x -= 1
            y += 1
            continue
         else:
            # save row and column values as a possible move
            tempRow = x
            tempColumn = y
       if temp == 2 and tempRow != 9 and tempColumn != 9:
            num += 1
            mySet.add((tempRow, tempColumn))
            two_in_row = True
       else:
            two_in_row = False
       x -= 1
       y += 1
   return mySet

# container to hold attributes for ai
class board():
   # board attributes
   two_in_row = False
   num_of_twos = 0
   mySet = set()

   def __init__(self, two_in_row, num_of_twos, mySet):
      self.two_in_row = two_in_row
      self.num_of_twos = num_of_twos
      self.mySet = mySet

window = tk.Tk()
window.title("Tic Tac Toe")
window.geometry("300x300")

# game frame
frame = tk.Frame(window)
# menu frame
menu_frame = tk.Frame(window)
# 3 by 3 grid
button_frame = tk.Frame(window)
# additional frame for choosing computer's difficulty
difficulty_frame = tk.Frame(window)
playing = True
valid = True
players = player_initialize("Jolene", "Jared")
player = random.choice(players).get()
win_count_zero = 0
win_count_one = 0
easy_flag = False
hard_flag = False

buttons = [[0, 0, 0], 
          [0, 0, 0], 
          [0, 0, 0]]

label = tk.Label(frame, text = player + "'s turn", font = ('consolas', 40))
label.pack(side = "top")

win_count_label = tk.Label(frame, text = players[0].get() + " wins: " + str(win_count_zero) + "\n" + players[1].get() + " wins: " + str(win_count_one), font = ('consolas', 20))
win_count_label.pack(side = "bottom")

menu_title_label = tk.Label(menu_frame, text = "Tic-Tac-Toe!", font = ('consolas', 40))
menu_title_label.pack(side = "top")

diff_label = tk.Label(difficulty_frame, text = "Choose Difficulty Level", font = ('consolas', 40))
diff_label.pack(side = "top")

menu_frame.pack()

reset_button = tk.Button(frame, text = "Restart", font = ('consolas', 20), command = new_game)
reset_button.pack(side = "top")

continue_button = tk.Button(frame, text = "Continue", font = ('consolas', 20), command = continue_game)

one_player_button = tk.Button(menu_frame, text = "One Player", font = ('consolas', 20), command = switch_to_diff_screen)
one_player_button.pack(side = "top")

two_player_button = tk.Button(menu_frame, text = "Two Player", font = ('consolas', 20), command = switch_to_game_screen)
two_player_button.pack(side = "top")

easy_button = tk.Button(difficulty_frame, text = "Easy", font = ('consolas', 30), command = switch_ai_screen)
easy_button.pack(side = "top")

hard_button = tk.Button(difficulty_frame, text = "Hard", font = ('consolas', 30), command = switch_hard_screen)
hard_button.pack(side = "top")

for row in range(3):
  for column in range(3):
    buttons[row][column] = tk.Button(button_frame, text = "", font = ('consolas', 20), width = 10, height = 4, command = lambda row =     row, column = column: next_turn(row, column))
    buttons[row][column].grid(row = row, column = column)

tk.mainloop()
