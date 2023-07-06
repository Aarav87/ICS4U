## Body Mass Index Calculator Assignment

# Output introduction about the program
print("Welcome to the BMI Calculator!\n")

# Get weight from user
while True:
    try:
        # Ask user to enter weight
        weight = float(input("Enter your weight (kg): "))

        # Validate if weight is positive
        if weight <= 0:
            print("Weight must be positive!")
        else:
            break

    except ValueError:
        print("Make sure you enter a positive number!")

# Get height from user
while True:
    try:
        # Ask user to enter height
        height = float(input("Enter your height (m): "))

        # Height if height is positive
        if height <= 0:
            print("Height must be positive!")
        else:
            break

    except ValueError:
        print("Make sure you enter a positive number!")

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
