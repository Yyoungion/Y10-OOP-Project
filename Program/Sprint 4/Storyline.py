import UserInterface as UI
import CombatSystem as Combat
import time
import threading
import msvcrt
import textwrap
import random
import sys

# Prints text slowly, allowing the user to skip by pressing a key

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

# Displays and manages the player's inventory
def Access_Inventory():
    inventory = Combat.Player.get_inventory()
    if not inventory:
        slow_print("Your inventory is empty.")
        return

    # Categorize items
    gold_items = [item for item in inventory if isinstance(item, Combat.Gold)]
    armour_items = [item for item in inventory if isinstance(item, Combat.Armour)]
    weapon_items = [item for item in inventory if isinstance(item, Combat.Weapon)]
    potion_items = [item for item in inventory if isinstance(item, (Combat.Healing, Combat.ManaHealing))]
    other_items = [
        item for item in inventory
        if not isinstance(item, (Combat.Gold, Combat.Armour, Combat.Weapon, Combat.Healing, Combat.ManaHealing))
    ]

    UI.DisplayTitle("Inventory")

    # Gold section
    if gold_items:
        for gold in gold_items:
            print(f"Gold: {gold.value} 🪙")
    else:
        print("Gold: 0 🪙")

    # Armour section
    print("\nArmour:")
    if armour_items:
        for item in armour_items:
            print(f" - {item.name} (Resist: {item.resistance}, Location: {item.location}, Value: {item.value} 🪙  )")
    else:
        print(" - None")

    # Weapons section
    print("\nWeapons:")
    if weapon_items:
        for item in weapon_items:
            print(f" - {item.name} (Damage: {item.damage}, Value: {item.value} 🪙  )")
    else:
        print(" - None")

    # Potions section
    print("\nPotions:")
    if potion_items:
        for item in potion_items:
            if isinstance(item, Combat.Healing):
                print(f" - {item.name} (Heals: {item.amount}, Value: {item.value} 🪙  )")
            elif isinstance(item, Combat.ManaHealing):
                print(f" - {item.name} (Restores Mana: {item.amount}, Value: {item.value} 🪙  )")
    else:
        print(" - None")

    # Other section
    print("\nOther:")
    if other_items:
        for item in other_items:
            print(f" - {item.name} (Value: {item.value} 🪙  )")
    else:
        print(" - None")

    # Build actions for usable items
    item_actions = {}
    for item in potion_items:
        item_actions[item.name] = (lambda name=item.name: Use_Item(name))
    item_actions["Exit Inventory"] = lambda: None

    UI.DisplaySubTitle("Select an item to use or exit:")
    UI.SelectAction(item_actions)
    return

# Uses an item from the inventory
def Use_Item(item_name):
    result = Combat.Player.use_item(item_name)
    if result:
        print()
        input("Press Enter to continue...")
    else:
        slow_print(f"Could not use {item_name}.\n")
        input("Press Enter to continue...")

# Initiates trade with the blacksmith
def BlacksmithTrade():
    Combat.Player.trade(Combat.Blacksmith_Bob)

# Blacksmith location logic
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

# Initiates trade with the merchant
def MerchantTrade():
   Combat.Player.trade(Combat.Merchant_Charlie)

# Merchant location logic
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

# Casino location logic
def Casino():
  while True:
    UI.DisplayTitle("Casino")
    slow_print("\n".join(textwrap.wrap(
      "You enter the bustling casino filled with the sounds of laughter and the clinking of coins. "
      "The air is thick with excitement as players gather around various tables, trying their luck at games of chance. "
      "You see a roulette table, a blackjack table, and a few slot machines in the corner. "
      "You can feel the thrill of the games calling to you.",
      width=140)))
    print("")
    actions = {
        "Play Roulette": Roulette,
        "Play Blackjack": Blackjack,
        "Exit Casino": EnterRiverbendAgain
    }
    UI.SelectAction(actions)

# Alternate casino menu for returning
def Casino2():
    UI.DisplayTitle("Casino")
    actions = {
        "Play Roulette": Roulette,
        "Play Blackjack": Blackjack,
        "Exit Casino": EnterRiverbendAgain
    }
    UI.SelectAction(actions)

# Roulette game logic
def Roulette():
    print("\nWelcome to the Roulette Table!")
    while True:
        player_gold = Combat.Player.get_gold().value
        print(f"\nYou have {player_gold} gold.")
        if player_gold <= 0:
            print("You have no gold left! You are escorted out of the casino.")
            EnterRiverbendAgain()

        print("What would you like to bet on?")
        print("1 - Red (pays 2x)")
        print("2 - Black (pays 2x)")
        print("3 - A number (1-36, pays 35x)")
        print("4 - Exit Roulette")
        try:
            choice = int(input("Enter your choice: "))
            if choice not in [1, 2, 3, 4]:
                print("Invalid choice. Please select a valid option.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 4:
            print("Leaving the roulette table.")
            Casino2()

        while True:
            bet = input("How much gold do you want to bet? ")
            try:
                bet = int(bet)
                if bet <= 0 or bet > player_gold:
                    print("Invalid bet amount.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
                continue

        if choice == 1 or choice == 2:
            color_bet = "Red" if choice == 1 else "Black"
            print(f"You bet {bet} gold on {color_bet}.")
            spin_color = random.choice(["Red", "Black", "Green"])
            print(f"The wheel spins... It lands on {spin_color}!")
            Combat.Player.get_gold().value -= bet
            if spin_color == color_bet:
                winnings = bet * 2
                print(f"You win {winnings} gold!")
                Combat.Player.get_gold().value += winnings
            else:
                print("You lost your bet.")
        elif choice == 3:
            number_bet = input("Pick a number between 1 and 36: ")
            try:
                number_bet = int(number_bet)
                if number_bet < 1 or number_bet > 36:
                    print("Invalid number.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue
            print(f"You bet {bet} gold on {number_bet}.")
            spin_number = random.randint(1, 36)
            print(f"The wheel spins... It lands on {spin_number}!")
            Combat.Player.get_gold().value -= bet
            if spin_number == number_bet:
                winnings = bet * 35
                print(f"Jackpot! You win {winnings} gold!")
                Combat.Player.get_gold().value += winnings
            else:
                print("You lost your bet.")
        else:
            print("Invalid choice. Try again.")

# Blackjack game logic
def Blackjack():
    print("\nWelcome to Blackjack!")
    deck = [str(n) for n in range(2, 11)] + ["J", "Q", "K", "A"]
    deck = deck * 4
    random.shuffle(deck)

    # Returns the value of a card
    def card_value(card):
        if card in ["J", "Q", "K"]:
            return 10
        elif card == "A":
            return 11
        else:
            return int(card)

    # Returns the total value of a hand, adjusting for aces
    def hand_value(hand):
        value = sum(card_value(card) for card in hand)
        # Adjust for Aces
        aces = hand.count("A")
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    player_gold = Combat.Player.get_gold().value
    if player_gold <= 0:
        print("You have no gold to bet!")
        Casino2()

    while True:
        print(f"\nYou have {player_gold} gold.")
        bet = input("How much gold do you want to bet? ")
        try:
            bet = int(bet)
            if bet <= 0 or bet > player_gold:
                print("Invalid bet amount.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        print(f"Your hand: {player_hand} (Value: {hand_value(player_hand)})")
        print(f"Dealer shows: {dealer_hand[0]}")

        # Player turn
        while True:
            if hand_value(player_hand) == 21:
                print("Blackjack!")
                print("")
                break
            move = input("Hit or Stand? (h/s): ").lower()
            if move == "h":
                player_hand.append(deck.pop())
                print(f"Your hand: {player_hand} (Value: {hand_value(player_hand)})")
                if hand_value(player_hand) > 21:
                    print("Bust! You lose.")
                    print("")
                    Combat.Player.get_gold().value -= bet
                    break
            elif move == "s":
                break
            else:
                print("Invalid input.")
        else:
            continue  

        # Dealer turn and outcome
        if hand_value(player_hand) <= 21:
            print(f"Dealer's hand: {dealer_hand} (Value: {hand_value(dealer_hand)})")
            while hand_value(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
                print(f"Dealer hits: {dealer_hand} (Value: {hand_value(dealer_hand)})")
            dealer_total = hand_value(dealer_hand)
            player_total = hand_value(player_hand)
            if dealer_total > 21 or player_total > dealer_total:
                winnings = bet
                print(f"You win {winnings} gold!")
                Combat.Player.get_gold().value += winnings
            elif player_total < dealer_total:
                print(f"Dealer wins. You lose {bet} gold.")
                Combat.Player.get_gold().value -= bet
            else:
                print("Push! It's a tie.")

        player_gold = Combat.Player.get_gold().value
        if player_gold <= 0:
            print("You have no gold left!")
            Casino2()
        while True:
            again = input("Play again? (y/n): ").lower()
            if again == "n":
                print("Leaving the blackjack table.")
                Casino2()
                break
            elif again == "y":
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

# Local dungeon logic and loop
def Local_Dungeon():
    slow_print("You enter the local dungeon. Prepare for a fight!")
    print("")
    Combat.BanditFight()
    print("")
    print(f"You have {Combat.Player.get_gold().value} gold.")
    Combat.Player.health = Combat.Player.max_health
    print(f"Your health has been restored to {Combat.Player.health}.")
    UI.DisplayStats(Combat.HeroName, Combat.Player.type, Combat.Player.health, Combat.Player.max_health, Combat.Player.mana, Combat.Player.max_mana)
    a = input("Do you want to do the dungeon again? (y/n): ").lower()
    while True:
        if a == "y":
            Local_Dungeon()
        elif a == "n":
            EnterRiverbendAgain()
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            a = input("Do you want to do the dungeon again? (y/n): ").lower()
            continue

# Main storyline introduction
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

# Forest path logic
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

# Tree path logic
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

# Cave path logic
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

# Bandit fight logic for forest/cave
def BanditAttack():
    Combat.BanditFight()
    UI.DisplayTitle("Bandit Attack")
    slow_print("\n".join(textwrap.wrap("You survive the bandit attack, but you are injured. You manage to escape the cave and find yourself back in the forest. You must decide your next move carefully.\n", width=140)))
    print("")
    actions = {
                   "Continue deeper into the forest": ContinueForest()
               }
    UI.SelectAction(actions)

# Bandit fight logic for tree path
def BanditAttack2():
    Combat.BanditFight2()
    UI.DisplayTitle("Bandit Attack")
    slow_print("\n".join(textwrap.wrap("You survive the bandit attack, but you are injured. You manage to escape the cave and find yourself back in the forest. You must decide your next move carefully.\n", width=140)))
    print("")
    actions = {
        "Continue deeper into the forest": ContinueForest()
    }
    UI.SelectAction(actions)

# Continue into the forest after bandit fight
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

# Enter the town of Riverbend
def EnterRiverbend():
    UI.DisplayTitle("Enter Riverbend")
    slow_print("\n".join(textwrap.wrap("You enter the town of Riverbend. The bustling marketplace is alive with the chatter of townsfolk and the aroma of fresh bread. Stalls line the cobblestone streets, offering everything from shining weapons to exotic trinkets. You take a deep breath, feeling a sense of relief after your journey. As you rest, the warmth of the town helps your wounds begin to heal.\n", width=140)))
    print("")
    Combat.Player.health = Combat.Player.max_health
    Combat.Player.mana = Combat.Player.max_mana
    UI.DisplayStats(Combat.HeroName, Combat.Player.type, Combat.Player.health, Combat.Player.max_health, Combat.Player.mana, Combat.Player.max_mana)
    input("Press Enter to continue...")

    slow_print("\n".join(textwrap.wrap("As you wake and explore the small town, you find a blacksmith and a merchant where you can restock. There is talk of a dungeon nearby where you can earn some gold. You can also leave the town and continue into the forest in search of the dragon that killed your family.\n", width=140)))
    print("")
    actions = {
        "Visit the Blacksmith": Blacksmith,
        "Visit the Merchant": Merchant,
        "Visit the Casino": Casino,
        "Visit the Local Dungeon": Local_Dungeon,
        "Check Inventory": lambda: None,
        "Leave Town": ContinueForest2
    }
    selected = UI.SelectAction(actions)
    if selected == "Check Inventory":
        Access_Inventory()
        EnterRiverbendAgain()

# Alternate Riverbend menu for returning
def EnterRiverbendAgain():
    actions = {
        "Visit the Blacksmith": Blacksmith,
        "Visit the Merchant": Merchant,
        "Visit the Casino": Casino,
        "Visit the Local Dungeon": Local_Dungeon,
        "Check Inventory": lambda: None,
        "Leave Town": ContinueForest2
    }
    selected = UI.SelectAction(actions)
    if selected == "Check Inventory":
        Access_Inventory()
        EnterRiverbendAgain()

# Continue deeper into the forest from Riverbend
def ContinueForest2():
    UI.DisplayTitle("Deeper into the Forest")
    slow_print("\n".join(textwrap.wrap(
        "You leave Riverbend behind, venturing deeper into the forest. The trees grow denser, and the path becomes harder to follow. You hear distant howls and the rustling of unseen creatures. As you push forward, you stumble upon a fork in the path. One trail leads toward a dark, ominous cave, while the other winds toward a sunlit clearing where you spot a mysterious figure tending a campfire.",
        width=140)))
    print("")
    actions = {
        "Investigate the cave": ExploreCave,
        "Approach the campfire": ApproachCampfire,
        "Check Inventory": lambda: None
    }
    selected = UI.SelectAction(actions)
    if selected == "Check Inventory":
        Access_Inventory()

# Explore the cave path
def ExploreCave():
    UI.DisplayTitle("The Dark Cave")
    slow_print("\n".join(textwrap.wrap(
        "You cautiously enter the cave, your footsteps echoing off the damp stone walls. The air is cold and heavy. Suddenly, you hear a low growl. A pair of glowing eyes appear in the darkness—a wild wolf leaps at you!",
        width=140)))
    print("")
    actions = {
        "Fight the skeleton": SkeletonFight,
        "Try to escape": lambda: (slow_print("You turn to run, but the skeleton is too fast. It catches up to you!"), UI.DisplayGameOver())
    }
    UI.SelectAction(actions)

# Skeleton fight logic
def SkeletonFight():
    Combat.SkeletonFight()
    UI.DisplayTitle("After the Battle")
    slow_print("\n".join(textwrap.wrap(
        "You defeat the skeleton after a fierce struggle.",
        width=140)))
    print("")

    input("Press Enter to continue...")
    CultistFightIntro()

# Approach the campfire path
def ApproachCampfire():
    UI.DisplayTitle("The Mysterious Stranger")
    slow_print("\n".join(textwrap.wrap(
        "You approach the campfire and see a hooded figure warming their hands. The stranger looks up and greets you with a nod. 'You look like you've been through a lot,' they say. 'Care to share some food and stories?'",
        width=140)))
    print("")
    actions = {
        "Sit and talk": TalkToStranger,
        "Attack the stranger": AttackTheStranger,
        "Leave quietly": CultistFightIntro
    }
    UI.SelectAction(actions)

# Attack the mysterious stranger
def AttackTheStranger():
    Combat.MysteriousStrangerFight()
    slow_print("You survived...")
    print("")
    slow_print("That was unexpected!")
    print("")
    input("Press Enter to continue...")
    CultistFightIntro()

# Talk to the mysterious stranger
def TalkToStranger():
    slow_print("\n".join(textwrap.wrap(
        "You sit by the fire and share your story. The stranger listens intently, then offers you some advice and a map of the forest. 'Beware the dragon's minions,' they warn. 'And trust no one.' You thank the stranger and continue your journey.",
        width=140)))
    print("")
    input("Press Enter to continue...")
    CultistFightIntro()

# Cultist encounter introduction
def CultistFightIntro():
    UI.DisplayTitle("Cultist Encounter")
    slow_print("\n".join(textwrap.wrap(
        "As you move deeper into the forest, you stumble upon a clearing illuminated by flickering torchlight. Three hooded cultist stands in the center, chanting in a strange tongue. Sensing your presence, they turn, eyes wild with fanatic devotion. They each take out a wicked dagger and rushes toward you, intent on sacrifice.",
        width=140)))
    print("")
    actions = {
        "Fight the cultist": CultistFight,
        "Run away": NoArtifact
    }
    UI.SelectAction(actions)

# Escape from cultists without artifact
def NoArtifact():
    slow_print("You escape the cultists and flee deeper into the forest. Eventually, you find your way to a peaceful village called Willowbrook.")
    print("")
    Willowbrook()

# Cultist fight logic
def CultistFight():
    Combat.Cultistfight()
    UI.DisplayTitle("After the Cultist Battle")
    slow_print("\n".join(textwrap.wrap(
        "You defeat the crazed cultist after a tense battle.",
        width=140)))
    print("")
    input("Press Enter to continue...")
    CultistBossIntro()

# Cultist boss encounter introduction
def CultistBossIntro():
    UI.DisplayTitle("Cultist Boss Encounter")
    slow_print("\n".join(textwrap.wrap(
        "As you catch your breath after the last battle, a chilling silence falls over the clearing. Suddenly, the torches flare with unnatural light, and a towering figure steps forward. Clad in dark robes adorned with sinister symbols, the cultist leader raises a staff crackling with dark energy. His eyes burn with fanatic zeal as he chants an ominous incantation. 'You have meddled in our sacred rites for the last time,' he hisses. 'Now, you will face the true power of the cult!'",
        width=140)))
    print("")
    actions = {
        "Fight the Cultist Boss": CultistBossFight
    }
    UI.SelectAction(actions)

# Cultist boss fight logic
def CultistBossFight():
    Combat.CultistFinalBoss()
    UI.DisplayTitle("After the Cultist Boss Battle")
    slow_print("\n".join(textwrap.wrap(
        "The cultist leader collapses, his staff clattering to the ground as the dark energy dissipates into the night. The forest is eerily quiet, save for your heavy breathing. You search the clearing and find a strange amulet among the cultist's belongings—its surface etched with runes that glow faintly in your hand. You use the artifact and you glow with warmth. You feel healthier. With the cultists defeated and the amulet in your possession, you gather your strength and press onward, determined to face whatever challenges await.",
        width=140)))
    print("")
    input("Press Enter to continue...")
    Willowbrook()

# Enter Willowbrook village
def Willowbrook():
    UI.DisplayTitle("Enter Willowbrook")
    slow_print("\n".join(textwrap.wrap(
        "You arrive at Willowbrook, a peaceful village nestled beside a sparkling river. The villagers greet you warmly, offering fresh bread and stories of their tranquil life. You notice a healer's hut, a bustling market, and a mysterious old tower at the edge of town.",
        width=140)))
    print("")
    UI.DisplayStats(Combat.HeroName, Combat.Player.type, Combat.Player.health, Combat.Player.max_health, Combat.Player.mana, Combat.Player.max_mana)
    input("Press Enter to continue...")

    slow_print("\n".join(textwrap.wrap(
        "As you explore Willowbrook, you can visit the healer to restore your strength, browse the market for rare items, or investigate the old tower rumored to be haunted.",
        width=140)))
    print("")

    actions = {
    "Visit the Healer": VisitHealer,
    "Visit the Market": VisitMarket,
    "Visit the Blacksmith": VisitBlacksmith,
    "Investigate the Tower": InvestigateTower,
    "Visit the Casino": VisitCasino,
    "Check Inventory": lambda: None,
    "Leave Willowbrook": ContinueForest3
    }
    selected = UI.SelectAction(actions)
    if selected == "Check Inventory":
        Access_Inventory()
        Willowbrook2()
        
# Alternate Willowbrook menu for returning
def Willowbrook2():
    actions = {
    "Visit the Healer": VisitHealer,
    "Visit the Market": VisitMarket,
    "Visit the Blacksmith": VisitBlacksmith,
    "Investigate the Tower": InvestigateTower,
    "Visit the Casino": VisitCasino,
    "Check Inventory": lambda: None,
    "Leave Willowbrook": ContinueForest3
    }
    selected = UI.SelectAction(actions)
    if selected == "Check Inventory":
        Access_Inventory()
        Willowbrook2()

# Willowbrook casino logic
def VisitCasino():
  while True:
    UI.DisplayTitle("Casino")
    slow_print("\n".join(textwrap.wrap(
      "You enter the bustling casino filled with the sounds of laughter and the clinking of coins. "
      "The air is thick with excitement as players gather around various tables, trying their luck at games of chance. "
      "You see a roulette table, a blackjack table, and a few slot machines in the corner. "
      "You can feel the thrill of the games calling to you.",
      width=140)))
    print("")
    actions = {
        "Play Roulette": Roulette,
        "Play Blackjack": Blackjack,
        "Exit Casino": Willowbrook2
    }
    UI.SelectAction(actions)

# Alternate Willowbrook casino menu
def Casino3():
    UI.DisplayTitle("Casino")
    actions = {
        "Play Roulette": Roulette2,
        "Play Blackjack": Blackjack2,
        "Exit Casino": Willowbrook2
    }
    UI.SelectAction(actions)

# Willowbrook roulette logic
def Roulette2():
    print("\nWelcome to the Roulette Table!")
    while True:
        player_gold = Combat.Player.get_gold().value
        print(f"\nYou have {player_gold} gold.")
        if player_gold <= 0:
            print("You have no gold left! You are escorted out of the casino.")
            Casino3()

        print("What would you like to bet on?")
        print("1 - Red (pays 2x)")
        print("2 - Black (pays 2x)")
        print("3 - A number (1-36, pays 35x)")
        print("4 - Exit Roulette")
        try:
            choice = int(input("Enter your choice: "))
            if choice not in [1, 2, 3, 4]:
                print("Invalid choice. Please select a valid option.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 4:
            print("Leaving the roulette table.")
            Casino3()

        while True:
            bet = input("How much gold do you want to bet? ")
            try:
                bet = int(bet)
                if bet <= 0 or bet > player_gold:
                    print("Invalid bet amount.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
                continue

        if choice == 1 or choice == 2:
            color_bet = "Red" if choice == 1 else "Black"
            print(f"You bet {bet} gold on {color_bet}.")
            spin_color = random.choice(["Red", "Black", "Green"])
            print(f"The wheel spins... It lands on {spin_color}!")
            Combat.Player.get_gold().value -= bet
            if spin_color == color_bet:
                winnings = bet * 2
                print(f"You win {winnings} gold!")
                Combat.Player.get_gold().value += winnings
            else:
                print("You lost your bet.")
        elif choice == 3:
            number_bet = input("Pick a number between 1 and 36: ")
            try:
                number_bet = int(number_bet)
                if number_bet < 1 or number_bet > 36:
                    print("Invalid number.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue
            print(f"You bet {bet} gold on {number_bet}.")
            spin_number = random.randint(1, 36)
            print(f"The wheel spins... It lands on {spin_number}!")
            Combat.Player.get_gold().value -= bet
            if spin_number == number_bet:
                winnings = bet * 35
                print(f"Jackpot! You win {winnings} gold!")
                Combat.Player.get_gold().value += winnings
            else:
                print("You lost your bet.")
        else:
            print("Invalid choice. Try again.")

# Willowbrook blackjack logic
def Blackjack2():
    print("\nWelcome to Blackjack!")
    deck = [str(n) for n in range(2, 11)] + ["J", "Q", "K", "A"]
    deck = deck * 4
    random.shuffle(deck)

    def card_value(card):
        if card in ["J", "Q", "K"]:
            return 10
        elif card == "A":
            return 11
        else:
            return int(card)

    def hand_value(hand):
        value = sum(card_value(card) for card in hand)
        # Adjust for Aces
        aces = hand.count("A")
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    player_gold = Combat.Player.get_gold().value
    if player_gold <= 0:
        print("You have no gold to bet!")
        Casino3()

    while True:
        print(f"\nYou have {player_gold} gold.")
        bet = input("How much gold do you want to bet? ")
        try:
            bet = int(bet)
            if bet <= 0 or bet > player_gold:
                print("Invalid bet amount.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        print(f"Your hand: {player_hand} (Value: {hand_value(player_hand)})")
        print(f"Dealer shows: {dealer_hand[0]}")

        # Player turn
        while True:
            if hand_value(player_hand) == 21:
                print("Blackjack!")
                print("")
                break
            move = input("Hit or Stand? (h/s): ").lower()
            if move == "h":
                player_hand.append(deck.pop())
                print(f"Your hand: {player_hand} (Value: {hand_value(player_hand)})")
                if hand_value(player_hand) > 21:
                    print("Bust! You lose.")
                    print("")
                    Combat.Player.get_gold().value -= bet
                    break
            elif move == "s":
                break
            else:
                print("Invalid input.")
        else:
            continue  

        if hand_value(player_hand) <= 21:
            print(f"Dealer's hand: {dealer_hand} (Value: {hand_value(dealer_hand)})")
            while hand_value(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
                print(f"Dealer hits: {dealer_hand} (Value: {hand_value(dealer_hand)})")
            dealer_total = hand_value(dealer_hand)
            player_total = hand_value(player_hand)
            if dealer_total > 21 or player_total > dealer_total:
                winnings = bet
                print(f"You win {winnings} gold!")
                Combat.Player.get_gold().value += winnings
            elif player_total < dealer_total:
                print(f"Dealer wins. You lose {bet} gold.")
                Combat.Player.get_gold().value -= bet
            else:
                print("Push! It's a tie.")

        player_gold = Combat.Player.get_gold().value
        if player_gold <= 0:
            print("You have no gold left!")
            Casino2()
        while True:
            again = input("Play again? (y/n): ").lower()
            if again == "n":
                print("Leaving the blackjack table.")
                Casino3()
                break
            elif again == "y":
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

# Visit the healer in Willowbrook
def VisitHealer():
    UI.DisplayTitle("Healer's Hut")
    slow_print("\n".join(textwrap.wrap(
        "The healer welcomes you and tends to your wounds. You feel rejuvenated and ready for your next adventure.",
        width=140)))
    print("")
    Combat.Player.health = Combat.Player.max_health
    Combat.Player.mana = Combat.Player.max_mana
    UI.DisplayStats(Combat.HeroName, Combat.Player.type, Combat.Player.health, Combat.Player.max_health, Combat.Player.mana, Combat.Player.max_mana)
    input("Press Enter to return to Willowbrook...")
    Willowbrook2()

# Visit the market in Willowbrook
def VisitMarket():
    UI.DisplayTitle("Willowbrook Market")
    slow_print("\n".join(textwrap.wrap(
        "The market is filled with colorful stalls selling potions, trinkets, and rare ingredients. You might find something useful for your journey.",
        width=140)))
    print("")
    Combat.Player.trade(Combat.Merchant_Charlie)
    input("Press Enter to return to Willowbrook...")
    Willowbrook2()

# Visit the blacksmith in Willowbrook
def VisitBlacksmith():
    UI.DisplayTitle("Willowbrook Blacksmith")
    slow_print("\n".join(textwrap.wrap(
        "You enter the blacksmith's workshop, filled with the sound of hammering and the glow of hot metal. The blacksmith greets you and offers to trade weapons and armor.",
        width=140)))
    print("")
    Combat.Player.trade(Combat.Blacksmith_Bob)
    input("Press Enter to return to Willowbrook...")
    Willowbrook2()

# Investigate the old tower in Willowbrook
def InvestigateTower():
    UI.DisplayTitle("The Old Tower")
    slow_print("\n".join(textwrap.wrap(
        "You approach the old tower, its stones covered in moss. As you enter, you sense a magical presence. Suddenly, a ghostly figure appears, challenging you to a riddle or a duel.",
        width=140)))
    print("")
    actions = {
        "Solve the riddle": SolveRiddle,
        "Fight the ghost": FightGhost,
        "Leave": Willowbrook2
    }
    UI.SelectAction(actions)

# Solve the ghost's riddle
def SolveRiddle():
    UI.DisplayTitle("The Riddle")
    slow_print("The ghost asks: 'I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?'")
    print("")
    answer = input("Your answer: ").strip().lower()
    if "echo" in answer:
        slow_print("The ghost smiles and vanishes, blessing you. You feel a bit healthier")
        print("")
        Combat.Player.max_health = Combat.Player.max_health + 50
        Combat.Player.health = Combat.Player.max_health

    else:
        slow_print("The ghost wails and attacks!")
        FightGhost()

    input("Press Enter to return to Willowbrook...")
    Willowbrook2()

# Fight the ghost in the tower
def FightGhost():
    Combat.GhostFight()
    input("Press Enter to return to Willowbrook...")
    Willowbrook2()

# Continue journey after Willowbrook
def ContinueForest3():
    UI.DisplayTitle("Journey Continues")
    slow_print("\n".join(textwrap.wrap(
        "With new supplies and knowledge, you press on into the thick forest. The forest thins, and you see the silhouette of a ruined castle in the distance. "
        "You sense that your quest for vengeance is only just beginning...",
        width=140)))
    print("")
    actions = {
        "Approach the castle": Approach_The_Castle,
        "Check Inventory": lambda: None,
    }
    selected = UI.SelectAction(actions)
    if selected == "Check Inventory":
        Access_Inventory()
        ContinueForest3()

# Approach the castle
def Approach_The_Castle():
    UI.DisplayTitle("Approaching the Castle")
    slow_print("\n".join(textwrap.wrap(
        "You approach the castle, your heart pounding with anticipation. The gates are ajar, and you can see shadows moving inside. "
        "This is where your journey will truly begin, where you will face the dragon and avenge your family.",
        width=140)))
    print("")
    actions = {
        "Enter the castle": SpiderAndSkeletonIntro,
        "Check Inventory": lambda: None,
    }
    selected = UI.SelectAction(actions)
    if selected == "Check Inventory":
        Access_Inventory()
        Approach_The_Castle()

# Spider and skeleton fight introduction
def SpiderAndSkeletonIntro():
    UI.DisplayTitle("Spider and Skeleton Fight")
    slow_print("\n".join(textwrap.wrap(
        "As you enter the dimly lit chamber, two giant spiders descend from the ceiling, their fangs bared. "
        "At the same time, a skeleton emerges from the shadows, brandishing a bow. "
        "You must fight them both to survive!",
        width=140)))
    print("")
    actions = {
        "Fight the spider": SpiderAndSkeletonFight
    }
    UI.SelectAction(actions)

# Spider and skeleton fight logic
def SpiderAndSkeletonFight():
    Combat.SpiderAndSkeletonFight()
    UI.DisplayTitle("After the Battle")
    slow_print("\n".join(textwrap.wrap(
        "You defeat the spiders and skeleton, but you are injured. You manage to escape the chamber and find yourself in a long hallway. ",
        width=140)))
    print("")
    actions = {
        "Continue deeper into the castle": ContinueCastle
    }
    UI.SelectAction(actions)

# Continue deeper into the castle
def ContinueCastle():
    UI.DisplayTitle("Deeper into the Castle")
    slow_print("\n".join(textwrap.wrap(
        "You go through the castle, at the end of the hallway you find a large door. You crack it open a find a large room filled with goblins.",
        width=140)))
    print("")
    actions = {
        "Attack the Goblins": GoblinFight,
        "Check Inventory": lambda: None
    }
    selected = UI.SelectAction(actions)
    if selected == "Check Inventory":
        Access_Inventory()
        ContinueCastle()

# Goblin fight logic
def GoblinFight():
    Combat.GoblinFight()
    UI.DisplayTitle("After the Goblin Fight")
    slow_print("\n".join(textwrap.wrap(
        "You defeat the goblins, but you are injured. You manage to escape the room and find yourself in yet another long hallway. ",
        width=140)))
    print("")
    actions = {
        "Continue deeper into the castle": ContinueCastle2
    }
    UI.SelectAction(actions)

# Continue deeper into the castle after goblins
def ContinueCastle2():
    UI.DisplayTitle("Deeper into the Castle")
    slow_print("\n".join(textwrap.wrap(
        "You go through the castle, at the end of the hallway you find a large door. You crack it open and this time you find a large room filled with treasure.",
        width=140)))
    print("")
    actions = {
        "Take the treasure": TakeTreasure,
        "Check Inventory": lambda: None
    }
    selected = UI.SelectAction(actions)
    if selected == "Check Inventory":
        Access_Inventory()
        ContinueCastle2()
    
# Take the treasure and proceed to dragon fight
def TakeTreasure():
    Combat.LootRoom()
    DragonFightIntro()
    
# Dragon fight introduction
def DragonFightIntro():
    UI.DisplayTitle("The Dragon")
    slow_print("\n".join(textwrap.wrap(
        "With the treasure in hand, you step into the final chamber. The ground trembles as the mighty dragon emerges from the shadows, its scales glinting in the dim light. "
        "This is the beast that destroyed your village and family. The air is thick with heat and danger. The dragon fixes its gaze on you, smoke curling from its nostrils.",
        width=140)))
    print("")
    actions = {
        "Fight the Dragon": DragonFight
    }
    UI.SelectAction(actions)

# Dragon fight logic
def DragonFight():
    Combat.DragonFight()
    Winner()

# End of game victory screen
def Winner():
    UI.DisplayTitle("Victory!")
    slow_print("\n".join(textwrap.wrap(
        "With a final, triumphant blow, you slay the dragon. The beast collapses, its reign of terror finally ended. "
        "You stand victorious amidst the ruins, the memory of your family burning bright in your heart. "
        "The people of the land will remember your courage and sacrifice for generations to come. "
        "Congratulations, hero.You have avenged your family and restored peace to the realm.",
        width=140)))
    print("")
    input("Press Enter to exit the game...")
    sys.exit()
