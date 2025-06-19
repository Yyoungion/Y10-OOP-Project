import UserInterface as UI
import Storyline as Storyline
import CombatSystem as Combat

# Access the HeroName attribute from the Combat module
Combat.HeroName

def main():
    # Display the title screen
    UI.DisplayTitleScreen()
    # Display a separator line
    UI.DisplaySeparator()
    # Wait for user input to continue
    input("Press Enter to continue...")
    print("")
    # Display player stats
    UI.DisplayStats(
        Combat.HeroName,
        Combat.Player.type,
        Combat.Player.health,
        Combat.Player.max_health,
        Combat.Player.mana,
        Combat.Player.max_mana
    )
    # Show equipped items for the player
    Combat.Player.show_equiped()
    print("")
    # Wait for user input to continue
    input("Press Enter to continue...")

    Storyline.Storyline()

# Run main
main()