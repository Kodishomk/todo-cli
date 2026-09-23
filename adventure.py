"""
Text Adventure Game: The Forgotten Observatory
---------------------------------------------
A branching text adventure demonstrating function-to-function state transitions,
inventory tracking, and menu re-prompting.
"""

import sys


def start_game() -> None:
    """Initializes player state and launches the starting scene."""
    inventory: set[str] = set()
    print("\n==========================================")
    print("   WELCOME TO THE FORGOTTEN OBSERVATORY   ")
    print("==========================================")
    print("You stand before the rusted gates of an abandoned stone estate.")
    scene_courtyard(inventory)


def scene_courtyard(inventory: set[str]) -> None:
    """Scene 1: Starting point. Branching into Hallway or Searching."""
    print("\n--- ACT I: THE COURTYARD ---")
    print("Rain drips from the crumbling statues. The heavy wooden main door")
    print("is slightly ajar. To your right, overgrown rose bushes hide something.")

    print("\nWhat will you do?")
    print("1. Enter through the main door")
    print("2. Search the rose bushes")

    while True:
        choice = input("\nChoose (1 or 2): ").strip()
        if choice == "1":
            scene_dark_hallway(inventory)
            break
        elif choice == "2":
            if "brass_key" not in inventory:
                print("\nYou search the thick rose bushes and find a heavy BRASS KEY!")
                inventory.add("brass_key")
            else:
                print("\nYou check the bushes again, but there's nothing left to find.")
            
            # Offer immediate transition to door
            print("\nWith nowhere else to go in the courtyard, you head inside.")
            scene_dark_hallway(inventory)
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


def scene_dark_hallway(inventory: set[str]) -> None:
    """Scene 2: Central hub. Branching into Locked Door or Observatory Stairs."""
    print("\n--- ACT II: THE DARK HALLWAY ---")
    print("The air is cold and smells of wet parchment. Cobwebs hang like curtains.")
    print("Straight ahead is a reinforced oak door with a large keyhole.")
    print("To your left, a narrow spiral staircase leads upward into the mist.")

    print("\nWhat will you do?")
    print("1. Try the reinforced door")
    print("2. Climb the spiral staircase")

    while True:
        choice = input("\nChoose (1 or 2): ").strip()
        if choice == "1":
            scene_reinforced_door(inventory)
            break
        elif choice == "2":
            scene_tower_observatory(inventory)
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


def scene_reinforced_door(inventory: set[str]) -> None:
    """Scene 3A: Checkpoint using item state."""
    print("\n--- THE REINFORCED DOOR ---")
    print("You approach the door and inspect the iron lock mechanism.")

    if "brass_key" in inventory:
        print("You insert the BRASS KEY you found in the bushes. It clicks loudly!")
        print("The door swings open to reveal a hidden tunnel leading out to safety.")
        ending_escape()
    else:
        print("The door is firmly locked. As you rattle the handle, the floor gives way!")
        print("You tumble down into a dark dungeon cell.")
        ending_caught()


def scene_tower_observatory(inventory: set[str]) -> None:
    """Scene 3B: Deepest branch before multiple endings."""
    print("\n--- ACT III: THE TOWER OBSERVATORY ---")
    print("You emerge at the top of the tower under a shattered glass dome.")
    print("A massive brass telescope points toward a glowing cosmic tear in the sky.")
    print("An arched window frame looks out over the misty cliffside below.")

    print("\nWhat will you do?")
    print("1. Climb out the arched window to descend the ivy")
    print("2. Peer into the eyepiece of the brass telescope")

    while True:
        choice = input("\nChoose (1 or 2): ").strip()
        if choice == "1":
            ending_fall()
            break
        elif choice == "2":
            ending_star_rift()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


# --- ENDINGS & REPLAY LOOP ---

def ending_escape() -> None:
    """Ending A: Victory via key item."""
    print("\n==========================================")
    print("   ENDING A: THE SECRET ESCAPE (VICTORY)  ")
    print("==========================================")
    print("You run down the moonlit secret tunnel and emerge safely on the valley road!")
    prompt_replay()


def ending_caught() -> None:
    """Ending B: Defeat via missing key item."""
    print("\n==========================================")
    print("   ENDING B: TRAPPED IN THE CELL (DEFEAT) ")
    print("==========================================")
    print("The cell door locks behind you. You are trapped in the estate forever.")
    prompt_replay()


def ending_fall() -> None:
    """Ending C: Misfortune via bad choice."""
    print("\n==========================================")
    print("   ENDING C: THE TREACHEROUS DESCENT      ")
    print("==========================================")
    print("The old ivy snaps under your weight! You fall into the rocky waters below.")
    prompt_replay()


def ending_star_rift() -> None:
    """Ending D: Strange Sci-Fi Ending."""
    print("\n==========================================")
    print("   ENDING D: ABSORBED BY THE VOID        ")
    print("==========================================")
    print("As you peer through the telescope, a strange beam pulls your consciousness")
    print("into the rift. You now wander the cosmos as a cosmic observer.")
    prompt_replay()


def prompt_replay() -> None:
    """Asks player if they want to play again or exit cleanly."""
    while True:
        choice = input("\nPlay again? (y/n): ").strip().lower()
        if choice == "y":
            start_game()
            break
        elif choice == "n":
            print("\nThanks for playing! Goodbye.")
            sys.exit(0)
        else:
            print("Please enter 'y' for Yes or 'n' for No.")


if __name__ == "__main__":
    start_game()