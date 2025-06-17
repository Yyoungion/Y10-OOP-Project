import UserInterface as UI
import Storyline as Storyline
import CombatSystem as Combat

Combat.HeroName

def main():
    UI.DisplayTitleScreen()
    UI.DisplaySeparator()
    input("Press Enter to continue...")
    Storyline.Storyline()

main()