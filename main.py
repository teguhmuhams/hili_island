import sys
import os
import random
from time import sleep


def screen_clear():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


def input_message(message):
    print(message)
    print("Please wait...")
    sleep(3)


def typewriter(message):
    special_chars = [',', '?', '!']
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        if char == "\n":
            sleep(1.5)
        elif char in special_chars:
            sleep(0.7)
        elif char == ".":
            sleep(0.2)
        else:
            sleep(0.05)


def isSkip(section):
    skip = False
    while True:
        screen_clear()
        print("Do you want to skip the story for", section)
        try:
            want_to_skip = input("Type YES or NO: ").upper()
            if(want_to_skip == "YES"):
                skip = True
                break
            elif(want_to_skip == "NO"):
                skip = False
                break
            else:
                input_message("Wrong input. Try again!")
        except:
            input_message("Invalid input.")
    return skip


def play_story(section):
    screen_clear()
    filename = "lore.txt"
    with open(filename, "r") as text:
        for find in text:
            if section in find:
                for line in text:
                    if "*" in line:
                        break
                    else:
                        typewriter(line)


def check_winner(pw, ew):
    if(pw == "Rocks"):
        if (ew == "Rocks"):
            return "d"
        elif(ew == "Paper"):
            return "e"
        else:
            return "p"
    if(pw == "Paper"):
        if (ew == "Paper"):
            return "d"
        elif(ew == "Scissors"):
            return "e"
        else:
            return "p"
    if(pw == "Scissors"):
        if (ew == "Scissors"):
            return "d"
        elif(ew == "Rocks"):
            return "e"
        else:
            return "p"


def calc_score(attempt, level):
    if(level == 1):
        tmp = 1000 - attempt * 10
        if tmp < 0:
            # if the player's luck is so bad
            return 100
        return tmp
    elif(level == 2):
        tmp = 10000 - attempt * 100
        if tmp < 0:
            # if the player's luck is so bad
            return 1000
        return tmp
    elif(level == 3):
        tmp = 50000 - attempt * 500
        if tmp < 0:
            # if the player's luck is so bad
            return 5000
        return tmp


def battle(level, player_name):
    keep_losing = True
    length = len(player_name)
    pad = length+6 if length > 17 else 17
    while keep_losing:
        weapons = ['Rocks', 'Paper', 'Scissors']
        attempt = 1
        isOver = False
        # Base stats
        if (level == 1):
            enemy = {"HP": 100, "ATK": 15, "weapon": ""}
            player = {"HP": 100, "ATK": 30, "weapon": ""}
        elif(level == 2):
            enemy = {"HP": 300, "ATK": 30, "weapon": ""}
            player = {"HP": 100, "ATK": 100, "weapon": ""}
        elif(level == 3):
            enemy = {"HP": 5000, "ATK": 100, "weapon": ""}
            player = {"HP": 1000, "ATK": 400, "weapon": ""}
        player_base_hp = player["HP"]
        enemy_base_hp = enemy["HP"]
        # Loop until gets winner
        while not isOver:
            # Loop for input choice
            while True:
                screen_clear()
                print("===  BATTLE", level, " ===")
                print("Attempt:", attempt, "\n")
                print(player_name, "stats".ljust(pad-length-1),
                      ": HP=", player["HP"], "| ATK=", player["ATK"])
                print("Hilichurl stats".ljust(pad),
                      ": HP=", enemy["HP"], "| ATK=", enemy["ATK"])
                print("Weapons:\n1. Rocks\n2. Paper\n3. Scissors")
                try:
                    choice = int(input("Type the number of your choice: "))
                    if(not (1 <= choice <= 3)):
                        input("Invalid number. Press enter to try again!")
                    else:
                        break
                except ValueError:
                    input("Invalid input. Press enter to try again!")

            print()
            player["weapon"] = weapons[choice - 1]
            enemy["weapon"] = random.choice(weapons)
            print("You use", player["weapon"])
            print("The hilichurl use", enemy["weapon"])
            res = check_winner(player["weapon"], enemy["weapon"])
            if(res == "d"):
                print("Draw!")
            elif(res == "p"):
                print("You got him!")
                enemy["HP"] -= player["ATK"]
            elif(res == "e"):
                print("He hits you!")
                player["HP"] -= enemy["ATK"]
            attempt += 1
            sleep(3)
            # Check if HP is below 0
            if(player["HP"] <= 0):
                print("You lose the battle!")
                player["HP"] = player_base_hp
                enemy["HP"] = enemy_base_hp
                input("Please enter to try again!")
            elif(enemy["HP"] <= 0):
                print("Congrats, you win the battle!")
                keep_losing = False
                isOver = True

    score = calc_score(attempt, level)
    print("Score in this battle:", score)
    input("Press enter to continue...")
    return score


def play():
    screen_clear()
    try:
        f = open("lore.txt", "r")
    except IOError:
        print("lore.txt is not Found. The game won't run.")
        print("Please contact the developer for the missing files.")
        input("Press enter to go back...")
        main_menu()

    while True:
        total_score = 0
        screen_clear()
        name = input("Please enter your name: ")
        print()
        print("Hello " + name +
              ", Welcome to Lost in Hili Island Game. Hope you liked it!\n")
        sleep(1)
        print("Sorry if the english in this game is bad :(")
        sleep(2)
        if not isSkip("Prologue"):
            play_story("#1")
        if not isSkip("Chapter 1"):
            play_story("#2")
        total_score += battle(1, name)
        if not isSkip("Chapter 2"):
            play_story("#3")
        total_score += battle(2, name)
        if not isSkip("Chapter 3"):
            play_story("#4")
        total_score += battle(3, name)
        if not isSkip("Chapter 4"):
            play_story("#5")

        print("You've WON the game!")
        print("Total score:", total_score)
        input("Press enter to go back to the main menu")
        main_menu()


def about():
    screen_clear()
    print("Developed by M Teguh Sinulingga.\nContact: https://instagram.com/mhdteguhs")
    print("For missing files: https://github.com/teguhmuhams/hiliislandgame")
    print("Version: 1.0\n")
    print("Thanks:")
    print("-Bang Randy Heksadesianto from IMILKOM USU\n-Stackoverflow (obvious)\n-Tutorialspoint\n-GeeksforGeeks\n-Genshin Impact for hilichurl reference\n-etc\n")
    input("Press enter to continue...")


def tutorial():
    screen_clear()
    print("=== HOW TO PLAY ===\n")
    filename = "tutorials.txt"
    try:
        with open(filename, "r") as text:
            for line in text:
                print(line)
        print()
        input("Press enter to continue...")
    except:
        print("tutorials.txt is not Found.")
        print("Please contact the developer for the missing files.")
        input("Press enter to continue...")


def main_menu():
    while True:
        screen_clear()
        print("===========================")
        print("    Lost in Hili Island    ")
        print("===========================\n")
        try:
            print("1. Play")
            print("2. Tutorial")
            print("3. About n Contact")
            print("4. Exit")
            choice = int(input("Type your choice: "))
            if (1 <= choice <= 4):
                if(choice == 1):
                    play()
                elif(choice == 2):
                    tutorial()
                elif(choice == 3):
                    about()
                elif(choice == 4):
                    exit(0)
            else:
                input_message("Wrong input.")
        except ValueError:
            input_message("Invalid input.")


main_menu()
print("End of program")
