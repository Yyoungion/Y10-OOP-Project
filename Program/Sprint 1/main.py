import UserInterface as UI
import Storyline as Storyline

# Player stats
player_name = "Hero"
player_type = "Warrior"
player_health = 18
player_max_health = 100
player_mana = 50
player_max_mana = 50
player_damage = 20
player_defence = 5




def main():
    UI.DisplayTitleScreen()
    UI.DisplaySeparator()
    print("=======================================")
    print("Player Stats")
    print("=======================================")
    print()
    UI.DisplayStats(player_name, player_type, player_health, player_max_health, player_mana, player_max_mana, player_damage, player_defence)
    input("Press Enter to continue...")
    Storyline.Storyline()



main()    