# Swap Algorithm Assignment
# Name: Aarav Chhabra
# Date: July 20, 2023

import random


# Subprograms

# Gets validated input from the user
def get_input():
    while True:
        # Get input
        user_input = input("\nEnter 3 numbers/words/letters separated with a space: ").split()

        # Ensure that user only entered 3 numbers/letters/words
        if len(user_input) != 3:
            print("Make sure you only enter 3 numbers/letters/words separated by a space.")
        else:
            return user_input


# Main

# Output introduction message
print("Welcome to the Swap Algorithm Simulator!")

# Keeps track of if the simulator is running
running = "Y"

# Loop as long as the user wants the simulator to run
while running == "Y":
    # Get validated input from the user
    data = get_input()

    # Swap the user's input
    new_data = [data[1], data[2], data[0]]

    # Output data before and after swap
    print("Before swap:", data[0], data[1], data[2])
    print("After swap:", new_data[0], new_data[1], new_data[2])

    # Ask user if they want to continue the simulator
    running = input("\nDo you want to continue the simulator (Y/N): ").upper()
