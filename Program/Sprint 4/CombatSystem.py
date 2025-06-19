import UserInterface as UI
import random

# Prompt the user to enter their hero's name
HeroName = input("Enter your name: ")

# Function to display a selection dialog and return the selected item
def select_dialog(prompt, items):
    while(True):
        index = 1
        UI.DisplayTitle(prompt)
        for item in items:
            if isinstance(item, Item):
                print(f"{index:2} - {item.name:20} {item.value:5} 🪙")
            else:
                print(f"{index:2} - {item.name:20}")
            index += 1
        try:
            item_index = int(input("Selection: "))
            item = items[item_index-1]
            print("You have selected:", item.name)
            return item
        except:
            print("Stop being an idiot!!!")
            continue

# Function to roll a dice with a given number of sides and print the result
def roll_dice(prompt, sides):
    result = random.randrange(1, sides)
    print(f"{prompt}: {result}")
    return result

# Base class for all items
class Item(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

# Healing item that restores health
class Healing(Item):
    def __init__(self, name, value, amount):
        super().__init__(name, value)
        self.amount = amount

# Mana healing item that restores mana
class ManaHealing(Item):
    def __init__(self, name, value, amount):
        super().__init__(name, value)
        self.amount = amount

# Gold item representing currency
class Gold(Item):
    def __init__(self, value):
        self.value = value
        super().__init__(f"Bag Of Gold", value)

# Weapon item with damage attribute
class Weapon(Item):
    def __init__(self, name, value, damage):
        super().__init__(name, value)
        self.resistance = 0
        self.damage = damage

# Armour item with resistance and location attributes
class Armour(Item):
    def __init__(self, name, value, resistance, location):
        super().__init__(name, value)
        self.resistance = resistance
        self.location = location

# Base class for all characters (player, enemies, NPCs)
class Character(object):
    def __init__(self, name, type, health, max_mana=0):
        # Equipped items (default to "Nothing")
        self.equipped = {
            'Head': Armour("Nothing", 0, 0, "Head"),
            'Torso': Armour("Nothing", 0, 0, "Torso"),
            'Legs': Armour("Nothing", 0, 0, "Legs"),
            'Weapon': Weapon("Nothing", 0, 0)
        }
        self.name = name
        self.type = type
        self.health = health
        self.max_health = health
        self.inventory = []
        self.mana = max_mana
        self.max_mana = max_mana

    # Display character stats using UI
    def stats(self):
        UI.DisplayStats(self.name, self.type, self.health, self.max_health, self.mana, self.max_mana)

    # Get inventory, optionally filtered by item type
    def get_inventory(self, item_type=None):
        if item_type is None:
            return self.inventory
        return [item for item in self.inventory if isinstance(item, item_type)]

    # Display the character's inventory
    def DisplayInventory(self):
        self.show_item_list(f"{self.name} inventory:", self.inventory)

    # Get only armour items from inventory
    def get_inventory_armour(self):
        return self.get_inventory(Armour)

    # Use an item by name (healing, mana, etc.)
    def use_item(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                if isinstance(item, Healing):
                    self.heal(item.amount)
                    print(f"{self.name} used {item.name} and healed for {item.amount} HP.")
                    self.stats()
                    self.remove(item.name)
                    return True
                elif isinstance(item, ManaHealing):
                    self.mana += item.amount
                    if self.mana > self.max_mana:
                        self.mana = self.max_mana
                    print(f"{self.name} used {item.name} and restored {item.amount} Mana.")
                    self.stats()
                    self.remove(item.name)
                    return True
                else:
                    print(f"{item.name} cannot be used directly.")
                    return False
        print(f"{item_name} not found in inventory.")
        return False

    # Equip an item (weapon or armour)
    def equip(self, item):
        if isinstance(item, Weapon):
            self.equipped["Weapon"] = item
        elif isinstance(item, Armour):
            self.equipped[item.location] = item
        elif isinstance(item, Healing):
            self.heal(item.amount)
            self.remove(item.name)

    # Unequip an item (replace with "Nothing")
    def unequip(self, item):
        for location in self.equipped.keys():
            if item == self.equipped[location]:
                if isinstance(item, Weapon):
                    self.equipped[location] = Weapon("Nothing", 0, 0)
                elif isinstance(item, Armour):
                    self.equipped[location] = Armour("Nothing", 0, 0, location)

    # Get the gold item from inventory, or create one if not present
    def get_gold(self):
        for destination_item in self.inventory:
            if isinstance(destination_item, Gold):
                return destination_item
        destination_item = Gold(0)
        self.inventory.append(destination_item)
        return destination_item

    # Add gold from another item
    def add_gold(self, source_item):
        gold = self.get_gold()
        gold.value += source_item.value

    # Add an item to inventory (special handling for gold)
    def give(self, item):
        if isinstance(item, Gold):
            self.add_gold(item)
        else:
            self.inventory.append(item)

    # Remove an item from inventory by name
    def remove(self, target_item_name):
        for inventory_item in self.inventory:
            if target_item_name == inventory_item.name:
                self.unequip(inventory_item)
                self.inventory.remove(inventory_item)
                return

    # Give and equip an item
    def give_and_equip(self, item):
        self.give(item)
        self.equip(item)

    # Show currently equipped items
    def show_equiped(self):
        UI.DisplayTitle("Equiped items")
        for location in self.equipped.keys():
            print(f"{location:10}:", self.equipped[location].name)

    # Dialog for equipping or using items
    def equip_dialog(self):
        while True:
            print("What would you like to do?")
            print(" 1 - Equip an item")
            print(" 2 - Use an item")
            print(" 3 - No (exit)")
            response = input("Selection: ").strip()
            if response == '1':
                response = 'equip'
            elif response == '2':
                response = 'use'
            elif response == '3':
                response = 'no'
            else:
                response = ''
            if response == 'equip':
                item = select_dialog("Equip item", self.inventory)
                already_equipped = False
                if isinstance(item, Weapon):
                    already_equipped = self.equipped["Weapon"] == item
                elif isinstance(item, Armour):
                    already_equipped = self.equipped[item.location] == item
                if already_equipped:
                    self.unequip(item)
                    print(f"{item.name} has been unequipped.")
                    self.show_equiped()
                elif isinstance(item, (Weapon, Armour)):
                    self.equip(item)
                    print(f"{item.name} has been equipped.")
                    self.show_equiped()
                else:
                    print(f"{item.name} cannot be equipped.")

            elif response == 'use':
                item = select_dialog("Use item", self.inventory)
                if isinstance(item, (Healing, ManaHealing)):
                    self.use_item(item.name)
                else:
                    print(f"{item.name} cannot be used directly.")

            elif response == 'no':
                print("No items equipped.")
                return

            else:
                print("Invalid option. Please choose 'Equip', 'Use', or 'No'.")
                continue

    # Show a list of items with their values
    def show_item_list(self, title, list):
        UI.DisplayTitle(title)
        index = 1
        for item in list:
            print(f"{index:2} - {item.name:20} {item.value:5} 🪙")
            index += 1

    # Calculate total resistance from equipped armour
    def get_total_resistance(self):
        resistance = 0
        for location in self.equipped.keys():
            resistance = resistance + self.equipped[location].resistance
        return resistance

    # Attack another character (calculates damage, applies resistance)
    def attack(self, target):
        sides = 6
        attack_roll = roll_dice(f"{self.name}'s Attack Roll", sides)
        attack_damage = int((self.equipped["Weapon"].damage * attack_roll) / sides)
        resistance = target.get_total_resistance()
        if resistance == 0:
            armoured_attack_damage = attack_damage
        else:
            armoured_attack_damage = round(attack_damage / resistance)
            if armoured_attack_damage == 0:
                armoured_attack_damage = 1

        print(f"After resistance ({resistance}), {target.name} takes {armoured_attack_damage} damage.")
        if armoured_attack_damage < 0:
            armoured_attack_damage = 0
        target.health -= armoured_attack_damage

    # Heal the character by a certain amount (not above max health)
    def heal(self, amount):
        self.health = self.health + amount
        if self.health > self.max_health:
            self.health = self.max_health

    # Check if the character is dead
    def is_dead(self):
        if self.health <= 0:
            return True
        return False

    # Sell an item to another character
    def sell(self, target):
        item = select_dialog(f"{self.name} selling to {target.name}", self.inventory)
        if isinstance(item, Gold):
            return
        target_gold = target.get_gold()
        self_gold = self.get_gold()
        if target_gold.value >= item.value:
            print(f"{self.name} sold the the {item.name} to {target.name} for {item.value} gold")
            target.give(item)
            self.remove(item.name)
            target_gold.value -= item.value
            self_gold.value += item.value
        else:
            print(f"{target.name} does not have enough gold")

    # Buy an item from another character
    def buy(self, target):
        target.sell(self)

    # Trade dialog between two characters
    def trade(self, target):
        while True:
            self.DisplayInventory()
            target.DisplayInventory()
            UI.DisplayTitle(f"{self.name} is trading with {target.name}")
            index = 1
            options = ["Buy from them", "Sell to them", "Stop Trading"]
            for option in options:
                print(f"{index:2} - {option:20}")
                index += 1
            try:
                option_index = int(input("Selection: "))
                option = options[option_index - 1]
                print("You have selected:", option)
                if option == "Buy from them":
                    target.sell(self)
                elif option == "Sell to them":
                    self.sell(target)
                else:
                    return
            except Exception:
                print("Please select a valid option")
                continue

    # Fight sequence between self and a list of enemies
    def fight(self, enemies):
        UI.DisplayTitle("A fight has started")
        round = 1
        while(True):
            UI.DisplayTitle(f"Round {round}")
            round += 1
            self.stats()
            live_enemies = []
            for enemy in enemies:
                if not enemy.is_dead():
                    enemy.stats()
                    live_enemies.append(enemy)

            if len(live_enemies) == 0:
                print("YOU WIN!!!")
                return True
            self.equip_dialog()
            target = select_dialog("Who will you attack?", live_enemies)
            self.attack(target)
            for enemy in live_enemies:
                enemy.attack(self)
                if self.is_dead():
                    UI.DisplayGameOver()
                    exit(0)

# Hero class (player character)
class Hero(Character):
    def __init__(self, name):
        super().__init__(name, "Human", 100, max_mana=50)
        self.give_and_equip(Weapon("Stick", 0, random.randrange(5, 15)))
        self.give(ManaHealing("Lvl 1 Mana Potion", 5, 10))
        self.give(Healing("Lvl 1 Health Potion", 5, 10))
        self.give(Gold(10))

# Goblin enemy class
class Goblin(Character):
    def __init__(self, name):
        super().__init__(name, "Goblin", random.randrange(40, 50), max_mana=0)
        self.give_and_equip(Weapon("Club", 1, random.randrange(5, 10)))

# Human enemy class
class Human(Character):
    def __init__(self, name):
        super().__init__(name, "Human", 25, max_mana=0)
        self.give_and_equip(Weapon("Level 1 Wooden Sword", 2, 5))

# Unbeatable human (boss enemy)
class UnbeatableHuman(Character):
    def __init__(self, name):
        super().__init__(name, "Unbeatable Human", 1000, max_mana=0)
        self.give_and_equip(Weapon("Unbeatable Sword", 100, 2000))
        self.give_and_equip(Armour("Unbeatable Chestplate", 100, 100, 'Torso'))
        self.give_and_equip(Armour("Unbeatable Helmet", 100, 100, 'Head'))
        self.give_and_equip(Armour("Unbeatable Leggings", 100, 100, 'Legs'))

# Merchant NPC class
class Merchant(Character):
    def __init__(self, name):
        super().__init__(name, "Merchant", random.randrange(50, 55), max_mana=0)
        self.give(Healing("Lvl 1 Health Potion", 5, 10))
        self.give(Healing("Lvl 2 Health Potion", 15, 20))
        self.give(Healing("Lvl 3 Health Potion", 25, 30))
        self.give(Healing("Lvl 4 Health Potion", 40, 50))
        self.give(ManaHealing("Lvl 1 Mana Potion", 5, 10))
        self.give(ManaHealing("Lvl 2 Mana Potion", 15, 20))
        self.give(ManaHealing("Lvl 3 Mana Potion", 25, 30))
        self.give(ManaHealing("Lvl 4 Mana Potion", 40, 50))
        self.give(Gold(10000000000))

# Blacksmith NPC class
class Blacksmith(Character):
    def __init__(self, name):
        super().__init__(name, "Blacksmith", random.randrange(50, 55), max_mana=0)
        self.give(Weapon("Lvl 1 Wooden Sword", 3, 5))
        self.give(Weapon("Lvl 2 Wooden Sword", 6, 10))
        self.give(Weapon("Lvl 3 Wooden Sword", 9, 15))

        self.give(Weapon("Lvl 1 Metal Sword", 13, 20))
        self.give(Weapon("Lvl 2 Metal Sword", 16, 25))
        self.give(Weapon("Lvl 3 Metal Sword", 19, 30))

        self.give(Weapon("Lvl 1 Diamond Sword", 23, 35))
        self.give(Weapon("Lvl 2 Diamond Sword", 26, 40))
        self.give(Weapon("Lvl 3 Diamond Sword", 29, 45))

        self.give(Armour("Leather chestplate", 5, 2, 'Torso'))
        self.give(Armour("Leather helmet", 2, 1, 'Head'))
        self.give(Armour("Leather leggings", 4, 2, 'Legs'))

        self.give(Armour("Metal chestplate", 15, 11, 'Torso'))
        self.give(Armour("Metal helmet", 12, 10, 'Head'))
        self.give(Armour("Metal leggings", 14, 10, 'Legs'))

        self.give(Armour("Diamond chestplate", 25, 20, 'Torso'))
        self.give(Armour("Diamond helmet", 22, 15, 'Head'))
        self.give(Armour("Diamond leggings", 24, 15, 'Legs'))

        self.give(Gold(10000000000))

# Skeleton enemy class
class Skeleton(Character):
    def __init__(self, name):
        super().__init__(name, "Skeleton", random.randrange(40, 60), max_mana=0)
        self.give_and_equip(Weapon("Level 1 Wooden Bow", 5, random.randrange(17, 27)))

# Spider enemy class
class Spider(Character):
    def __init__(self, name):
        super().__init__(name, "Spider", random.randrange(40, 60), max_mana=0)
        self.give_and_equip(Weapon("Fangs", 0, random.randrange(15, 27)))

# Dragon boss enemy class
class Dragon(Character):
    def __init__(self, name):
        super().__init__(name, "Dragon", 100, max_mana=0)
        self.give_and_equip(Weapon("Fire Breath", 0, 60))

# Cultist enemy class
class Cultist(Character):
    def __init__(self, name):
        super().__init__(name, "Cultist", random.randrange(50, 70), max_mana=0)
        self.give_and_equip(Weapon("Cult Hex", 0, random.randrange(40, 60)))

# Cultist boss enemy class
class CultistBoss(Character):
    def __init__(self, name):
        super().__init__(name, "Cultist", 150, max_mana=0)
        self.give_and_equip(Weapon("Magic Hands", 0, 100))

# Ghost enemy class
class Ghost(Character):
    def __init__(self, name):
        super().__init__(name, "Ghost", random.randrange(30, 50), max_mana=0)
        self.give_and_equip(Weapon("Ethereal Touch", 0, random.randrange(20, 35)))

# Fight functions for different encounters, reward the player after victory

def GoblinFight():
    Player.fight([Goblin("Brzt")])
    Player.give(Weapon("Club", 1, random.randrange(5, 10)))
    Player.give(Gold(5))

def BanditFight():
    Player.fight([Human("Bob"), Human("Gary")])
    Player.give(Weapon("Level 1 Wooden Sword", 2, random.randrange(5, 10)))
    Player.give(Weapon("Level 1 Wooden Sword", 2, random.randrange(5, 10)))
    Player.give(Gold(10))
    Player.give(Healing("Lvl 1 Health Potion", 5, 10))

def BanditFight2():
    Player.fight([Human("Bob")])
    Player.give(Weapon("Level 1 Wooden Sword", 2, random.randrange(5, 10)))
    Player.give(Gold(10))
    Player.give(Healing("Lvl 1 Health Potion", 5, 10))

def SkeletonFight():
    Player.fight([Skeleton("Norman"), Skeleton("Harry"), Skeleton("George")])
    Player.give(Weapon("Level 1 Wooden Bow", 5, random.randrange(15, 25)))
    Player.give(Weapon("Level 1 Wooden Bow", 5, random.randrange(15, 25)))
    Player.give(Weapon("Level 1 Wooden Bow", 5, random.randrange(15, 25)))
    Player.give(Gold(15))

def SpiderFight():
    Player.fight([Spider("Spider"), Spider("Spider"), Spider("Spider")])
    Player.give(Healing("Lvl 1 Health Potion", 5, 10))
    Player.give(Healing("Lvl 1 Health Potion", 5, 10))
    Player.give(Gold(15))

def MysteriousStrangerFight():
    Player.fight([UnbeatableHuman("Mysterious Stranger")])
    Player.give(Weapon("Stick", 1, 0))
    Player.give(Healing("Lvl 1 Health Potion", 5, 10))

def GhostFight():
    Player.fight([Ghost("Spooky")])
    Player.give(Weapon("Ethereal Touch", 0, random.randrange(20, 35)))
    Player.give(Healing("Lvl 2 Health Potion", 15, 20))
    Player.give(Gold(20))

def SpiderAndSkeletonFight():
    Player.fight([Skeleton("George"), Spider("Mark"), Spider("Spider")])
    Player.give(Healing("Lvl 1 Health Potion", 5, 10))
    Player.give(Healing("Lvl 1 Health Potion", 5, 10))
    Player.give(Weapon("Level 1 Wooden Bow", 5, random.randrange(15, 25)))
    Player.give(Weapon("Level 1 Wooden Bow", 5, random.randrange(15, 25)))
    Player.give(Weapon("Level 1 Wooden Bow", 5, random.randrange(15, 25)))
    Player.give(Gold(30))
    Player.give(Healing("Lvl 4 Health Potion", 40, 50))
    Player.give(Healing("Lvl 4 Health Potion", 40, 50))

def GoblinRoomFight():
    Player.fight([Goblin("Klink"), Goblin("Kaaduk"), Goblin("Ebalk"), Goblin("Kaaduk")])
    Player.give(Weapon("Club", 1, random.randrange(5, 10)))
    Player.give(Weapon("Club", 1, random.randrange(5, 10)))
    Player.give(Weapon("Club", 1, random.randrange(5, 10)))
    Player.give(Gold(25))
    Player.give(Healing("Lvl 4 Health Potion", 40, 50))

def LootRoom():
    Player.give(Gold(50))
    Player.give(Weapon("Lvl 3 Metal Sword", 19, 30))
    Player.give(Healing("Lvl 3 Health Potion", 25, 30))
    Player.give(Healing("Lvl 3 Health Potion", 25, 30))

def DragonFight():
    Player.fight([Dragon("Toothless")])
    Player.give(Weapon("Lvl 2 Diamond Sword", 26, 40))
    Player.give(Healing("Lvl 3 Health Potion", 25, 30))
    Player.give(Healing("Lvl 4 Health Potion", 40, 50))
    Player.give(Healing("Lvl 3 Health Potion", 25, 30))
    Player.give(Healing("Lvl 4 Health Potion", 40, 50))
    Player.give(Gold(100))

def Cultistfight():
    Player.fight([Cultist("Perfaren"), Cultist("Tratoris"), Cultist("Ianxalim")])
    Player.give(Healing("Lvl 2 Health Potion", 15, 20))
    Player.give(Healing("Lvl 2 Health Potion", 15, 20))
    Player.give(Healing("Lvl 3 Health Potion", 25, 30))
    Player.give(Weapon("Lvl 1 Mithril Sword", 30, 50))

def CultistFinalBoss():
    Player.fight([CultistBoss("Scolrang")])
    Player.give(Armour("Metal chestplate", 15, 11, 'Torso'))
    Player.give(Armour("Metal helmet", 12, 10, 'Head'))
    Player.give(Armour("Metal leggings", 14, 10, 'Legs'))
    Player.max_health = Player.max_health + 50

# Create the main player and some NPCs
Player = Hero(HeroName)
Blacksmith_Bob = Blacksmith("Blacksmith Bob")
Merchant_Charlie = Merchant("Merchant Charlie")
Merchant_Barlie = Merchant("Merchant Barlie")
