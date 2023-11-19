import os
import json
import colorama
from colorama import Fore, Back, Style

colorama.init()

save_file_path = os.path.expandvars(r"%APPDATA%\Godot\app_userdata\Cruelty Squad\savegame.save") # Default save file path

def load_save_file():
    global save_file_path
    try:
        with open(save_file_path, "r") as file:
            save_data = file.read()
            return json.loads("{" + save_data.split("{", 1)[1])
    except FileNotFoundError: # If the save file is not found, ask the user to enter the path to the save file
        print(Fore.RED + f"File {save_file_path} not found." + Style.RESET_ALL)
        new_path = input("Please enter the path to the savegame.save file: ")
        try:
            with open(new_path, "r") as file:
                save_data = file.read()
                save_file_path = new_path  # Update the save file path
                return json.loads("{" + save_data.split("{", 1)[1])
        except FileNotFoundError:
            print(Fore.RED + f"File {save_file_path} not found." + Style.RESET_ALL)
            return None

def save_save_file(data):
    save_data = json.dumps(data, separators=(",", ":"))
    with open(save_file_path, "w") as file:
        file.write('{"' + save_data.split('{"', 1)[1])

def print_status(save_data):
    levels_unlocked = save_data["levels_unlocked"]
    weapons_unlocked = sum(save_data["weapons_unlocked"])
    money = save_data["money"]

    difficulty_mapping = {
        "soul": "Divine Light",
        "hell_discovered": "Flesh Automation",
        "husk": "Power In Misery",
        "hope": "Hope Eradicated"
    }

    current_difficulty = "Unknown"  # If no difficulty is found, set it to unknown (should never happen)

    for key, value in difficulty_mapping.items():
        if save_data.get(key):
            current_difficulty = value
            break
    
    life_death_symbol = "LIFE" if not save_data.get("death") else "DEATH"
    symbol_color = Fore.GREEN if life_death_symbol == "LIFE" else Fore.RED

    print("Cruelty Squad Save Editor")
    print("Current Levels Unlocked:", Fore.RED + str(levels_unlocked) + Style.RESET_ALL)
    print("Number of Weapons Unlocked:", Fore.RED + str(weapons_unlocked) + Style.RESET_ALL)
    print("Current Money:", Fore.GREEN + str(money) + Style.RESET_ALL)
    print("Current Difficulty:", Fore.RED + str(current_difficulty) + Style.RESET_ALL)
    print("Current Life/Death Symbol:", symbol_color + str(life_death_symbol) + Style.RESET_ALL)

def clear_console():
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)

def main():
    save_data = load_save_file()
    if save_data is None:
        return
    
    levels_unlocked = save_data["levels_unlocked"]
    weapons_unlocked = sum(save_data["weapons_unlocked"])
    money = save_data["money"]

    difficulty_mapping = {
        "soul": "Divine Light",
        "hell_discovered": "Flesh Automation",
        "husk": "Power In Misery",
        "hope": "Hope Eradicated"
    }

    for key, value in difficulty_mapping.items():
        if save_data.get(key):
            current_difficulty = value
            break

    print_status(save_data)
    
    
    while True:
        
        print("\nOptions:")
        print("1) Edit levels unlocked")
        print("2) Unlock all weapons")
        print("3) Edit Money")
        print("4) Edit Difficulty")
        print("5) Change Life/Death Symbol")
        print("6) Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            new_levels_unlocked = int(input("Enter new levels unlocked (1-19): "))
            if 1 <= new_levels_unlocked <= 19:
                save_data["levels_unlocked"] = new_levels_unlocked
                save_save_file(save_data)
                print("Levels unlocked updated.")
                clear_console()
                print_status(save_data)
            else:
                print("Invalid input.")
        
        elif choice == "2":
            save_data["weapons_unlocked"] = [True] * len(save_data["weapons_unlocked"])
            save_save_file(save_data)
            print("All weapons unlocked.")
            clear_console()
            print_status(save_data)
        
        elif choice == "3":
            new_money = int(input("Enter new money amount: "))
            save_data["money"] = new_money
            save_save_file(save_data)
            print("Money updated.")
            clear_console()
            print_status(save_data)
        
        elif choice == "4":
            print("\nDifficulties:")
            print("1) Divine Light " + Fore.GREEN + "(default)" + Style.RESET_ALL)
            print("2) Flesh Automation " + Fore.YELLOW + "(second easiest difficulty)" + Style.RESET_ALL)
            print("3) Power In Misery " + Fore.GREEN + "(easiest difficulty)" + Style.RESET_ALL)
            print("4) Hope Eradicated " + Fore.RED + "(secret hardest difficulty)" + Style.RESET_ALL)
            print("5) Go back to main menu")

            difficulty_choice = input("Enter your choice: ")

            difficulties = ["soul", "hell_discovered", "husk", "hope"]

            if 1 <= int(difficulty_choice) <= 4:
                for difficulty in difficulties:
                    save_data[difficulty] = False

                save_data[difficulties[int(difficulty_choice) - 1]] = True
                save_save_file(save_data)
                print("Difficulty updated.")
                clear_console()
                print_status(save_data)
            else:
                clear_console()
                print_status(save_data)

        elif choice == "5":
            print("\nLife/Death Symbols:")
            print("1) LIFE " + Fore.GREEN + "(default)" + Style.RESET_ALL)
            print("2) DEATH " + Fore.RED + "(secret)" + Style.RESET_ALL)
            print("3) Go back to main menu")

            symbol_choice = input("Enter your choice: ")

            if 1 <= int(symbol_choice) <= 2:
                save_data["death"] = True if int(symbol_choice) == 2 else False
                save_save_file(save_data)
                print("Life/Death Symbol updated.")
                clear_console()
                print_status(save_data)
            else:
                clear_console()
                print_status(save_data)
        
        elif choice == "6":
            break
        
        else:
            print("Invalid choice. Please enter a valid option.")
    
    save_save_file(save_data)
    print("Changes saved.")

if __name__ == "__main__":
    main()
