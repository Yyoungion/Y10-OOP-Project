import pyfiglet

def DisplayTitleScreen():
    print(pyfiglet.figlet_format("Beyond the Horizon"))

def DisplaySeparator():
    print("+"+"-"*78+"+")

def DisplayTitle(title):
    DisplaySeparator()
    print(f"| {title:76} |")
    DisplaySeparator()

def DisplaySubTitle(title):
    print(f"| {title:76} |")
    DisplaySeparator()

def SelectAction(actions):
    while(True):
        DisplaySeparator()
        index=1
        options=list(actions.keys())
        for option in options:
            print(index,"-",option)
            index+=1
        try:
            option_index = int(input("Selection: "))
            print("You have selected:#", option_index)
            DisplaySeparator()
            action=options[option_index-1]
            print("You have selected:", action)
            actions[action]()
            return
        except:

            exit()

def DisplayDialog(title, description):
    DisplayTitle(title)
    print(description)

def DisplayScene(title, story, actions):
    DisplayDialog(title, story)
    selection=SelectAction(actions)

def DisplaySceneWithEvent(title, pre_description, event, post_description, actions):
    DisplayDialog(title,pre_description)
    event()
    DisplayDialog(title,post_description)
    selection=SelectAction(actions)

def DisplayStats(name, type, health, max_health, mana, max_mana, damage, defence):
    print(f"| Name: {name} |")
    print(f"| Type: {type} |")
    bar_count=int(health*10/max_health)
    bars="█"*bar_count
    dashes="█"*(10-bar_count)
    print(f"| Health❤️ : [\033[31m{bars}█\033[0m{dashes}]({health}/{max_health})|")
    bar_count=int(mana*10/max_mana)
    bars="█"*bar_count
    dashes="█"*(10-bar_count)
    print(f"| Mana✨ : [\033[94m{bars}█\033[0m{dashes}]({mana}/{max_mana})|")
    print(f"| Damage🗡️ : {damage} |")
    print(f"| Defence🛡️ : {defence} |")
    print("=======================================")

def DisplayInventory(inventory):
    print("=======================================")
    print("Inventory")
    print("=======================================")
    for item in inventory:
        print(f"| {item} |")
    print("=======================================")

def DisplayGameOver():
    print("=======================================")
    print("Game Over")
    print("=======================================")
    print("You have died. Please restart the game.")
    print("=======================================")
    print("Thank you for playing Beyond the Horizon!")
    print("=======================================")



