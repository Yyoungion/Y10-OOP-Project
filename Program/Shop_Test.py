from Classes import *
from Object_Creation import *


# Initialize the shop inventory
shop_inventory = [
    Weapon("Fragile Stick", 1, 0, 0),
    Weapon("Club", 5, 10, 0),
    Weapon("Dull Sword", 10, 20, 0),
    Weapon("Short Sword", 15, 30, 1),
    Weapon("Sword", 20, 50, 3),
    Weapon("Lance", 30, 70, 3),
    Weapon("Spear", 35, 80, 5),
    Weapon("Enchanted Sword", 45, 100, 7),  
    Weapon("Enchanted Lance", 60, 120, 7),
    Weapon("Enchanted Spear", 75, 150, 10),
    Armor("Leather Armor", 5, 10),  
    Armor("Chainmail Armor", 15, 20),   
    Armor("Iron Armor", 25, 30),    
    Armor("Gold Armor", 30, 50),
    Armor("Enchanted Chainmail Armor", 50, 70),
    Armor("Enchanted Iron Armor", 70, 90),
    Armor("Enchanted Gold Armor", 100, 110),
    Potion("Health Potion", 20, 0, 10),
    Potion("Mana Potion", 0, 20, 10),]

# Initialize the player's inventory
player_inventory = []

# Initialize the player's gold
player_gold = 1000

def display_shop_inventory():
    print("Shop Inventory:")
    for i, item in enumerate(shop_inventory):
        print(f"{i + 1}. {item}")
    print("0. Exit")
    print()
def display_player_inventory():
    print("Player Inventory:")
    for i, item in enumerate(player_inventory):
        print(f"{i + 1}. {item}")
    print("0. Exit")
    print()
def buy_item(item_index):
    global player_gold
    if item_index < 0 or item_index >= len(shop_inventory):
        print("Invalid item index.")
        return

    item = shop_inventory[item_index]
    if player_gold >= item.cost:
        player_gold -= item.cost
        player_inventory.append(item)
        print(f"You bought {item.name} for {item.cost} gold.")
    else:
        print("You don't have enough gold to buy this item.")

def view_inventory():
    print("Your Inventory:")
    for i, item in enumerate(player_inventory):
        print(f"{i + 1}. {item}")

def main():
    while True:
        print("Welcome to the shop!")
        print("1. Buy")
        print("2. View Inventory")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            display_shop_inventory()
            item_choice = int(input("Enter the item number you want to buy: ")) - 1
            buy_item(item_choice)
        elif choice == "2":
            display_player_inventory()
        elif choice == "3":
            print("Thank you for visiting the shop!")
            break
        else:
            print("Invalid choice. Please try again.")
        print()

main()


