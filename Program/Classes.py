class Player:
    def __init__(self, name, health, attack, defense, mana, level, inventory, gold):  # Fixed typo here
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.mana = mana
        self.level = level
        self.inventory = inventory
        self.gold = gold

    def __str__(self):
        return f"Name: {self.name}, Health: {self.health}, Attack: {self.attack}, Defense: {self.defense}, Mana: {self.mana}, Level: {self.level}"

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
    
    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = health
    
    def get_attack(self):
        return self.attack

    def set_attack(self, attack):
        self.attack = attack

    def get_defense(self):
        return self.defense
    
    def set_defense(self, defense):
        self.defense = defense

    def get_mana(self):
        return self.mana
    
    def set_mana(self, mana):
        self.mana = mana
    
    def get_level(self):
        return self.level
    
    def set_level(self, level):
        self.level = level

    def get_inventory(self):
        return self.inventory
    
    def set_inventory(self, inventory):
        self.inventory = inventory
        
    def get_gold(self):
        return self.gold
    
    def set_gold(self, gold):
        self.gold = gold

class Weapon:
    def __init__(self, name, attack, cost, level_requirement):
        self.name = name
        self.attack = attack
        self.cost = cost
        self.level_requirement = level_requirement

    def __str__(self):
        return f"Name: {self.name}, Attack: {self.attack}, Cost: {self.cost}, Level Requirement: {self.level_requirement}"

class Armor:
    def __init__(self, name, defense, cost):
        self.name = name
        self.defense = defense
        self.cost = cost

    def __str__(self):
        return f"Name: {self.name}, Defense: {self.defense}, Cost: {self.cost}"

class Enemy:
    def __init__(self, race, health, attack, defense, level, loot, loot_percentage):
        self.race = race
        self.health = health
        self.attack = attack
        self.defense = defense
        self.level = level
        self.loot = loot   
        self.loot_percentage = loot_percentage
    def __str__(self):
        return f"race{self.race}, health: {self.health}, attack: {self.attack}, defense: {self.defense}, level: {self.level}, loot: {self.loot}, loot_percentage: {self.loot_percentage}"

class Potion:
    def __init__(self, type, health, mana, cost):
        self.type = type
        self.health = health
        self.mana = mana
        self.cost = cost

    def __str__(self):
        return f"Type: {self.type}, Health Regenerated: {self.health}, Mana Regenerated: {self.mana}, Cost: {self.cost}"

class Grimoire:
    def __init__(self, spell, cost):
        self.spell = spell
        self.cost = cost
    
    def __str__(self):
        return f"Spell: {self.spell}, Cost: {self.cost}"

class Spell_Attack:
    def __init__(self, name, damage, mana_cost):
        self.name = name
        self.damage = damage
        self.mana_cost = mana_cost

    def __str__(self):
        return f"Name: {self.name}, Damage: {self.damage}, Mana Cost: {self.mana_cost}"

class Cards:
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit

    def __str__(self):
        return f"Number: {self.number}, Suit: {self.suit}"
    

        