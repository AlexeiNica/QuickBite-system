from datetime import datetime

# Function to display a table with data and headers
def display_table(data, headers):
    print("\n" + "-" * 40)
    # Print headers with proper alignment
    print(f"{headers[0].ljust(10)} | {headers[1].center(20)} | {headers[2].rjust(7)}")
    print("-" * 40)
    # Iterate through each item in data and display formatted output
    for item in data:
        print(f"{item[0].ljust(10)} | {item[1].center(20)} | £{item[2]:.2f}".rjust(7))
    print("-" * 40)


# Function to display the menu items
def display_menu(menu):
    # Create a list of tuples for menu data (item number, name, price)
    menu_data = [(str(index + 1), item['name'], item['price']) for index, item in enumerate(menu)]
    # Display the table with menu items
    display_table(menu_data, headers=["No.", "Item", "Price"])


# Function to get input from the user with optional validation
def get_input(prompt, valid_options=None):
    while True:
        response = input(prompt)
        # Return input if valid or if no validation list is provided
        if not valid_options or response in valid_options:
            return response
        # Display an error message if input is invalid
        print("INVALID CHOICE. PLEASE TRY AGAIN.")


# Function to get an integer input with error handling
def get_integer_input(prompt):
    while True:
        try:
            # Attempt to convert input to integer
            return int(input(prompt))
        except ValueError:
            # Error message for invalid input
            print("INVALID INPUT. PLEASE ENTER A VALID INTEGER.")


# Function to place an order based on the menu
def place_order(menu):
    order = {}  # Initialize an empty dictionary to store the order
    display_menu(menu)  # Show the menu to the user

    while True:
        # Prompt user to choose an item or exit
        choice = get_input("Enter the number of the item to order, or 'e' to exit: ",
                           [str(i) for i in range(1, len(menu) + 1)] + ['e'])
        if choice == 'e':  # Exit the order loop
            break

        index = int(choice) - 1  # Get the index of the chosen item
        # Get quantity for the chosen item
        quantity = get_integer_input(f"Enter quantity for {menu[index]['name']}: ")
        if quantity < 1:  # Validate quantity input
            print("INVALID INPUT. QUANTITY MUST BE AT LEAST 1.")
            continue

        item_name = menu[index]['name']
        # Add or update the item quantity in the order
        if item_name in order:
            order[item_name] += quantity
        else:
            order[item_name] = quantity
        print(f"✔️  Added {quantity} x {item_name} to your order.")

    return order  # Return the final order


# Function to display the receipt of the order
def display_receipt(order, menu):
    if not order:  # Check if the order is empty
        print("NO ITEMS ORDERED.")
        return

    print("=" * 60)
    print("QUICKBITE ORDER RECEIPT".center(60))
    # Display the current date and time
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    total = 0  # Initialize total cost
    for item_name, quantity in order.items():
        # Get the price of the item from the menu
        price = next(item['price'] for item in menu if item['name'] == item_name)
        item_total = price * quantity
        # Display item details
        print(f"{item_name}: {quantity} x £{price:.2f} = £{item_total:.2f}")
        total += item_total

    # Display the total cost
    print("=" * 60)
    print(f"Total Due: £{total:.2f}")
    print("=" * 60)


# Function to review and modify the order
def review_and_modify_order(order, menu):
    while True:
        if not order:  # Check if the order is empty
            print("YOUR ORDER IS EMPTY.")
            return order

        # Ask user if they want to modify the order or add new items
        choice = get_input("Would you like to modify or add items? (modify/add/exit): ", ['modify', 'add', 'exit'])
        if choice == 'exit':  # Exit the modification process
            break

        elif choice == 'modify':
            item_name = get_input("Enter the name of the item to modify: ")
            if item_name not in order:  # Validate item existence
                print("INVALID ITEM NAME. PLEASE TRY AGAIN.")
                continue

            # Get new quantity for the item
            new_quantity = get_integer_input(f"Enter new quantity for {item_name} (0 to remove): ")
            if new_quantity == 0:
                # Remove item if quantity is zero
                del order[item_name]
                print(f"✔️  {item_name} removed from your order.")
            else:
                order[item_name] = new_quantity
                print(f"✔️  Updated {item_name} to quantity {new_quantity}.")

        elif choice == 'add':
            display_menu(menu)  # Display the menu again
            item_choice = get_input("Enter the number of the item to add: ", [str(i) for i in range(1, len(menu) + 1)])
            index = int(item_choice) - 1
            item_name = menu[index]['name']
            quantity = get_integer_input(f"Enter quantity for {item_name}: ")

            if item_name in order:
                order[item_name] += quantity
                print(f"✔️  Added {quantity} more of {item_name}. New total: {order[item_name]}")
            else:
                order[item_name] = quantity
                print(f"✔️  Added {quantity} x {item_name} to your order.")

    return order  # Return the modified order


# Main menu function to control the program flow
def main_menu(menu):
    while True:
        print("\nWELCOME TO QUICKBITE ORDERING SYSTEM!")
        print("1. View Menu")
        print("2. Place Your Order")
        print("3. Exit")
        # Get user choice for main menu
        choice = get_input("Please choose an option: ", ['1', '2', '3'])
        if choice == '1':
            display_menu(menu)
        elif choice == '2':
            order = place_order(menu)
            final_order = review_and_modify_order(order, menu)
            display_receipt(final_order, menu)
        elif choice == '3':
            if get_input("Are you sure you want to exit? (yes/no): ", ['yes', 'no']) == 'yes':
                print("THANK YOU FOR VISITING US!")
                break


# Define the menu with items
menu = [
    {'name': 'Pizza', 'price': 10.00},
    {'name': 'Fish', 'price': 5.35},
    {'name': 'Salad', 'price': 3.40},
    {'name': 'Chips', 'price': 1.45},
    {'name': 'Drink', 'price': 1.99}
]

# Entry point of the program
if __name__ == "__main__":
    try:
        main_menu(menu)
    except Exception as e:
        # Catch any unexpected errors and display an error message
        print(f"Oops! Something went wrong: {e}")
