def show_intro():
    print("===================================")
    print("     WELCOME TO THE TEXT QUEST")
    print("===================================")
    print("Type one of the commands below to begin your journey.\n")

def show_options():
    print("Available commands:")
    print(" - move")
    print(" - help")
    print(" - inventory")
    print(" - quit\n")

def show_help():
    print("\nHELP:")
    print(" - move: explore a new location")
    print(" - inventory: check what you're carrying")
    print(" - quit: exit the game\n")

def show_inventory():
    print("\nINVENTORY:")
    print(" - Map")
    print(" - Lantern")
    print(" - Apple\n")

def movement():
    print("\nPlayer moves north, east, south or west...\n")

def quit_game():
    print("\nThanks for playing. Goodbye!\n")

def main():
    show_intro()
    show_options()

    while True:
        command = input("> ").strip().lower()

        if command == "move":
            movement()
        elif command == "help":
            show_help()
        elif command == "inventory":
            show_inventory()
        elif command == "quit":
            quit_game()
            break
        else:
            print("Unknown command. Type 'help' to see available commands.\n")

if __name__ == "__main__":
    main()