import UserInterface as UI

# Main function to start the storyline
def Storyline():
    # Display the initial scene and present choices to the player
    UI.DisplayScene(
        "The Village of Eldoria", 
        """You wake up to find your home burning in the sunlight and a loud roar in the distance. 
You run outside to see your whole village ravaged by fire and a large winged beast flying away. 
You try to find your family but your efforts are worthless as you find out from the town mayor. 
Your Mother and Sister were trapped under a burning pile of wood and were burnt. 
You ask the mayor about your father and the mayor lowers his head. 
In a weak voice he says your father couldn't deal with the news of your mother and sister and has run away leaving you and the rest of the town. 
More Buildings collapse as you stand there sobbing but action for your survival must be done. 
Rocks are falling around you.""", 
        {
            "Run to the forest": Run_to_Forest,
            "Climb a tree": Climb_Tree,
            "Hide in a cave": Hide_Cave
        }
    )

# Function for the "Run to the forest" choice
def Run_to_Forest():
    UI.DisplayScene(
        "The Forest", 
        """You run into the forest and find a small cave.
You hide in the cave and wait for the danger to pass.
After a while, you hear the sound of footsteps approaching.
You hold your breath and try to stay quiet.
Suddenly, a group of bandits enters the cave.
They look around and spot you hiding in the corner.
They draw their weapons and approach you.""", 
        exit  # Calls the exit function when this scene ends
    )

# Function for the "Climb a tree" choice
def Climb_Tree():
    UI.DisplayScene(
        "The Tree", 
        """You climb up the tree and find a branch to sit on.
You look around and see the village burning below you.
You see the dragon flying away in the distance.
You take a deep breath and try to calm down.
Suddenly, you hear a loud crack.
The branch you are sitting on is breaking!""", 
        exit  # Calls the exit function when this scene ends
    )

# Function for the "Hide in a cave" choice
def Hide_Cave():
    UI.DisplayScene(
        "The Cave", 
        """You hide in the cave and wait for the danger to pass.
You hear the sound of footsteps approaching.
You hold your breath and try to stay quiet.
Suddenly, a group of bandits enters the cave.
They look around and spot you hiding in the corner.
They draw their weapons and approach you.
You have to think fast!""", 
        # No next function specified, scene ends here
    )

# Function to end the game
def exit():
    print("Game Over. You have been defeated.")
    exit(0)
