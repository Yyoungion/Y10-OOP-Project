import UserInterface as UI
import Storyline as Storyline
import CombatSystem as Combat

Combat.HeroName

def main():
    UI.DisplayTitleScreen()
    UI.DisplaySeparator()
    input("Press Enter to continue...")
    print("")
    UI.DisplayStats(Combat.HeroName, Combat.Player.type, Combat.Player.health, Combat.Player.max_health, Combat.Player.mana, Combat.Player.max_mana)
    Combat.Player.show_equiped()
    print("")
    input("Press Enter to continue...")
    Storyline.Storyline()

main()