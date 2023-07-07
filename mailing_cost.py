# Mailing Program Assignment
# Name: Aarav Chhabra
# Date: July 11, 2023

# Subprograms

# Gets valid mass input from the user
def validate_mass():
    while True:
        try:
            # Ask user to enter mass of the letter
            mass = float(input(f"Enter the mass of the letter (g): "))

            # Validate if value is positive
            if mass <= 0:
                print(f"The letter must weight something! Make sure you enter a positive value.")
            else:
                return mass

        # Handle value error when letters are entered
        except ValueError:
            print("The mass must be a number! Make sure you enter a positive value.")


# Main

# Output introduction message
print("Welcome to mailing cost calculator!\n")

# Get mass from user
mass = validate_mass()

# Initialize cost of mailing a letter
cost = 0

# Add the corresponding cost depending on the mass
if mass < 30:
    cost += 40
elif 30 <= mass < 50:
    cost += 55
elif 50 <= mass <= 100:
    cost += 70
else:
    cost += 70 + (25 * ((mass - 100) // 50 + 1))

# Output the cost
print(f"\nThe cost to mail a letter weighing {mass} grams is {int(cost)} sinas.")
