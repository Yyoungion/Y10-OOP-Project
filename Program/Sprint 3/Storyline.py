import UserInterface as UI
import CombatSystem as Combat
import sys
import time
import threading
import msvcrt
import textwrap

def slow_print(text, delay=0.03):
    skip = {"value": False}

    def wait_for_enter():
        try:
            msvcrt.getch()
        except ImportError:
            input()
        skip["value"] = True

    thread = threading.Thread(target=wait_for_enter, daemon=True)
    thread.start()

    i = 0
    length = len(text)
    while i < length:
        print(text[i], end='', flush=True)
        if skip["value"]:
            print(text[i+1:], end='', flush=True)
            break
        time.sleep(delay)
        i += 1

def Access_Inventory():
    inventory = Combat.Player.get_inventory()
    if not inventory:
        slow_print("Your inventory is empty.")
        return
    item_actions = {item.name: (lambda name=item.name: Use_Item(name)) for item in inventory}
    item_actions["Exit Inventory"] = lambda: None
    UI.DisplayScene("Inventory", "Select an item to use or exit:", item_actions)
    return

def Use_Item(item_name):
    result = Combat.Player.use_item(item_name)
    if result:
        print()
        input("Press Enter to continue...")
    else:
        slow_print(f"Could not use {item_name}.\n")
        input("Press Enter to continue...")

def BlacksmithTrade():
    Combat.Player.trade(Combat.Blacksmith_Bob)

def Blacksmith():
  while True: 

    UI.DisplayScene(
      "Blacksmith",
      "You walk into the blacksmith to see incredible weapons and armours",
      {
        "Trade": BlacksmithTrade,
        "Back to town": EnterRiverbendAgain
      }
    ) 

def MerchantTrade():
   Combat.Player.trade(Combat.Merchant_Charlie)

def Merchant():
  while True: 

    UI.DisplayScene(
      "Merchant",
      "You see many exotic items aound the merchant's stall",
      {
        "Trade":MerchantTrade,
        "Back to town":EnterRiverbendAgain
      }
  )

def Storyline():
    UI.DisplayTitle("The Burning Village")
    intro_text = "You wake up to find your home burning in the sunlight and a loud roar in the distance. You run outside to see your whole village ravaged by fire and a large winged beast flying away. You try to find your family but your efforts are worthless as you find out from the town mayor. Your Mother and Sister were trapped under a burning pile of wood and were burnt. You ask the mayor about your father and the mayor lowers his head. In a weak voice he says your father couldn't deal with the news of your mother and sister and has run away leaving you and the rest of the town. More Buildings collapse as you stand there sobbing but action for your survival must be done. Rocks are falling around you.\n"
    wrapped_text = "\n".join(textwrap.wrap(intro_text, width=140))
    slow_print(wrapped_text)
    print("")
    actions = {
        "Run to the forest": Run_to_Forest,
        "Climb a tree": Climb_Tree,
        "Hide in a cave": Hide_Cave,
        "Check Inventory": lambda: None
    }
    selected = UI.SelectAction(actions)
    if selected == "Check Inventory":
        Access_Inventory()
        Storyline()

def Run_to_Forest():
    UI.DisplayTitle("Run to the Forest")
    forest_text = "You run into the forest and find a small cave. You hide in the cave and wait for the danger to pass. After a while, you hear the sound of footsteps approaching. You hold your breath and try to stay quiet. Suddenly, a group of bandits enters the cave. They look around and spot you hiding in the corner. They draw their weapons and approach you. What do you do?\n"
    wrapped_text = "\n".join(textwrap.wrap(forest_text, width=140))
    slow_print(wrapped_text)
    print("")
    actions = {
        "Stand up and fight": BanditAttack,
        "Try to run away": lambda: (slow_print("You try to run away, but the bandits catch you!"), UI.DisplayGameOver())
    }
    UI.SelectAction(actions)

def Climb_Tree():
    UI.DisplayTitle("Climb Tree")
    climb_tree_text = "You climb up the tree and find a sturdy branch to sit on. From your vantage point, you see the village engulfed in flames and the dragon soaring away in the distance. You steady your breath, trying to process the chaos below. Suddenly, the branch beneath you snaps with a loud crack! You crash down, landing on top of a bandit and knocking him out cold. His companion, startled and angry, draws his weapon and advances toward you. You must act quickly.\n"
    wrapped_text = "\n".join(textwrap.wrap(climb_tree_text, width=140))
    slow_print(wrapped_text)
    print("")
    actions = {
        "Run away": lambda: (slow_print("You try to run away, but the bandit catches you!"), UI.DisplayGameOver()),
        "Fight the bandit": BanditAttack2
    }
    UI.SelectAction(actions)

def Hide_Cave():
    UI.DisplayTitle("Hide in Cave")
    hide_cave_text = "You hide in the cave and wait for the danger to pass. You hear the sound of footsteps approaching. You hold your breath and try to stay quiet. Suddenly, a group of bandits enters the cave. They look around and spot you hiding in the corner. They draw their weapons and approach you. You have to think fast!\n"
    wrapped_text = "\n".join(textwrap.wrap(hide_cave_text, width=140))
    slow_print(wrapped_text)
    print("")
    actions = {
        "Fight the bandits": BanditAttack,
        "Try to sneak past": lambda: (slow_print("You try to sneak past, but they notice you!"), UI.DisplayGameOver())
    }
    UI.SelectAction(actions)

def BanditAttack():
    Combat.BanditFight()
    UI.DisplayTitle("Bandit Attack")
    slow_print("\n".join(textwrap.wrap("You survive the bandit attack, but you are injured. You manage to escape the cave and find yourself back in the forest. You must decide your next move carefully.\n", width=140)))
    print("")
    actions = {
                   "Continue deeper into the forest": ContinueForest()
               }
    UI.SelectAction(actions)

def BanditAttack2():
    Combat.BanditFight2()
    UI.DisplayTitle("Bandit Attack")
    slow_print("\n".join(textwrap.wrap("You survive the bandit attack, but you are injured. You manage to escape the cave and find yourself back in the forest. You must decide your next move carefully.\n", width=140)))
    print("")
    actions = {
        "Continue deeper into the forest": ContinueForest()
    }
    UI.SelectAction(actions)

def ContinueForest():
    UI.DisplayTitle("Continue into the Forest")
    slow_print("\n".join(textwrap.wrap("You press on into the thick forest, the sounds of the burning village fading behind you. The trees close in, their shadows long and mysterious. Every step is uncertain, but you refuse to give up. Eventually, you catch sight of rooftops peeking through the foliage—a town called Riverbend. The warm glow of lanterns and the hum of distant voices offer hope and a brief respite from your ordeal.\n", width=140)))
    print("")
    actions = {
        "Enter Riverbend": EnterRiverbend,
        "Check Inventory": lambda: None
    }
    selected = UI.SelectAction(actions)
    if selected == "Check Inventory":
        Access_Inventory()
        ContinueForest()

def EnterRiverbend():
    UI.DisplayTitle("Enter Riverbend")
    slow_print("\n".join(textwrap.wrap("You enter the town of Riverbend. The bustling marketplace is alive with the chatter of townsfolk and the aroma of fresh bread. Stalls line the cobblestone streets, offering everything from shining weapons to exotic trinkets. You take a deep breath, feeling a sense of relief after your journey. As you rest, the warmth of the town helps your wounds begin to heal.\n", width=140)))
    print("")
    Combat.Player.health = Combat.Player.max_health
    Combat.Player.mana = Combat.Player.max_mana
    UI.DisplayStats(Combat.HeroName, Combat.Player.type, Combat.Player.health, Combat.Player.max_health, Combat.Player.mana, Combat.Player.max_mana)
    input("Press Enter to continue...")

    slow_print("\n".join(textwrap.wrap("As you wake and explore the small town, you find a blacksmith and a merchant where you can restock. You can also leave the town and continue into the forest in search of the dragon that killed your family.\n", width=140)))
    print("")
    actions = {
        "Visit the Blacksmith": Blacksmith,
        "Visit the Merchant": Merchant,
        "Leave Town": ContinueForest2
    }
    selected = UI.SelectAction(actions)
    if selected == "Visit the Blacksmith":
        Combat.Blacksmith()
        EnterRiverbendAgain()
    elif selected == "Visit the Merchant":
        Combat.Merchant()
        EnterRiverbendAgain()

def EnterRiverbendAgain():
    actions = {
        "Visit the Blacksmith": Blacksmith,
        "Visit the Merchant": Merchant,
        "Leave Town": ContinueForest2
    }
    selected = UI.SelectAction(actions)
    if selected == "Visit the Blacksmith":
        Combat.Blacksmith()
        EnterRiverbendAgain()
    elif selected == "Visit the Merchant":
        Combat.Merchant()
        EnterRiverbendAgain()

def ContinueForest2():
    exit()