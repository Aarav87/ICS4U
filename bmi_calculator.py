### Body Mass Index Calculator Assignment

## Subprograms

# Gets valid input from the user
def validate_input(measurement):
    while True:
        try:
            # Ask user to enter value
            user_value = float(input(f"Enter your {measurement.lower()}: "))

            # Validate if value is positive
            if user_value <= 0:
                print(f"{measurement} must be positive!")
            else:
                return user_value

        except ValueError:
            print("Make sure you enter a positive number!")


## Main Program

# Output introduction about the program
print("Welcome to the BMI Calculator!\n")

# Get height and weight from user
weight = validate_input("Weight (kg)")
height = validate_input("Height (m)")

# Calculate BMI
bmi = weight / (height ** 2)

# Determine the category where the BMI falls into
if bmi < 18.5:
    category = "underweight"
elif 18.5 <= bmi <= 24.9:
    category = "normal weight"
elif 25 <= bmi <= 29.9:
    category = "overweight"
elif 30 <= bmi <= 34.9:
    category = "obesity (class 1)"
elif 35 <= bmi <= 39.9:
    category = "obesity (class 2)"
else:
    category = "extreme obesity (class 3)"

# Output the category and rounded BMI
print(f"\nYour body mass index is around {round(bmi, 2)} and you fall into the {category} class.")
