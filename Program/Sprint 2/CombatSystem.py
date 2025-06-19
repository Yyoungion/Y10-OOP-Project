import UserInterface as UI
import random

# Ask the player for their hero's name
HeroName = input("Enter your name: ")

def select_dialog(prompt,items):
    """
    Display a selection dialog for the user to choose an item from a list.
    """
    while(True):
        index=1
        UI.DisplayTitle(prompt)
        for item in items:
            if isinstance(item,Item):
                print(f"{index:2} - {item.name:20} {item.value:5} 🪙")
            else:
                print(f"{index:2} - {item.name:20}")
            index+=1
        try:
            item_index = int(input("Selection: "))
            item=items[item_index-1]
            print("You have selected:", item.name)
            return item
        except:
            print("Stop being an idiot!!!")
            continue

def roll_dice(prompt, sides):
    """
    Simulate rolling a dice with a given number of sides.
    """
    result = random.randrange(1,sides)
    print(f"{prompt}: {result}")
    return result

# Base class for all items
class Item(object):
    def __init__(self,name,value):
        self.name=name
        self.value=value

# Healing item class
class Healing(Item):
    def __init__(self,name,value,amount):
        super().__init__(name,value)
        self.amount=amount

# Gold item class
class Gold(Item):
    def __init__(self,value):
        super().__init__("Bag of Gold",value)
        self.value=value

# Weapon item class
class Weapon(Item):
    def __init__(self,name,value,damage):
        super().__init__(name,value)
        self.resistance=0
        self.damage=damage

# Armour item class
class Armour(Item):
    def __init__(self,name,value,resistance,location):
        super().__init__(name,value)
        self.resistance=resistance
        self.location=location

# Base class for all characters
class Character(object):
    def __init__(self,name,type,health,max_mana=0):
        # Equipped items: Head, Torso, Legs, Weapon
        self.equipped={
            'Head': Armour("Nothing",0,0,"Head"),
            'Torso': Armour("Nothing",0,0,"Torso"),
            'Legs': Armour("Nothing",0,0,"Legs"),
            'Weapon' : Weapon("Nothing",0,0)}
        self.name=name
        self.type=type
        self.health=health
        self.max_health=health
        self.inventory=[]
        self.max_mana = max_mana
        self.mana = max_mana

    def stats(self):
        """
        Display the character's stats.
        """
        UI.DisplayStats(self.name,self.type, self.health,self.max_health,self.mana,self.max_mana)

    def get_inventory(self, item_type=None):
        """
        Get the character's inventory, optionally filtered by item type.
        """
        if item_type is None:
            return self.inventory
        return [item for item in self.inventory if isinstance(item, item_type)]

    def get_inventory_armour(self):
        """
        Get all armour items in the inventory.
        """
        return self.get_inventory(Armour)
    
    def use_item(self, item_name):
        """
        Use an item from inventory by name. If it's a Healing item, apply healing.
        """
        for item in self.inventory:
            if item.name == item_name:
                if isinstance(item, Healing):
                    self.heal(item.amount)
                    print(f"{self.name} used {item.name} and healed for {item.amount} HP.")
                    self.stats()
                    self.remove(item.name)
                    return True
                else:
                    print(f"{item.name} cannot be used directly.")
                    return False
        print(f"{item_name} not found in inventory.")
        return False

    def equip(self,item):
        """
        Equip a weapon or armour, or use a healing item.
        """
        if isinstance(item,Weapon):
            self.equipped["Weapon"]=item
        elif isinstance(item,Armour):
            self.equipped[item.location]=item
        elif isinstance(item,Healing):
            self.heal(item.amount)
            self.remove(item.name)

    def unequip(self,item):
        """
        Unequip an item from the equipped slots.
        """
        for location in self.equipped.keys():
            if item==self.equipped[location]:
                if isinstance(item,Weapon):
                    self.equipped[location]=Weapon("Nothing",0,0)
                elif isinstance(item,Armour):
                    self.equipped[location]=Armour("Nothing",0,0,location)

    def get_gold(self):
        """
        Get the gold item from inventory, or create one if not present.
        """
        for destination_item in self.inventory:
            if isinstance(destination_item,Gold):
                return destination_item
        destination_item=Gold(0)
        self.inventory.append(destination_item)
        return destination_item

    def add_gold(self,source_item):
        """
        Add gold from another item to this character's gold.
        """
        gold=self.get_gold()
        gold.value+=source_item.value

    def give(self,item):
        """
        Give an item to the character (add to inventory).
        """
        if isinstance(item,Gold):
            self.add_gold(item)
        else:
            self.inventory.append(item)
        
    def remove(self,target_item_name):
        """
        Remove an item from inventory by name.
        """
        for inventory_item in self.inventory:
            if target_item_name == inventory_item.name:
                self.unequip(inventory_item)
                self.inventory.remove(inventory_item)
                return

    def give_and_equip(self,item):
        """
        Give an item and equip it immediately.
        """
        self.give(item)
        self.equip(item)

    def show_equiped(self):
        """
        Display currently equipped items.
        """
        UI.DisplayTitle("Equiped items")
        for location in self.equipped.keys():
            print(f"{location:10}:",self.equipped[location].name)

    def equip_dialog(self):
        """
        Dialog for equipping items from inventory.
        """
        while True:
            response = input("Do you want to equip an item?(Yes / No) ")
            if response == 'Yes' or response == 'yes':
                self.equip(select_dialog("Equip item",self.inventory))
                self.show_equiped()
            else:
                return

    def show_item_list(self,title,list):
        """
        Display a list of items with a title.
        """
        UI.DisplayTitle(title)
        index=1
        for item in list:
            print(f"{index:2} - {item.name:20} {item.value:5} 🪙")
            index+=1

    def get_total_resistance(self):
        """
        Calculate total resistance from equipped armour.
        """
        resistance=0
        for location in self.equipped.keys():
            resistance=resistance+self.equipped[location].resistance
        return resistance
        
    def attack(self,target):
        """
        Attack a target character, considering weapon damage and target's resistance.
        """
        sides=6
        attack_damage = int((self.equipped["Weapon"].damage*roll_dice("\tAttacking",sides))/sides)
        resistance=target.get_total_resistance()
        armoured_attack_damage=attack_damage-resistance
        if armoured_attack_damage<0:
            armoured_attack_damage=0           
        target.health-=armoured_attack_damage

    def heal(self,amount):
        """
        Heal the character by a certain amount, up to max health.
        """
        self.health = self.health + amount
        if self.health > self.max_health:
            self.health=self.max_health

    def is_dead(self):
        """
        Check if the character is dead.
        """
        if self.health<=0:
            return True
        return False

    def sell(self,target):
        """
        Sell an item to another character.
        """
        item=select_dialog(f"{self.name} selling to {target.name}",self.inventory)
        if isinstance(item,Gold):
            return
        target_gold=target.get_gold()
        self_gold=self.get_gold()
        if target_gold.value>=item.value:
            print(f"{self.name} sold the the {item.name} to {target.name} for {item.value} gold")
            target.give(item)
            self.remove(item.name)
            target_gold.value-=item.value
            self_gold.value+=item.value
        else:
            print(f"{target.name} does not have enough gold")

    def buy(self,target):
        """
        Buy an item from another character.
        """
        target.sell(self)

    def trade(self,target):
        """
        Trade items with another character.
        """
        while(True):
            self.DisplayInventory()
            target.DisplayInventory()
            UI.DisplayTitle(f"{self.name} is trading with {target.name}")
            index=1
            options=["Buy", "Sell","Stop Trading"]
            for option in options:
                print(f"{index:2} - {option:20}")
                index+=1
            try:
                option_index = int(input("Selection: "))
                option=options[option_index-1]
                print("You have selected:", option)
                if option=="Buy":
                    self.buy(target)
                elif option=="Sell":
                    self.sell(target)
                else:
                    return
            except:
                print("Stop being an idiot!!!")

    def fight(self,enemies):
        """
        Start a fight with a list of enemy characters.
        """
        UI.DisplayTitle("A fight has started")
        round=1
        while(True):
            UI.DisplayTitle(f"Round {round}")
            round+=1
            self.stats()
            #player attacks
            live_enemies=[]
            for enemy in enemies:
                if not enemy.is_dead():
                    enemy.stats()
                    live_enemies.append(enemy)

            if len(live_enemies)==0:
                print("YOU WIN!!!")
                return True
            self.equip_dialog()
            target=select_dialog("Who will you attack?",live_enemies)
            self.attack(target)
            for enemy in live_enemies:
                enemy.attack(self)
                if self.is_dead():
                    print("""
██╗░░░██╗░█████╗░██╗░░░██╗  ██████╗░██╗███████╗██████╗░
╚██╗░██╔╝██╔══██╗██║░░░██║  ██╔══██╗██║██╔════╝██╔══██╗
░╚████╔╝░██║░░██║██║░░░██║  ██║░░██║██║█████╗░░██║░░██║
░░╚██╔╝░░██║░░██║██║░░░██║  ██║░░██║██║██╔══╝░░██║░░██║
░░░██║░░░╚█████╔╝╚██████╔╝  ██████╔╝██║███████╗██████╔╝
░░░╚═╝░░░░╚════╝░░╚═════╝░  ╚═════╝░╚═╝╚══════╝╚═════╝░""")
                    exit(0)

# Hero character class
class Hero(Character):
    def __init__(self,name):
        super().__init__(name,"Human", 100, max_mana=50)
        self.give_and_equip(Weapon("Stick",0,random.randrange(5,15)))
        self.give(Gold(10))

# Goblin enemy class
class Goblin(Character):
    def __init__(self,name):
        super().__init__(name,"Goblin", random.randrange(40,50), max_mana=0)
        self.give_and_equip(Weapon("Club",1,random.randrange(5,10)))

# Human enemy class
class Human(Character):
    def __init__(self,name):
        super().__init__(name,"Human", 25, max_mana=0)
        self.give_and_equip(Weapon("Level 1 Wooden Sword",2,5))

# Merchant NPC class
class Merchant(Character):
    def __init__(self,name):
        super().__init__(name,"Merchant", random.randrange(50,55), max_mana=0)
        # Add multiple healing potions to inventory
        self.give(Healing("Lvl 1 Health Potion",5,10))
        self.give(Healing("Lvl 2 Health Potion",15,20))
        self.give(Healing("Lvl 3 Health Potion",25,30))
        self.give(Healing("Lvl 4 Health Potion",40,50))
        self.give(Healing("Lvl 5 Health Potion",70,100))
        self.give(Healing("Lvl 1 Health Potion",5,10))
        self.give(Healing("Lvl 2 Health Potion",15,20))
        self.give(Healing("Lvl 3 Health Potion",25,30))
        self.give(Healing("Lvl 4 Health Potion",40,50))
        self.give(Healing("Lvl 5 Health Potion",70,100))
        self.give(Healing("Lvl 1 Health Potion",5,10))
        self.give(Healing("Lvl 2 Health Potion",15,20))
        self.give(Healing("Lvl 3 Health Potion",25,30))
        self.give(Healing("Lvl 4 Health Potion",40,50))
        self.give(Healing("Lvl 5 Health Potion",70,100))
        self.give(Healing("Lvl 1 Health Potion",5,10))
        self.give(Healing("Lvl 2 Health Potion",15,20))
        self.give(Healing("Lvl 3 Health Potion",25,30))
        self.give(Healing("Lvl 4 Health Potion",40,50))
        self.give(Healing("Lvl 5 Health Potion",70,100))
        self.give(Gold(100))

# Blacksmith NPC class
class Blacksmith(Character):
    def __init__(self,name):
        super().__init__(name,"Blacksmith",random.randrange(50,55), max_mana=0)
        # Add various weapons and armour to inventory
        self.give(Weapon("Lvl 1 Wooden Sword",3, 5))
        self.give(Weapon("Lvl 2 Wooden Sword",6, 10))
        self.give(Weapon("Lvl 3 Wooden Sword",9, 15))

        self.give(Weapon("Lvl 1 Metal Sword",13, 20))
        self.give(Weapon("Lvl 2 Metal Sword",16, 25))
        self.give(Weapon("Lvl 3 Metal Sword",19, 30))

        self.give(Weapon("Lvl 1 Diamond Sword",23, 35))
        self.give(Weapon("Lvl 2 Diamond Sword",26, 40))
        self.give(Weapon("Lvl 3 Diamond Sword",29, 45))
        
        self.give(Armour("leather chestplate",5,2 ,'Torso'))
        self.give(Armour("leather helmet",2,1 ,'Head'))

        self.give(Armour("Metal chestplate",15,10 ,'Torso'))
        self.give(Armour("Metal helmet",12,7 ,'Head'))
        self.give(Gold(100))
        
# Skeleton enemy class
class Skeleton(Character):
    def __init__(self,name):
        super().__init__(name,"Skeleton", random.randrange(40,60), max_mana=0)
        self.give_and_equip(Weapon("Level 1 Wooden Bow",5,random.randrange(17,27)))

# Spider enemy class
class Spider(Character):
    def __init__(self,name):
        super().__init__(name,"Spider", random.randrange(40,60), max_mana=0)
        self.give_and_equip(Weapon("Fangs",0,random.randrange(15,27)))

# Dragon enemy class
class Dragon(Character):
    def __init__(self,name):
        super().__init__(name,"Dragon", 100, max_mana=0)
        self.give_and_equip(Weapon("Fire Breath",0,60))

# Mutant animal enemy class
class MutantAnimal(Character):
    def __init__(self,name):
        super().__init__(name,"MutantAnimal",random.randrange(40,60), max_mana=0)
        self.give_and_equip(Weapon("Bite",0,random.randrange(10,20)))

# Cultist enemy class
class Cultist(Character):
    def __init__(self,name):
        super().__init__(name,"Cultist",random.randrange(50,70), max_mana=0)
        self.give_and_equip(Weapon("Cult Hex",0,random.randrange(40,60)))

# Cultist boss enemy class
class CultistBoss(Character):
    def __init__(self, name):
        super().__init__(name, "Cultist", 150, max_mana=0)
        self.give_and_equip(Weapon("Magic Hands",0,100))

# Fight and loot event functions

def GoblinFight():
    """
    Fight a single goblin and receive loot.
    """
    Player.fight([Goblin("Brzt")])
    Player.give(Weapon("Club",1,random.randrange(5,10)))
    Player.give(Gold(5))

def BanditFight():
    """
    Fight two bandits and receive loot.
    """
    Player.fight([Human("Bob"),Human("Gary"),])
    Player.give(Weapon("Level 1 Wooden Sword",2,random.randrange(5,10)))
    Player.give(Weapon("Level 1 Wooden Sword",2,random.randrange(5,10)))
    Player.give(Weapon("Level 1 Wooden Sword",2,random.randrange(5,10)))
    Player.give(Gold(10))
    Player.give(Healing("Lvl 1 Health Potion",5,10))

def SkeletonFight():
    """
    Fight three skeletons and receive loot.
    """
    Player.fight([Skeleton("Norman"),Skeleton("Harry"),Skeleton("George")])
    Player.give(Weapon("Level 1 Wooden Bow",5,random.randrange(15,25)))
    Player.give(Weapon("Level 1 Wooden Bow",5,random.randrange(15,25)))
    Player.give(Weapon("Level 1 Wooden Bow",5,random.randrange(15,25)))
    Player.give(Gold(15))

def SpiderFight():
    """
    Fight three spiders and receive loot.
    """
    Player.fight([Spider("Spider"),Spider("Spider"),Spider("Spider")])
    Player.give(Healing("Lvl 1 Health Potion",5,10))
    Player.give(Healing("Lvl 1 Health Potion",5,10))
    Player.give(Gold(15))

def SpiderAndSkeletonFight():
    """
    Fight three skeletons and three spiders and receive loot.
    """
    Player.fight([Skeleton("Norman"),Skeleton("Harry"),Skeleton("George"),Spider("Spider"),Spider("Spider"),Spider("Spider")])
    Player.give(Healing("Lvl 1 Health Potion",5,10))
    Player.give(Healing("Lvl 1 Health Potion",5,10))
    Player.give(Weapon("Level 1 Wooden Bow",5,random.randrange(15,25)))
    Player.give(Weapon("Level 1 Wooden Bow",5,random.randrange(15,25)))
    Player.give(Weapon("Level 1 Wooden Bow",5,random.randrange(15,25)))
    Player.give(Gold(30))

def GoblinRoomFight():
    """
    Fight three goblins and receive loot.
    """
    Player.fight([Goblin("Klink"),Goblin("Kaaduk"),Goblin("Ebalk")])
    Player.give(Weapon("Club",1,random.randrange(5,10)))
    Player.give(Weapon("Club",1,random.randrange(5,10)))
    Player.give(Weapon("Club",1,random.randrange(5,10)))
    Player.give(Gold(25))

def LootRoom():
    """
    Receive loot from a loot room.
    """
    Player.give(Gold(50))
    Player.give(Weapon("Lvl 3 Metal Sword",19,30))

def DragonFight():
    """
    Fight a dragon and receive loot.
    """
    Player.fight([Dragon("Toothless")])
    Player.give(Weapon("Lvl 2 Diamond Sword",26,40))
    Player.give(Healing("Lvl 3 Health Potion",25,30))
    Player.give(Healing("Lvl 4 Health Potion",40,50))
    Player.give(Healing("Lvl 3 Health Potion",25,30))
    Player.give(Healing("Lvl 4 Health Potion",40,50))
    Player.give(Gold(100))

def MutantAnimalFight():
    """
    Fight five mutant animals and receive loot.
    """
    Player.fight([MutantAnimal("Mutated Animal"),MutantAnimal("Mutated Animal"),MutantAnimal("Mutated Animal"),MutantAnimal("Mutated Animal"),MutantAnimal("Mutated Animal")])
    Player.give(Gold(15))

def Cultistfight():
    """
    Fight three cultists and receive loot.
    """
    Player.fight([Cultist("Perfaren"),Cultist("Tratoris"),Cultist("Ianxalim")])
    Player.give(Healing("Lvl 2 Health Potion",15,20))
    Player.give(Healing("Lvl 2 Health Potion",15,20))
    Player.give(Healing("Lvl 3 Health Potion",25,30))
    Player.give(Weapon("Lvl 1 Mithril Sword",30, 50))

def CultistFinalBoss():
    """
    Fight the cultist boss.
    """
    Player.fight([CultistBoss("Scolrang")])

# Create main player and NPCs
Player = Hero(HeroName)
blacksmith_bob=Blacksmith("Blacksmith Bob")
Merchant_Charlie=Merchant("Merchant Charlie")
Merchant_Barlie=Merchant("Merchant Barlie")
