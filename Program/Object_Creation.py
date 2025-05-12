from Classes import *

#Player Creation
Player1 = Player("Jimmy", 100, 20, 10, 50, 1, [], 100)

#Weapon Creation
Fragile_Stick = Weapon("Fragile Stick", 1, 0, 0)
Club = Weapon("Club", 5, 10, 0)
Dull_Sword = Weapon("Dull Sword", 10, 20, 0)
Short_Sword = Weapon("Short Sword", 15, 30, 1)
Sword = Weapon("Sword", 20, 50, 3)
Lance = Weapon("Lance", 30, 70, 3)
Spear = Weapon("Spear", 35, 80, 5)
Enchanted_Sword = Weapon("Enchanted Sword", 45, 100, 7)
Enchanted_Lance = Weapon("Enchanted Lance", 60, 120, 7)
Enchanted_Spear = Weapon("Enchanted Spear", 75, 150, 10)
The_Big_Daddy = Weapon("The Big Daddy", 10000000000, 0, 0)

#Armor Creation
Leather_Armor = Armor("Leather Armor", 5, 10)
Chainmail_Armor = Armor("Chainmail Armor", 15, 20)
Iron_Armor = Armor("Iron Armor", 25, 30)
Gold_Armor = Armor("Gold Armor", 30, 50)
Enchanted_Chainmail_Armor = Armor("Enchanted Chainmail Armor", 50, 70)
Enchanted_Iron_Armor = Armor("Enchanted Iron Armor", 70, 90)
Enchanted_Gold_Armor = Armor("Enchanted Gold Armor", 100, 110)
Pillow = Armor("Pillow", 10000000000, 0)

#Potion Creation
Health_Potion = Potion("Health Potion", 20, 0, 10)
Mana_Potion = Potion("Mana Potion", 0, 20, 10)

#Enemy Creation
Goblin = Enemy("Goblin", 20, 5, 2, 1, [Fragile_Stick, Dull_Sword, Health_Potion], 20)
Bandit = Enemy("Bandit", 30, 10, 5, 2, Short_Sword, 100)
Skeleton = Enemy("Skeleton", 40, 15, 10, 3, Health_Potion, 150)
Bandit_Leader = Enemy("Bandit Leader", 50, 20, 15, 4, Sword, 200)
Orc = Enemy("Orc", 60, 25, 20, 5, Club, 250)


#Grimoire Creation
Fireball = Grimoire("Fireball", 20)
Lightning = Grimoire("Lightning", 30)
Ice_Shard = Grimoire("Ice Shard", 40)



#Spell Creation
Fireball_Spell = Spell_Attack("Fireball", 50, 20)
Lightning_Spell = Spell_Attack("Lightning", 70, 30)
Ice_Shard_Spell = Spell_Attack("Ice Shard", 90, 40)


#shop creation
