import pyfiglet

# Displays the main title screen using ASCII art
def DisplayTitleScreen():
    print(pyfiglet.figlet_format("Beyond the Horizon"))

# Prints a separator line for UI formatting
def DisplaySeparator():
    print("+"+"-"*78+"+")

# Displays a formatted title with separators
def DisplayTitle(title):
    DisplaySeparator()
    print(f"| {title.center(76)} |")
    DisplaySeparator()

# Displays a subtitle with a separator below
def DisplaySubTitle(title):
    print(f"| {title:76} |")
    DisplaySeparator()

# Prompts the user to select an action from a list or dict of actions
def SelectAction(actions):
    while(True):
        DisplaySeparator()
        index=1
        # Determine if actions is a dict or list
        if isinstance(actions, dict):
            options = list(actions.keys())
        elif isinstance(actions, list):
            options = actions
        else:
            return
        
        # Display options with indices
        for option in options:
            print(index,"-",option)
            index+=1

        try:
            option_input = input("Selection: ")
            option_index = int(option_input)
            # Validate input range
            if option_index < 1 or option_index > len(options):
                print("Invalid selection. Please enter a number between 1 and", len(options))
                continue
            print("You have selected:", option_index)
            DisplaySeparator()
            action=options[option_index-1]
            print("You have selected:", action)
            # Call the selected action (if actions is a dict)
            actions[action]()
            return
        
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            exit()

# Displays a dialog with a title and description
def DisplayDialog(title, description):
    DisplayTitle(title)
    print(description)

# Displays a scene with a title, story, and available actions
def DisplayScene(title, story, actions):
    DisplayDialog(title, story)
    selection=SelectAction(actions)

# Displays a scene with an event occurring between two descriptions
def DisplaySceneWithEvent(title, pre_description, event, post_description, actions):
    DisplayDialog(title,pre_description)
    event()
    DisplayDialog(title,post_description)
    selection=SelectAction(actions)

# Displays character stats with colored health and mana bars
def DisplayStats(name, type, health, max_health, mana, max_mana, damage, defence):
    print(f"| Name: {name} |")
    print(f"| Type: {type} |")
    
    # Calculate bonus health if health exceeds max
    if health > max_health:
        bonus_health = health - max_health
        health = max_health
    else:
        bonus_health = 0

    # Health bar rendering
    bar_count = int(health * 10 / max_health)
    bars = "█" * bar_count
    dashes = "█" * (10 - bar_count)
    health_bar = f"\033[31m{bars}\033[0m{dashes}"

    if bonus_health > 0:
        bonus_bar_count = int(bonus_health * 10 / max_health)
        bonus_bars = "\033[33m" + "█" * bonus_bar_count + "\033[0m"
        health_bar += bonus_bars
        print(f"| Health❤️ : [{health_bar}]({health + bonus_health}/{max_health})|")
    else:
        print(f"| Health❤️ : [{health_bar}]({health}/{max_health})|")

    # Calculate bonus mana if mana exceeds max
    if mana > max_mana:
        bonus_mana = mana - max_mana
        mana = max_mana
    else:
        bonus_mana = 0

    # Mana bar rendering
    bar_count = int(mana * 10 / max_mana)
    bars = "█" * bar_count
    dashes = "█" * (10 - bar_count)
    mana_bar = f"\033[94m{bars}\033[0m{dashes}"

    if bonus_mana > 0:
        bonus_bar_count = int(bonus_mana * 10 / max_mana)
        bonus_bars = "\033[96m" + "█" * bonus_bar_count + "\033[0m"
        mana_bar += bonus_bars
        print(f"| Mana ✨: [{mana_bar}]({mana + bonus_mana}/{max_mana})|")
    else:
        print(f"| Mana ✨ : [{mana_bar}]({mana}/{max_mana})|")
        
    print(f"| Damage🗡️ : {damage} |")
    print(f"| Defence🛡️ : {defence} |")
    print("=======================================")

# Displays the player's inventory
def DisplayInventory(inventory):
    print("=======================================")
    print("Inventory")
    print("=======================================")
    for item in inventory:
        print(f"| {item} |")
    print("=======================================")

# Displays the game over screen
def DisplayGameOver():
    print("=======================================")
    print("Game Over")
    print("=======================================")
    print("You have died. Please restart the game.")
    print("=======================================")
    print("Thank you for playing Beyond the Horizon!")
    print("=======================================")
