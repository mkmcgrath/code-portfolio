# Welcome to Grunk - An Improved Adventure Game

import secrets
import time

places = {
    (1, 1): "a clearing surrounded by thick forest. Paths lead in all directions.",
    (
        2,
        1,
    ): "a rocky shore. The ocean stretches endlessly to the east, waves crashing against the land.",
    (
        1,
        2,
    ): "a dense jungle filled with eerie sounds. Vines and shadows dance in the dim light.",
    (
        0,
        1,
    ): "a dark cave entrance. A chill wind flows from within, carrying whispers of the unknown.",
    (1, 0): "a grassy hilltop. The sky is vast, and Grunk can see for miles.",
}


class Person:
    def __init__(self, name, strength, luck, position_x, position_y):
        self.name = name
        self.strength = strength
        self.luck = luck
        self.position_x = position_x
        self.position_y = position_y
        self.points = 0
        self.health = 10
        self.start_time = time.time()


def mainmenu():
    print("\nWelcome to Grunk.")
    print("Options:")
    print("1. Start New Game")
    print("2. Load Game")
    print("3. Settings")
    print("4. Quit\n")
    choice = input("Make your selection: ")
    return choice


def randomizer(min, max):
    return secrets.randbelow(max - min + 1) + min


def newgame():
    print("\nWelcome to Grunk!")
    print("We will now randomly choose our attributes for Grunk\n")

    print("Generating random luck value (5-8)...")
    luck = randomizer(5, 8)
    print(f"Random luck value is {luck}\n")

    print("Generating random strength value (5-8)...")
    strength = randomizer(5, 8)
    print(f"Random strength value is {strength}\n")

    player = Person("Grunk", strength, luck, 1, 1)
    gameloop(player)


def gameloop(player):
    alive = True
    while alive and player.health > 0:
        dialog(player)
        direction = input("What will Grunk do? ")
        changelocation(direction, player)
        player.points += 1  # Survival points

        if encounter():
            alive = battle(player)

        print(f"Grunk's Health: {player.health}\n")

    print("Grunk has perished. The adventure is over.")
    print(
        f"Final Score: {player.points} points. Time survived: {int(time.time() - player.start_time)} seconds.\n"
    )


def encounter():
    return randomizer(1, 5) == 1  # 20% chance of an encounter


def battle(player):
    print("\nGrunk encounters a dangerous beast!")
    beast_number = randomizer(0, 1)
    guess = int(input("Guess a number (0 or 1): "))

    if guess == beast_number:
        print("Grunk wins the fight! He gains 10 points!\n")
        player.points += 10
        return True
    else:
        print(
            f"Grunk guessed {guess}, but the beast's number was {beast_number}. The beast strikes Grunk!\n"
        )
        player.health -= randomizer(2, 5)
        if player.health <= 0:
            return False
        return True


def dialog(player):
    print("\nGrunk looks around...")
    location = places.get(
        (player.position_x, player.position_y),
        "a strange and unfamiliar landscape. The surroundings shift eerily.",
    )
    print(f"Grunk is in {location}\n")


def changelocation(direction, player):
    if direction.lower() == "east":
        if player.position_x == 2:
            print("Water so cold, and Grunk can't swim.")
        else:
            print("Grunk goes east.")
            player.position_x += 1
    elif direction.lower() == "west":
        if player.position_x == 0:
            print("Water so cold, and Grunk can't swim.")
        else:
            print("Grunk goes west.")
            player.position_x -= 1
    elif direction.lower() == "south":
        print("Grunk goes south.")
        player.position_y += 1
    elif direction.lower() == "north":
        print("Grunk goes north.")
        player.position_y -= 1


def main():
    choice = mainmenu()
    if choice == "1":
        newgame()
    elif choice == "2":
        print("Load game not implemented yet.")
    elif choice == "3":
        print("Settings not implemented yet.")
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid choice.")
        main()


if __name__ == "__main__":
    main()

