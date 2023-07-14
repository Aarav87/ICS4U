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

# Get validated input from the user
data = get_input()

# Generate random indices for the swap
index0, index1, index2 = random.sample(range(3), 3)

# Swap the user's input
new_data = [data[index0], data[index1], data[index2]]

# Output data before and after swap
print("Before swap:", data[0], data[1], data[2])
print("After swap:", new_data[0], new_data[1], new_data[2])
