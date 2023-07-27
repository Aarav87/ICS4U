# Shopping Cart | Final Project
# Name: Aarav Chhabra
# Date: July 25, 2023

import subprocess
import random
import customtkinter as ctk


# Classes

# Class for a shopping item
class Item:
    def __init__(self, name, price):
        # Initialize the name and price of the item
        self.name = name
        self.price = price


# Class for the shopping cart
class Cart:
    def __init__(self):
        # List of shopping cart items
        self.cart = []

        # Number of items in the cart
        self.numOfItems = 0

        # Total price
        self.totalPrice = 0


# Class for a generic page
class BasePage(ctk.CTkScrollableFrame):
    def __init__(self, master, pageName, cart):
        super().__init__(master, corner_radius=20, fg_color="transparent")

        # Configure page grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        # Reference to the shopping cart object
        self.shoppingCart = cart

        # Page label
        self.label = ctk.CTkLabel(self, text=pageName, compound="left", anchor="w", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, pady=(0, 10))


# Class for the shopping cart page
class CartPage(BasePage):
    def __init__(self, master, cart):
        super().__init__(master, "Cart 🛒", cart)

        # Message for when there are no items in cart
        self.noItemsMsg = ctk.CTkLabel(self, text="There is nothing in the cart.", compound="left", padx=5, anchor="w")

        # Keep track of all labels and buttons
        self.labels = []
        self.buttons = []

    # Displays cart items on the screen
    def displayItems(self):
        # Clear the labels and buttons list
        self.labels.clear()
        self.buttons.clear()

        # Iterate through each item
        for i, item in enumerate(self.shoppingCart.cart):
            # Show a label (with item name and price) and a remove from cart button on the screen
            label = ctk.CTkLabel(self, text=f"{item.name} - ${item.price}", compound="left", padx=5, anchor="w")
            button = ctk.CTkButton(self, text="Remove From Cart", width=100, height=24, command=lambda index=i: self.removeFromCart(index))
            label.grid(row=i + 1, column=0, pady=(0, 10), sticky="w")
            button.grid(row=i + 1, column=4, pady=(0, 10), padx=5)

            # Append the label and button to lists
            self.labels.append(label)
            self.buttons.append(button)

    # Deletes cart items from the screen (labels and buttons) if they exist
    def deleteItems(self):
        if self.labels:
            for i in range(len(self.labels)):
                self.labels[i].destroy()
                self.buttons[i].destroy()

    # Removes an item from the cart using the index of the button clicked
    def removeFromCart(self, index):
        # Update the cart's total price
        self.shoppingCart.totalPrice -= self.shoppingCart.cart[index].price

        # Delete the item from the cart
        del self.shoppingCart.cart[index]
        self.shoppingCart.numOfItems -= 1

        # Delete all the cart items from the screen
        self.deleteItems()

        # Rerender the cart items on the screen
        self.displayItems()

        # Display a message if the cart is empty
        self.emptyCartMessage()

    # Displays a message when the cart is empty
    def emptyCartMessage(self):
        if self.shoppingCart.numOfItems == 0:
            self.noItemsMsg.grid(row=0, column=0, pady=(0, 10), sticky="w")
        else:
            self.noItemsMsg.grid_remove()


# Class for the shop page (from which users can add items to their cart)
class ShopPage(BasePage):
    def __init__(self, master, cart):
        super().__init__(master, "Shop 🥕", cart)

        # Label for number of items in cart
        self.cartItems = ctk.CTkLabel(self, text=f"Items in Cart: {self.shoppingCart.numOfItems}", compound="left", anchor="w", font=ctk.CTkFont(size=15, weight="bold"))
        self.cartItems.grid(row=0, column=4, pady=(0, 10))

        # List of all items that can be added to cart
        self.allItems = []
        self.generateItems()

        # Display all the items on the screen
        self.displayItems()

    # Generates a list of all items that can be added to cart
    def generateItems(self):
        # Read a text file with grocery items
        with open("food.txt") as file:
            # Loop through each item in the file
            for item in file:
                # Remove whitespace from the item
                name = item.rstrip().title()

                # Generate a random float for the price
                price = round(random.uniform(1.50, 11.99), 2)

                # Append an item object with the name and price to the list
                self.allItems.append(Item(name, price))

    # Displays shopping items on the screen
    def displayItems(self):
        # Iterate through each item
        for i, item in enumerate(self.allItems):
            # Show a label (with item name and price) and an add to cart button on the screen
            label = ctk.CTkLabel(self, text=f"{item.name} - ${item.price}", compound="left", padx=5, anchor="w")
            button = ctk.CTkButton(self, text="Add To Cart", width=100, height=24, command=lambda index=i: self.addToCart(index))
            label.grid(row=i + 1, column=0, pady=(0, 10), sticky="w")
            button.grid(row=i + 1, column=4, pady=(0, 10), padx=5)

    # Adds the item to the cart using the index of the button clicked
    def addToCart(self, index):
        # Update the cart's total price
        self.shoppingCart.totalPrice += self.allItems[index].price

        # Add the item to the cart
        self.shoppingCart.cart.append(self.allItems[index])
        self.shoppingCart.numOfItems += 1

        # Update the number of items label
        self.cartItems.configure(text=f"Items in Cart: {self.shoppingCart.numOfItems}")


# Class for the checkout page
class CheckoutPage(BasePage):
    def __init__(self, master, cart):
        super().__init__(master, "Checkout 💰", cart)

        # Initialize all the error messages
        self.emptyCartMsg = ctk.CTkLabel(self, text="There is nothing in the cart. Cannot checkout.", compound="left", padx=5, anchor="w")
        self.lessMoneyMsg = ctk.CTkLabel(self, text="Please give more money than the total price.", compound="left", padx=5, anchor="w")
        self.enterNumbersMsg = ctk.CTkLabel(self, text="Please enter numbers for money amount.", compound="left", padx=5, anchor="w")
        self.unnecessaryChange = ctk.CTkLabel(self, text="Please do not provide unnecessary change (max change $100).", compound="left", padx=5, anchor="w")

        # Initialize label for total price
        self.finalPrice = ctk.CTkLabel(self, text=f"Final Price - ${round(self.shoppingCart.totalPrice, 2)}", compound="left", padx=5, anchor="w")

        # Initialize payment options buttons/entries
        self.payCashLabel = ctk.CTkLabel(self, text="Enter Cash Amount:", compound="left", padx=5, anchor="w")
        self.payCashInput = ctk.CTkEntry(self, width=100, height=10)
        self.payCashButton = ctk.CTkButton(self, text="Pay Cash", width=100, height=24, command=lambda: self.handleCashPayment())
        self.optionLabel = ctk.CTkLabel(self, text="OR", compound="left", padx=5, anchor="w")
        self.payCreditButton = ctk.CTkButton(self, text="Pay Credit", width=100, height=24, command=lambda: self.handleCreditPayment())

        # List of coin denominations
        self.denominations = [2, 1, 0.25, 0.10, 0.05]

    # Handles credit payment
    def handleCreditPayment(self):
        # Hide the error messages for invalid payment
        self.lessMoneyMsg.grid_remove()
        self.unnecessaryChange.grid_remove()
        self.enterNumbersMsg.grid_remove()

        # Create the receipt
        self.createReceipt(self.shoppingCart.totalPrice, 0)

    # Handle cash payment
    def handleCashPayment(self):
        # Hide the error messages for invalid payment
        self.lessMoneyMsg.grid_remove()
        self.unnecessaryChange.grid_remove()
        self.enterNumbersMsg.grid_remove()

        # Get the value from the entry box
        amountPaid = self.payCashInput.get()

        # Validate that amount paid is a float
        try:
            amountPaid = round(float(amountPaid), 2)

            # Check if user paid more than the total price
            if amountPaid >= self.shoppingCart.totalPrice:
                # Check if user paid within $100 of the cart price (unnecessary change otherwise)
                if amountPaid <= (self.shoppingCart.totalPrice + 100):
                    # Calculate the change due
                    changeDue = round(amountPaid - self.shoppingCart.totalPrice, 2)

                    # Get the number of coins needed of each denomination for the change
                    coins = self.calculateChange(changeDue)

                    # Display a receipt on screen
                    self.createReceipt(amountPaid, changeDue, coins=coins)
                else:
                    # Show unnecessary change message
                    self.unnecessaryChange.grid(row=5, column=0, pady=(0, 10), padx=(0, 5), sticky="w")
            else:
                # Show error message for less money entered
                self.lessMoneyMsg.grid(row=5, column=0, pady=(0, 10), padx=(0, 5), sticky="w")

        # Show error message for letters entered
        except ValueError:
            self.enterNumbersMsg.grid(row=5, column=0, pady=(0, 10), padx=(0, 5), sticky="w")

    # Calculates the number of coins needed of each denomination
    def calculateChange(self, change):
        # Initialize a list that holds the count of each coin
        coins = [0, 0, 0, 0, 0]

        # Initialize a counter variable that keeps track of the current coin
        i = 0

        # Loop if there is more than 5 cents of change
        while change >= 0.05:
            # Check if the change is greater than the value of the current coin
            if change >= self.denominations[i]:
                # Reduce change by that coin and increase the coin count
                change = round(change - self.denominations[i], 2)
                coins[i] += 1
            else:
                # Change the current coin
                i += 1

        # Round to the nearest nickel if there is more than 3 cents of change remaining
        if change >= 0.03:
            coins[4] += 1

        return coins

    # Creates a receipt in a text file
    def createReceipt(self, amountPaid, change, coins=[]):
        # Hide payment options
        self.hidePayment()

        # Create receipt as a text file
        with open("receipt.txt", "w") as file:
            file.write("------RECEIPT------\n")
            file.write(f"Total: ${round(self.shoppingCart.totalPrice, 2)}\n")
            file.write(f"Amount Paid: ${round(amountPaid, 2)}\n")
            file.write(f"Change: ${change}\n")

            # Loop through each coin denomination
            for coin in range(len(coins)):
                # Add the number of coins to the text file if it's used in the change
                if coins[coin] > 0:
                    file.write(f"${round(self.denominations[coin], 2)} Coins: {coins[coin]}\n")

        # Clear shopping cart
        self.shoppingCart.cart.clear()
        self.shoppingCart.numOfItems = 0
        self.shoppingCart.totalPrice = 0

        # Show empty cart message
        self.showEmptyCartMsg()

        # Open the receipt
        subprocess.Popen("receipt.txt", shell=True)

    # Displays a message when the user goes on the checkout page with an empty cart
    def showEmptyCartMsg(self):
        # Check if cart is empty
        if self.shoppingCart.numOfItems == 0:
            # Display the message and hide payment options
            self.emptyCartMsg.grid(row=0, column=0, pady=(0, 10), sticky="w")
            self.hidePayment()
        else:
            # Hide the message and show payment options
            self.emptyCartMsg.grid_remove()
            self.showPayment()

    # Displays payment options
    def showPayment(self):
        self.finalPrice.grid(row=1, column=0, pady=(0, 10), sticky="w")
        self.payCashLabel.grid(row=2, column=0, pady=(0, 10), sticky="w")
        self.payCashInput.grid(row=3, column=0, pady=(0, 10), sticky="w")
        self.payCashButton.grid(row=4, column=0, pady=(0, 10), padx=(0, 5), sticky="w")
        self.optionLabel.grid(row=3, column=1, pady=(0, 10), sticky="w")
        self.payCreditButton.grid(row=3, column=2, pady=(0, 10), padx=(10, 0), sticky="w")

    # Hides payment options
    def hidePayment(self):
        self.finalPrice.grid_remove()
        self.payCashLabel.grid_remove()
        self.payCashInput.grid_remove()
        self.payCashButton.grid_remove()
        self.optionLabel.grid_remove()
        self.payCreditButton.grid_remove()


# Class for the app
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Shopping Cart")
        self.geometry(f"{700}x{450}")
        self.resizable(False, False)

        # Configure page grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create navigation bar
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="Walmart", compound="left", font=ctk.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        self.shop_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Shop 🥕", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=lambda: self.showShopPage())
        self.shop_button.grid(row=1, column=0, sticky="ew")
        self.cart_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Cart 🛒", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=lambda: self.showCartPage())
        self.cart_button.grid(row=2, column=0, sticky="ew")
        self.checkout_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Checkout 💰", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=lambda: self.showCheckoutPage())
        self.checkout_button.grid(row=3, column=0, sticky="ew")

        # Initialize shopping cart
        self.shoppingCart = Cart()

        # Initialize the shop, cart, and checkout page
        self.shopPage = ShopPage(self, self.shoppingCart)
        self.cartPage = CartPage(self, self.shoppingCart)
        self.checkoutPage = CheckoutPage(self, self.shoppingCart)

        # Show the shop page
        self.showShopPage()

    # Shows the shop page
    def showShopPage(self):
        self.shopPage.grid(row=0, column=1, sticky="nsew")
        self.cartPage.grid_remove()
        self.checkoutPage.grid_remove()

        # Update the label for the number of items in cart
        self.shopPage.cartItems.configure(text=f"Items in Cart: {self.shoppingCart.numOfItems}")

    # Shows the cart page
    def showCartPage(self):
        self.cartPage.grid(row=0, column=1, sticky="nsew")
        self.shopPage.grid_remove()
        self.checkoutPage.grid_remove()

        # Display a message if the cart is empty
        self.cartPage.emptyCartMessage()

        # Deletes the items in the cart off the screen and re-renders them
        self.cartPage.deleteItems()
        self.cartPage.displayItems()

    # Shows the checkout page
    def showCheckoutPage(self):
        self.checkoutPage.grid(row=0, column=1, sticky="nsew")
        self.cartPage.grid_remove()
        self.shopPage.grid_remove()

        # Update label for the cart's total price
        self.checkoutPage.finalPrice.configure(text=f"Final Price - ${round(self.shoppingCart.totalPrice, 2)}")

        # Display a message when the user goes on the checkout page with an empty cart
        self.checkoutPage.showEmptyCartMsg()


# Main
ctk.set_appearance_mode("Dark")
app = App()
app.mainloop()
