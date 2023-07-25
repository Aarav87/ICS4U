# Shopping Cart | Final Project
# Name: Aarav Chhabra
# Date: July 25, 2023

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
        self.label = ctk.CTkLabel(self, text=pageName, compound="left", anchor="w",
                                  font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, pady=(0, 10))


# Class for the shopping cart page
class CartPage(BasePage):
    def __init__(self, master, cart):
        super().__init__(master, "Cart 🛒", cart)

        # Message for when there is no items in cart
        self.noItemsMsg = ctk.CTkLabel(self, text="There is nothing in the cart.", compound="left", padx=5, anchor="w")

        # Keep track of all labels and buttons
        self.labels = []
        self.buttons = []

    # Display cart items on the screen
    def displayItems(self):
        # Clear the labels and buttons list
        self.labels.clear()
        self.buttons.clear()

        # Iterate through each item
        for i, item in enumerate(self.shoppingCart.cart):
            # Show a label and button on the screen
            label = ctk.CTkLabel(self, text=f"{item.name} - ${item.price}", compound="left", padx=5, anchor="w")
            button = ctk.CTkButton(self, text="Remove From Cart", width=100, height=24, command=lambda index=i: self.removeFromCart(index))
            label.grid(row=i + 1, column=0, pady=(0, 10), sticky="w")
            button.grid(row=i + 1, column=4, pady=(0, 10), padx=5)

            # Append the label and button to lists
            self.labels.append(label)
            self.buttons.append(button)

    # Removes an item from the cart using the index of the button clicked
    def removeFromCart(self, index):
        # Update the cart total price
        self.shoppingCart.totalPrice -= self.shoppingCart.cart[index].price

        # Delete the item from the cart
        del self.shoppingCart.cart[index]
        self.shoppingCart.numOfItems -= 1

        # Delete all the cart items from the screen
        for i in range(self.shoppingCart.numOfItems + 1):
            self.labels[i].destroy()
            self.buttons[i].destroy()

        # Rerender the cart items on the screen
        self.displayItems()

        # Display a message if there is nothing in the cart
        if self.shoppingCart.numOfItems == 0:
            self.addItemsMessage()

    # Displays a message when there is nothing in the cart
    def addItemsMessage(self):
        self.noItemsMsg.grid(row=0, column=0, pady=(0, 10), sticky="w")


# Class for the shop page (from which users can add items to their cart)
class ShopPage(BasePage):
    def __init__(self, master, cart):
        super().__init__(master, "Shop 🥕", cart)

        # Number of items in cart label
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

    # Display items on the screen
    def displayItems(self):
        # Iterate through each item
        for i, item in enumerate(self.allItems):
            # Show a label and button on the screen
            label = ctk.CTkLabel(self, text=f"{item.name} - ${item.price}", compound="left", padx=5, anchor="w")
            button = ctk.CTkButton(self, text="Add To Cart", width=100, height=24, command=lambda index=i: self.addToCart(index))
            label.grid(row=i + 1, column=0, pady=(0, 10), sticky="w")
            button.grid(row=i + 1, column=4, pady=(0, 10), padx=5)

    # Adds the item to the cart using the index of the button clicked
    def addToCart(self, index):
        # Update the cart total price
        self.shoppingCart.totalPrice += self.allItems[index].price

        # Add item to the cart
        self.shoppingCart.cart.append(self.allItems[index])
        self.shoppingCart.numOfItems += 1

        # Update the number of items label
        self.cartItems.configure(text=f"Items in Cart: {self.shoppingCart.numOfItems}")


# Class for the checkout page
class Checkout(BasePage):
    def __init__(self, master, cart):
        super().__init__(master, "Checkout 💰", cart)

        # Message for when user can't checkout
        self.invalidCheckout = ctk.CTkLabel(self, text="There is nothing in the cart. Cannot checkout.", compound="left", padx=5, anchor="w")

        # Initialize label for total price
        self.finalPrice = ctk.CTkLabel(self, text=f"Final Price - ${round(self.shoppingCart.totalPrice, 2)}", compound="left", padx=5, anchor="w")

        # Initialize payment options buttons/entries
        self.payCashLabel = ctk.CTkLabel(self, text="Enter Cash Amount:", compound="left", padx=5, anchor="w")
        self.payCashInput = ctk.CTkEntry(self, width=100, height=10)
        self.payCashButton = ctk.CTkButton(self, text="Pay Cash", width=100, height=24, command=lambda: self.handleCashPayment())
        self.optionLabel = ctk.CTkLabel(self, text="OR", compound="left", padx=5, anchor="w")
        self.payCreditButton = ctk.CTkButton(self, text="Pay Credit", width=100, height=24, command=lambda: self.handleCreditPayment())

        # Initialize invalid payment message
        self.invalidPaymentMsg = ctk.CTkLabel(self, text="Make sure you enter a number greater than the cost.", compound="left", padx=5, anchor="w")

        # Initialize receipt labels
        self.receiptLabel = ctk.CTkLabel(self, text="---Receipt---", compound="left", padx=5, anchor="w")
        self.totalLabel = ctk.CTkLabel(self, compound="left", padx=5, anchor="w")
        self.amountPaid = ctk.CTkLabel(self, compound="left", padx=5, anchor="w")
        self.change = ctk.CTkLabel(self, compound="left", padx=5, anchor="w")

    # Handles credit payment
    def handleCreditPayment(self):
        self.displayReceipt(self.shoppingCart.totalPrice, 0)

    # Handle cash payment
    def handleCashPayment(self):
        # Get the value from the entry box
        amountPaid = self.payCashInput.get()

        # Verify that amount paid is a float
        try:
            amountPaid = round(float(amountPaid), 2)

            # Check if amount paid is greater than the total price
            if amountPaid >= self.shoppingCart.totalPrice:
                # Change due
                changeDue = amountPaid - self.shoppingCart.totalPrice

                # Get the number of coins needed of each denomination for the change
                coins = self.calculateChange(changeDue)

                # Display receipt on screen
                self.displayReceipt(amountPaid, changeDue, coins=coins)
            else:
                # Show error message
                self.invalidPaymentMsg.grid(row=5, column=0, pady=(0, 10), padx=(0, 5), sticky="w")

        # Show error message
        except ValueError:
            self.invalidPaymentMsg.grid(row=5, column=0, pady=(0, 10), padx=(0, 5), sticky="w")

    # Calculates the number of coins needed of each denomination
    def calculateChange(self, change):
        coins = {"Toonies": 0, "Loonies": 0, "Quarters": 0, "Dimes": 0, "Nickels": 0}

        # Keep looping as long as there is change
        while change >= 0:
            # Check the coin that must be drawn from the largest to smallest value
            if change >= 2:
                coins["Toonies"] += 1
                change -= 2
            elif change >= 1:
                coins["Loonies"] += 1
                change -= 1
            elif change >= 0.25:
                coins["Quarters"] += 1
                change -= 0.25
            elif change >= 0.10:
                coins["Dimes"] += 1
                change -= 0.10
            elif change >= 0.05:
                coins["Nickels"] += 1
                change -= 0.05
            elif change >= 0.03:
                coins["Nickels"] += 1
                change -= 0.05
            else:
                change -= 0.05

        return coins

    # Displays receipt on the screen
    def displayReceipt(self, amountPaid, change, coins={}):
        # Hide payment options
        self.hidePayment()

        # Render receipt title label
        self.receiptLabel.grid(row=1, column=0, pady=(0, 10), padx=(0, 5), sticky="w")

        # Render total amount label
        self.totalLabel.configure(text=f"Total: ${round(self.shoppingCart.totalPrice, 2)}")
        self.totalLabel.grid(row=2, column=0, pady=(0, 10), padx=(0, 5), sticky="w")

        # Update and render amount paid and change due
        self.amountPaid.configure(text=f"Amount Paid: ${amountPaid}")
        self.amountPaid.grid(row=3, column=0, pady=(0, 10), sticky="w")
        self.change.configure(text=f"Change: ${round(change, 2)}")
        self.change.grid(row=4, column=0, pady=(0, 10), sticky="w")

        # Display the number of coins needed of each denomination for the change
        row = 5
        for coin in coins:
            if coins[coin] > 0:
                label = ctk.CTkLabel(self, text=f"{coin}: {coins[coin]}", compound="left", padx=5, anchor="w")
                label.grid(row=row, column=0, pady=(0, 10), sticky="w")
                row += 1

        # Clear shopping cart
        self.shoppingCart.cart.clear()
        self.shoppingCart.numOfItems = 0
        self.shoppingCart.totalPrice = 0

    # Displays message when cart is empty and hides payment options
    def invalidCheckoutMessage(self):
        self.invalidCheckout.grid(row=0, column=0, pady=(0, 10), sticky="w")
        self.hidePayment()

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
        self.checkoutPage = Checkout(self, self.shoppingCart)

        # Show the shop page
        self.showShopPage()

    # Show the shop page
    def showShopPage(self):
        self.shopPage.grid(row=0, column=1, sticky="nsew")
        self.cartPage.grid_remove()
        self.checkoutPage.grid_remove()

        # Update the number of items label
        self.shopPage.cartItems.configure(text=f"Items in Cart: {self.shoppingCart.numOfItems}")

    # Show the cart page
    def showCartPage(self):
        self.cartPage.grid(row=0, column=1, sticky="nsew")
        self.shopPage.grid_remove()
        self.checkoutPage.grid_remove()

        # Display a message if there is nothing in the cart
        if self.shoppingCart.numOfItems == 0:
            self.cartPage.addItemsMessage()
        else:
            self.cartPage.noItemsMsg.grid_remove()

        # Render the items in the cart
        self.cartPage.displayItems()

    # Show the checkout page
    def showCheckoutPage(self):
        self.checkoutPage.grid(row=0, column=1, sticky="nsew")
        self.cartPage.grid_remove()
        self.shopPage.grid_remove()

        # Update total price label
        self.checkoutPage.finalPrice.configure(text=f"Final Price - ${round(self.shoppingCart.totalPrice, 2)}")

        # Check if there is nothing in the cart
        if self.shoppingCart.numOfItems == 0:
            # Show an invalid checkout message
            self.checkoutPage.invalidCheckoutMessage()
        else:
            self.checkoutPage.invalidCheckout.grid_remove()

            # Show payment options
            self.checkoutPage.showPayment()


# Main
ctk.set_appearance_mode("Dark")
app = App()
app.mainloop()
