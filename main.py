import turtle
import pandas
from tkinter import messagebox
import time

NO_OF_STATES = 28

# setting up turtle screen
screen = turtle.Screen()
screen.title("Indian States Game")
screen.setup(width=800, height=900)

# adding the blank indian map
image = "states_map.gif"
screen.addshape(image)
turtle.shape(image)

# reading data from csv file
data = pandas.read_csv("28_states.csv")

# storing all the state names as a list
all_states = data["state"]

# storing states guessed by user
guessed_states = []

# no of states guessed
score = 0

# turning off the tracer of turtle
turtle.tracer(0)


# function to display a state on the map
def display_state(guess, text_color):
    state_row = data[data.state == guess]
    x = int(state_row.x)
    y = int(state_row.y)
    writer = turtle.Turtle()
    writer.hideturtle()
    writer.penup()
    writer.color(text_color)
    writer.goto(x, y)
    writer.write(arg=f"{guess}", align="center", font=('Arial', 12, 'bold'))
    # updating the screen
    turtle.update()


# displaying information about game
message = f"Try guessing all of the 28 Indian states. " \
          f"\n\nNote:" \
          f"\n1. Union Territories are not included." \
          f"\n2. You can enter the states in any case (upper/lower)." \
          f"\n3. You can enter 'exit' to give up."
messagebox.showinfo(title="Indian States Game", message=message)

# start time
start_time = time.time()

game_is_on = True
while game_is_on:
    # taking user guess as input
    user_guess = screen.textinput(f"{score}/{NO_OF_STATES} Your guess", "Enter a state (enter 'exit' to give up):").title()
    # if user wants to exit
    if user_guess == "Exit":
        game_is_on = False
        break

    # state guessed is valid and has not been guessed before
    if user_guess in all_states.to_list() and user_guess not in guessed_states:
        score += 1
        guessed_states.append(user_guess)
        display_state(user_guess, "black")

    # all states have been guessed
    if score == NO_OF_STATES:
        game_is_on = False

end_time = time.time()

# displaying appropriate message based on score

# all states were guesses
if score == NO_OF_STATES:
    # computing time taken to guess all the states
    time_taken = round(end_time - start_time)
    message_to_display = f"You have guessed all the states." \
                         f"\nTime taken: {int(time_taken / 60)} minute(s) and {time_taken % 60} seconds"
    messagebox.showinfo(title="Game Over", message=message_to_display)

# all states were not guessed
else:
    message_to_display = f"You could not guess {NO_OF_STATES - score}/{NO_OF_STATES} states." \
                         f"\nThe missing states have been saved in a separate file."
    messagebox.showinfo(title="", message=message_to_display)

    # storing all the missing states in a list
    missing_states = [state for state in all_states if state not in guessed_states]

    # displaying all the missing states in red color on the map
    for state in missing_states:
        display_state(state, "red")

    # storing the missing states in a csv file for the user to access
    df = pandas.DataFrame(missing_states)
    df.to_csv("missing_states.csv")

turtle.mainloop()
