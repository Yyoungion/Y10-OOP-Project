from Classes import *
from Object_Creation import *

def test_combat():
    # Create a player and an enemy
    player = Player1 
    enemy = Goblin      

    # Display initial stats
    Player1.__str__()
    Goblin.__str__()
    while player.health > 0 and enemy.health > 0:
        # Player attacks enemy
        damage_to_enemy = player.attack / enemy.defense
        if damage_to_enemy < 0:
            damage_to_enemy = 0
        enemy.health -= damage_to_enemy
        print(f"{player.name} attacks {enemy.race} for {damage_to_enemy} damage. {enemy.race} HP: {enemy.health}")

        # Check if enemy is defeated
        if enemy.health <= 0:
            print(f"{enemy.race} is defeated!")
            break

        # Enemy attacks player
        damage_to_player = enemy.attack / player.defense
        if damage_to_player < 0:
            damage_to_player = 0
        player.health -= damage_to_player
        print(f"{enemy.race} attacks {player.name} for {damage_to_player} damage. {player.name} HP: {player.health}")

        # Check if player is defeated
        if player.health <= 0:
            print(f"{player.name} is defeated!")
            break

# Run the test

if __name__ == "__main__":
    test_combat()