import UserInterface as UI
import CombatSystem as Combat

# Main storyline function
def Storyline():
    # Display the title of the scene
    UI.DisplayTitle("The Burning Village")
    # Print the opening narrative
    print("""You wake up to find your home burning in the sunlight and a loud roar in the distance. 
You run outside to see your whole village ravaged by fire and a large winged beast flying away. 
You try to find your family but your efforts are worthless as you find out from the town mayor. 
Your Mother and Sister were trapped under a burning pile of wood and were burnt. 
You ask the mayor about your father and the mayor lowers his head. 
In a weak voice he says your father couldn't deal with the news of your mother and sister and has run away leaving you and the rest of the town. 
More Buildings collapse as you stand there sobbing but action for your survival must be done. 
Rocks are falling around you.""")
    # Define possible actions for the player
    actions = {
        "Run to the forest": Run_to_Forest,
        "Climb a tree": Climb_Tree,
        "Hide in a cave": Hide_Cave,
        "Check Inventory": lambda: None
    }
    # Let the player select an action
    selected = UI.SelectAction(actions)
    # If player checks inventory, show inventory and return to this scene
    if selected == "Check Inventory":
        Access_Inventory()
        Storyline()

# Action: Run to the forest
def Run_to_Forest():
    UI.DisplaySubTitle("Run to the Forest")
    print("""You run into the forest and find a small cave.
You hide in the cave and wait for the danger to pass.
After a while, you hear the sound of footsteps approaching.
You hold your breath and try to stay quiet.
Suddenly, a group of bandits enters the cave.
They look around and spot you hiding in the corner.
They draw their weapons and approach you.""")
    # Define actions in this scenario
    actions = {
        "Stand up and fight": BanditAttack,
        "Try to run away": lambda: (print("You try to run away, but the bandits catch you!"), UI.DisplayGameOver()),
        "Check Inventory": lambda: None
    }
    selected = UI.SelectAction(actions)
    # If player checks inventory, show inventory and return to this scene
    if selected == "Check Inventory":
        Access_Inventory()
        Run_to_Forest()

# Action: Climb a tree
def Climb_Tree():
    UI.DisplaySubTitle("Climb Tree")
    print("""You climb up the tree and find a branch to sit on.
You look around and see the village burning below you.
You see the dragon flying away in the distance.
You take a deep breath and try to calm down.
Suddenly, you hear a loud crack.
The branch you are sitting on is breaking!""")
    # Define actions in this scenario
    actions = {
        "Jump down quickly": lambda: print("You jump down and land safely, but you are shaken."),
        "Hold on tight": lambda: print("You hold on, but the branch snaps and you fall!"),
        "Check Inventory": lambda: None
    }
    selected = UI.SelectAction(actions)
    # If player checks inventory, show inventory and return to this scene
    if selected == "Check Inventory":
        Access_Inventory()
        Climb_Tree()

# Action: Hide in a cave
def Hide_Cave():
    UI.DisplaySubTitle("Hide in Cave")
    print("""You hide in the cave and wait for the danger to pass.
You hear the sound of footsteps approaching.
You hold your breath and try to stay quiet.
Suddenly, a group of bandits enters the cave.
They look around and spot you hiding in the corner.
They draw their weapons and approach you.
You have to think fast!""")
    # Define actions in this scenario
    actions = {
        "Fight the bandits": BanditAttack,
        "Try to sneak past": lambda: (print("You try to sneak past, but they notice you!"), UI.DisplayGameOver()),
        "Check Inventory": lambda: None
    }
    selected = UI.SelectAction(actions)
    # If player checks inventory, show inventory and return to this scene
    if selected == "Check Inventory":
        Access_Inventory()
        Hide_Cave()

# Handles the bandit attack scenario
def BanditAttack():
    # Start the combat with bandits
    Combat.BanditFight()

    # Display the aftermath scene
    UI.DisplayScene("Bandit Attack",
                    """You survive the bandit attack, but you are injured.
You manage to escape the cave and find yourself back in the forest.
""",
                    {
                        "Continue deeper into the forest": exit
                    })

# Allows the player to access and use items from their inventory
def Access_Inventory():
    inventory = Combat.Player.get_inventory()
    if not inventory:
        print("Your inventory is empty.")
        return
    # Create actions for each item in inventory
    item_actions = {item.name: (lambda name=item.name: Use_Item(name)) for item in inventory}
    item_actions["Exit Inventory"] = lambda: None
    # Display inventory scene
    UI.DisplayScene("Inventory", "Select an item to use or exit:", item_actions)
    return

# Handles using an item from the inventory
def Use_Item(item_name):
    result = Combat.Player.use_item(item_name)  # Use the Player instance
    if result:
        print()
        input("Press Enter to continue...")
    else:
        print(f"Could not use {item_name}.")
        input("Press Enter to continue...")
