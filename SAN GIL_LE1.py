import os
import time

# Function to pause and clear terminal screen
def pause():
    time.sleep(1.5)
    os.system('cls' if os.name == 'nt' else 'clear')
 
# Dictionary to store game library with their quantities and rental costs
game_library = {
    "Donkey Kong": {"quantity": 3, "cost": 2.00},
    "Super Mario Bros": {"quantity": 5, "cost": 3.00},
    "Tetris": {"quantity": 2, "cost": 1.00},
    # Add more games as needed
}

# Dictionary to store user accounts with their balances and points
user_accounts = {}

# Admin account details
admin_username = "admin"
admin_password = "adminpass"

# Function to display available games with their numbers and rental costs
def display_available_games():
    print("GAME LIBRARY:\n")
    count = 1
    for game in game_library:
        print(f"{count}. {game}\n     Quantity: {game_library[game]["quantity"]}\n     Cost: ${game_library[game]["cost"]:.2f}")
        count += 1

# Function to register a new user
def register_user():
    try:
        username = input("Enter desired username: ")

        if username in user_accounts:
            print("\nUsername already exists. Please try again.")
        else:
            password = input("Enter desired password: ")
            user_accounts[username] = {"password": password, "balance": 0, "inventory":{}, "points": 0}
            print("\nAccount succesfully registered.")
            pause()
            main_menu()
            return user_accounts
    except ValueError as e:
        print(str(e))
        pause()
        main_menu()
        
# Function to log-in
def login_user():
    try:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username not in user_accounts:
            raise ValueError("Username not found. Please try again.")
        
        if password != user_accounts[username]["password"]:
            raise ValueError("Incorrect password. Please try again.")
        
        game_id_map = {}
        print("\nLogged in successfully.")
        pause()
        logged_in_menu(username, game_id_map)
    
    except ValueError as e:
        print(str(e))
        pause()
        main_menu()

# Function to rent a game
def rent_game(username, game_ID, quantity, inventory):
    try:
        inventory = user_accounts[username]["inventory"]
        games = list(game_library.keys())
        game_title = games[game_ID - 1]

        if game_title not in game_library:
            raise ValueError("Game does not exist in game library.")
        
        if quantity <= 0:
            raise ValueError("Invalid quantity. Please try again.")

        game = game_library[game_title]
        total_cost = game["cost"] * quantity

        balance = user_accounts[username]["balance"]
        if balance < total_cost:
            raise ValueError("Insufficient funds. Please top-up your account first.")

        if game_title in inventory:
            inventory[game_title] += quantity
        else:
            inventory[game_title] = quantity

        game_library[game_title]["quantity"] -= quantity
        user_accounts[username]["balance"] -= total_cost

        points = total_cost // 2
        user_accounts[username]["points"] += points

        print(f"\nSuccessfully rented {quantity}x of {game_title}.")
        print(f"\nTotal Cost: ${total_cost:.2f}. Remaining Balance: ${user_accounts[username]['balance']:.2f}")
        print(f"You earned {points} points from this transaction.")
        input("\nPress ENTER to return to user menu.")
        pause()
        logged_in_menu(username)

    except ValueError as e:
        print(str(e))
        input("\nPress ENTER to return to user menu.")
        pause()
        logged_in_menu(username)

# Function to return a game
def return_game(username, game_id_map):
    game_ID = int(input("\nEnter the ID of the game you wish to return: "))
    if game_ID in game_id_map:
        game = game_id_map[game_ID]
    if username in user_accounts:
        inventory = user_accounts[username]["inventory"]
        if inventory:
            if 1 <= game_ID <= len(game_id_map):
                game = game_id_map[game_ID]
                if game in inventory:
                    limit_quantity = inventory[game]
                    quantity = int(input(f"\nEnter the quantity of '{game}' you want to return: "))
                    if 1 <= quantity <= limit_quantity:
                        game_library[game]["quantity"] += quantity
                        inventory[game] -= quantity
                        print(f"\n Successfully returned {quantity}x of '{game}'")
                        if inventory[game] == 0:
                            del inventory[game]
                            pause()
                            print(f"\nAll games in your inventory have been returned.")
                    else:
                        print("Invalid quantity. Please try again")  
                else:
                    print("Game does not exist in user inventory.")
            else:
                print("Game ID does not exist. Please try again.")
        else:
            print("There are no games in your inventory.")
    else:
        print("User does not exist. Returning to main menu . . .") 
        pause()
        main_menu()
    input("\nPress ENTER to return to the user menu.")
    pause()
    logged_in_menu(username, game_id_map)

# Function to top-up user account
def top_up_account(username, amount):
    if amount == int(amount) and amount > 0:
        user_accounts[username]["balance"] += amount
        print(f"\nAccount top-up succesful. Your balance is now ${user_accounts[username]['balance']:.2f}.")
        input("\nPress ENTER to return to user menu.")
        pause()
        logged_in_menu(username)
    else:
        print("\nAccount top-up unsuccesful. Please input a valid amount.")
        pause()
        top_up_account(username,amount)

# Function to display user's inventory
def display_inventory(username):
    pause()
    if username in user_accounts:
        balance = user_accounts[username]["balance"]
        inventory = user_accounts[username]["inventory"]
        print(f"\nHello {username}, your current balance is ${balance:.2f}")
        print(f"\n{username}'s Game Library: \n")
        if inventory:
            count = 1
            game_id_map = {}
            for game in inventory:
                game_id_map[count] = game
                print(f"\n     {count}. {game}\n         Quantity: {inventory[game]}")
                count += 1
            input("\nPress ENTER to return to the user menu.")
            pause()
            logged_in_menu(username)
        else:
            print("You have no games in your library.")
            input("\n Press ENTER to return back to the user menu.")
            pause()
            logged_in_menu(username)
    else:
        print("User does not exist. Please try again")
        main_menu()

# Function for admin login
def admin_login():
    username = input("Enter admin username: ")
    if username == admin_username:
        password = input("Enter admin password: ")
        if password == admin_password:
            print("Admin login successful.")
            admin_menu()
        else:
            print("Admin login unsuccessful. Please try again.")
    else:
        print("Admin login unsuccessful. Please try again.")

# Function to edit game library, previously admin_update_games functio
def edit_library(game_ID):
    pause()
    game_keys = list(game_library.keys())
    if game_ID >= 1 and game_ID <= len(game_keys):
        game = game_keys[game_ID - 1]
        print(f"\n You are currently editing '{game}'.")
        print(f"\nGame Title: {game}\nQuantity: {game_library[game]["quantity"]}\nCost: ${game_library[game]["cost"]:.2f}")
        print("\n1. Edit Game Title\n2. Edit Game Quantity\n3. Edit Game Cost")
        choice = input("\n Enter choice: ")
        if choice == '1':
            edit_title = input("Enter new game title: ")
            game_library[edit_title] = game_library.pop(game)
        if choice == '2':
            edit_quantity = int(input("Enter new game quantity (Input a number ex. 1): "))
            game_library[game]["quantity"] = edit_quantity
        if choice == '3':
            edit_cost = float(input("Enter new game price (Enter a float number ex. 5.00): "))
            game_library[game]["cost"] = edit_cost
        else:
            print("Edit failed. Returning to admin menu.")
            pause()
            admin_menu()
        
        print(f"\n Successfully edited '{game}' details.")
        input("\n Press ENTER to return to admin menu.")
        pause()
        admin_menu()

    else:
        print("Game does not exist. Please try again.")
        pause()
        admin_menu()

# Admin menu
def admin_menu():
    pause()
    print("Welcome admin, what would you like to do?")
    print("\n1. View Admin Game Library\n2. Edit Game Library\n3. Return to Main Menu\n4. Exit")
    choice = input("\n Enter your choice: ")
    if choice == '1':
        display_game_inventory()
    elif choice == '2':
        display_available_games()
        game_ID = int(input("Enter the ID of the game you wish to edit: "))
        edit_library(game_ID)
    elif choice == '3':
        print("Returning to main menu . . .")
        pause()
        main_menu()
    elif choice == '4':
        print("Exiting program . . .")
        pause()
    else:
        pause()
        admin_menu()
    
# Function for users to redeem points for a free game rental
def redeem_free_rental(username):
    points = user_accounts[username]["points"]
    if points >= 3:
        print(f"You have {points} points available.")
        choice = input("Do you wish to rent a game for free? (Y/N): ").upper()
        if choice == 'Y':
            game_ID = int(input("Enter the Game ID of the game you want to rent: "))
            quantity = int(input("How many copies of this game would you like to rent?: "))
            games = list(game_library.keys())
            game_title = games[game_ID - 1]
            if game_title and game_title in game_library:
                game_title = games[game_ID - 1]
                if game_library[game_title]["quantity"] >= quantity:
                    game_library[game_title]["quantity"] -= quantity
                    user_accounts[username]["points"] -= 3
                    if game_title in user_accounts[username]["inventory"]:
                        user_accounts[username]["inventory"][game_title] += quantity
                    else:
                        user_accounts[username]["inventory"][game_title] = quantity
                    pause()
                    print(f"\n You have succesfully redeemed {quantity}x '{game_title}' for free!")
                    input("\nPress ENTER to return to the user menu.")
                    pause()
                    logged_in_menu(username)
                else:
                    print("\n There are not enough copies of this game to be rented.")
            else:
                print("\n Game does not exist in the game library.")
        else:
            print("Cancelling transaction.")
            pause()
    else:
        print("\n You do not have enough points to redeem a free game.")
    pause()
    logged_in_menu(username)

# Function to display game inventory
def display_game_inventory():
    pause()
    print("\n ADMIN GAME LIBRARY:\n")
    count = 1
    for game_title, game_info in game_library.items():
        currently_rented = sum(user_info["inventory"].get(game_title, 0) for user_info in user_accounts.values() )
        available_games = game_info["quantity"] - currently_rented
        print(f"{count}. {game_title}\n Available Copies: {available_games}\n Currently Rented Copies: {currently_rented}")
        count += 1

    input("\n Press ENTER to return to the admin menu.")
    pause()
    admin_menu()
 
# Function to handle user's logged-in menu
def logged_in_menu(username, game_id_map=None):
        print(f"Welcome {username}, what would you like to do?")
        print("\n1. View Game Inventory\n2. Rent Game\n3. Return Game\n4. Top-Up Balance\n5. Redeem Points\n6. Log-out")
        choice = input("\n Enter your choice: ")
        if choice == '1':
            display_inventory(username)
        elif choice =='2':
            pause()
            display_available_games()
            print("\n")
            balance = user_accounts[username]["balance"]
            print(f"Hello {username}, your current balance is ${balance:.2f}.")
            game_ID = int(input("Enter the Game ID of the game you want to rent: "))
            quantity = int(input("How many copies of this game would you like to rent?: "))
            rent_game(username, game_ID, quantity, game_id_map)
        elif choice == '3':
            pause()
            game_id_map = {}
            if username in user_accounts:
                inventory = user_accounts[username]["inventory"]
                print(f"\n{username}'s Game Library: \n")
                if inventory:
                    count = 1
                    for game in inventory:
                        print(f"\n     {count}. {game}\n         Quantity: {inventory[game]}")
                        game_id_map[count] = game
                        count += 1
                else:
                    print("You have no games in your library.")
                    input("Press ENTER to return to user menu.")
                    pause()
                    logged_in_menu(username, game_id_map)
            else:
                print("User does not exist. Returning to main menu . . .")
                pause()
                main_menu()
            
            return_game(username, game_id_map)
            
        elif choice == '4':
            pause()
            amount = int(input("Enter amount to top-up (ex. 5): "))
            top_up_account(username, amount)
        elif choice == '5':
            pause()
            redeem_free_rental()
        elif choice == '6':
            print("\nReturning to Main Menu . . .")
            pause()
            main_menu()
        elif choice == ' ':
            print("Transaction cancelled.")
            pause()
            main_menu()
        else:
            print("Invalid input. Please try again.")

# Function to display the main-menu

def main_menu():
    while True:
        print("Welcome to Hubert's Video Game Rentals.")
        print("\nWhat would you like to do?")
        print("\n1. Log-In\n2. Register\n3. View Game Library\n4. Admin Log-in\n5. Exit")
        choice = input("\n Enter your choice: ")
        if choice == '1':
            pause()
            login_user()
        elif choice == '2':
            pause()
            register_user()
        elif choice == '3':
            pause()
            display_available_games()
            input("\nPress ENTER to go back to the main menu.")
            pause()
        elif choice == '4':
            pause()
            admin_login()
        elif choice == '5':
            print("\nExiting program.")
            pause()
            break
        
        else:
            print("Invalid choice. Please try again.")
            pause()

    
# Main function to run the program
def main():
        main_menu()

if __name__ == "__main__":
    main()