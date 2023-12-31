import os
import datetime
import time
import json
import colorama
from colorama import Fore, Back, Style

colorama.init()

save_file_path = os.path.expandvars(r"%APPDATA%\Godot\app_userdata\Cruelty Squad\savegame.save") # Default save file path
stocks_file_path = os.path.expandvars(r"%APPDATA%\Godot\app_userdata\Cruelty Squad\stocks.save") # Default stocks file path

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

def load_stocks_file():
    global stocks_file_path
    try:
        with open(stocks_file_path, "r") as file:
            stocks_data = json.load(file)
            # Remove spaces from keys
            stocks_data = {key.strip(): value for key, value in stocks_data.items()}
            return stocks_data
    except FileNotFoundError: # If the save file is not found, ask the user to enter the path to the save file
        print(Fore.RED + f"File {stocks_file_path} not found." + Style.RESET_ALL)
        new_path = input("Please enter the path to the stocks.save file: ")
        try:
            with open(new_path, "r") as file:
                stocks_data = json.load(file)
                # Remove spaces from keys
                stocks_data = {key.strip(): value for key, value in stocks_data.items()}
                stocks_file_path = new_path  # Update the save file path
                return stocks_data
        except FileNotFoundError:
            print(Fore.RED + f"File {stocks_file_path} not found." + Style.RESET_ALL)
            return None

def save_save_file(data):
    save_data = json.dumps(data, separators=(",", ":"))
    with open(save_file_path, "w") as file:
        file.write('{"' + save_data.split('{"', 1)[1])

def save_stocks_file(data):
    stocks_data = json.dumps(data, separators=(",", ":"))
    with open(stocks_file_path, "w") as file:
        file.write('{"' + stocks_data.split('{"', 1)[1])

def print_status(save_data):
    levels_unlocked = save_data["levels_unlocked"]
    weapons_unlocked = sum(save_data["weapons_unlocked"])
    money = save_data["money"]
    implants_unlocked = save_data["implants_unlocked"]

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
    stocks_data = load_stocks_file()

    print("Cruelty Squad Save Editor created by Aholicknight")
    print("Current Levels Unlocked:", Fore.RED + str(levels_unlocked) + Style.RESET_ALL)
    print("Number of Weapons Unlocked:", Fore.RED + str(weapons_unlocked) + Style.RESET_ALL)
    print("Current Money:", Fore.GREEN + str(money) + Style.RESET_ALL)
    if stocks_data is not None:
            owned_stocks_str = ", ".join([f"{ticker.strip()} ({Fore.GREEN}{stocks_data[ticker]['owned']}{Style.RESET_ALL})" for ticker in stocks_data if isinstance(stocks_data[ticker], dict) and 'owned' in stocks_data[ticker] and stocks_data[ticker]['owned'] > 0])
            print(f"Current Stocks Owned: {owned_stocks_str}")
    print("Current Implants Unlocked:", Fore.RED + str(len(implants_unlocked)) + Style.RESET_ALL)
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
        print("6) Load/Backup Current Save File")
        print("7) " + Fore.GREEN + "Unlock" + Style.RESET_ALL + " all implants")
        print("8) " + Fore.RED + "Lock" + Style.RESET_ALL + " all implants")
        print("9) Edit Stocks")
        print("10) Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1": # unlock all levels
            new_levels_unlocked = int(input("Enter new levels unlocked (1-19): "))
            if 1 <= new_levels_unlocked <= 19:
                save_data["levels_unlocked"] = new_levels_unlocked
                save_save_file(save_data)
                print("Levels unlocked updated.")
                clear_console()
                print_status(save_data)
            else:
                print("Invalid input.")
        
        elif choice == "2": # unlock all weapons
            save_data["weapons_unlocked"] = [True] * len(save_data["weapons_unlocked"])
            save_save_file(save_data)
            print("All weapons unlocked.")
            clear_console()
            print_status(save_data)
        
        elif choice == "3": # edit money
            new_money = float(input("Enter new money amount: "))
            save_data["money"] = new_money
            save_save_file(save_data)
            print("Money updated.")
            clear_console()
            print_status(save_data)
        
        elif choice == "4": # edit difficulty
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

        elif choice == "5": # change life/death symbol
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
        
        elif choice == "6": # create and load save file backup
            backup_file_path = save_file_path.replace('.save', '.bak')

            if os.path.exists(backup_file_path):
                creation_time = os.path.getctime(backup_file_path)
                creation_date = datetime.datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %I:%M:%S %p")
                print(Fore.YELLOW + f"Backup file created on {creation_date}" + Style.RESET_ALL)

            print("\nSave File Operations:")
            print(Fore.GREEN + "1) Backup current save file" + Style.RESET_ALL)
            print(Fore.RED + "2) Load from backup" + Style.RESET_ALL)
            print("3) Go back to main menu")

            operation_choice = input("Enter your choice: ")

            if operation_choice == "1":
                if os.path.exists(backup_file_path): # delete existing backup file if it exists
                    os.remove(backup_file_path)
                with open(save_file_path, 'r') as original: data = original.read()
                with open(backup_file_path, 'w') as backup: backup.write(data)
                print("Backup created.")
            elif operation_choice == "2":
                with open(backup_file_path, 'r') as backup: data = backup.read()
                with open(save_file_path, 'w') as original: original.write(data)
                print("Backup loaded. Going back to main menu...")
                time.sleep(2) # wait 2 seconds before going back to main menu to print stats
                clear_console()
                print_status(save_data)
            else:
                clear_console()
                print_status(save_data)

        elif choice == "7": # unlock all implants
            all_implants = [
                "Nightmare Vision Goggles", "First Aid Kit", "Zoom N Go Bionic Eyes", 
                "Zomy X-200 Portable Cassette Player", "Vertical Entry Device", 
                "CSIJ Level IV Body Armor", "CSIJ Level III Body Armor", 
                "Speed Enhancer Gland", "CSIJ Level II Body Armor", "Life Sensor", 
                "Grappendix", "Speed Enhancer Total Organ Package", "Biothruster", 
                "Load Bearing Vest", "Tactical Blast Shield", "Composite Helmet", 
                "Icaros Machine", "Flechette Grenade", "Night Vision Goggles", 
                "Stealth Suit", "Cursed Torch", "HE Grenade", "Cortical Scaledown+", 
                "Hazmat Suit", "Tattered Rain Hat", "Holy Scope", "Abominator", 
                "Eyes of Corporate Insight", "Military Camouflage", "Extravagant Suit", 
                "ZZzzz Special Sedative Grenade", "Augmented arms", "Pneumatic Legs", 
                "Alien Leg Wetware", "Ammunition Gland", "Angular Advantage Tactical Munitions", 
                "Skullgun", "House", "CSIJ Level VI Golem Exosystem", "Goo Overdrive", 
                "Gunkboosters", "CSIJ Level V Biosuit", "CSIJ Level IIB Body Armor", 
                "Funkgrunters", "Microbial Oil Secretion Glands", "Biojet", 
                "Speed Enhancer Node Cluster", "Bouncy Suit", "Flowerchute"
            ]

            save_data["implants_unlocked"] = all_implants
            print("Are you sure you want to unlock all implants? (" + Fore.GREEN + "y" + Style.RESET_ALL + "/" + Fore.RED + "n" + Style.RESET_ALL + ")")
            choice = input("Enter your choice: ")
            if choice.lower() == "y":
                save_save_file(save_data)
                print(Fore.GREEN + "All implants unlocked." + Style.RESET_ALL)
                time.sleep(2)
                clear_console()
                print_status(save_data)
            else:
                print(Fore.RED + "No changes made." + Style.RESET_ALL)
                print("Going back to main menu...")
                time.sleep(2)
                clear_console()
                print_status(save_data)

        elif choice == "8": # reset/lock all implants
            save_data["implants_unlocked"] = []
            print("Are you sure you want to lock all implants? (" + Fore.GREEN + "y" + Style.RESET_ALL + "/" + Fore.RED + "n" + Style.RESET_ALL + ")")
            choice = input("Enter your choice: ")
            if choice.lower() == "y":
                save_save_file(save_data)
                print(Fore.GREEN + "All implants locked." + Style.RESET_ALL)
                time.sleep(2)
                clear_console()
                print_status(save_data)
            else:
                print(Fore.RED + "No changes made." + Style.RESET_ALL)
                print("Going back to main menu...")
                time.sleep(2)
                clear_console()
                print_status(save_data)

        elif choice == "9": # edit stocks
            stocks_data = load_stocks_file()
            print(Fore.GREEN + f"File {stocks_file_path} loaded." + Style.RESET_ALL)
            print(f"Last modified: {datetime.datetime.fromtimestamp(os.path.getmtime(stocks_file_path)).strftime('%Y-%m-%d %I:%M:%S %p')}")
            print(f"Last accessed: {datetime.datetime.fromtimestamp(os.path.getatime(stocks_file_path)).strftime('%Y-%m-%d %I:%M:%S %p')}")
            # print(f"Data: {stocks_data}")
            # Print the stock tickers
            tickers = [ticker.strip() for ticker in stocks_data.keys() if ticker not in ['fish_found', 'org_found']]
            tickers_str = ", ".join(tickers)
            print(f"Tickers: {tickers_str}")
            # Print the stocks owned
            owned_stocks_str = ", ".join([f"{ticker.strip()} ({Fore.GREEN}{stocks_data[ticker]['owned']}{Style.RESET_ALL})" for ticker in stocks_data if isinstance(stocks_data[ticker], dict) and 'owned' in stocks_data[ticker] and stocks_data[ticker]['owned'] > 0])
            print(f"Bought stocks: {owned_stocks_str}")
            stocks_data = load_stocks_file()
            if stocks_data is None:
                return
            while True:
                print("What do you want to do?")
                print("1. Edit stock")
                print("2. Remove stocks")
                print("3. Go back to main menu")
                choice = input("Enter your choice: ")
                if choice == "1":
                    stock_name = input("Enter the stock name (Ticker): ").strip()  # remove leading and trailing spaces
                    if stock_name in stocks_data:
                        owned_stocks = input("Enter the number of owned stocks: ")
                        stocks_data[stock_name]['owned'] = int(owned_stocks)
                        save_stocks_file(stocks_data)
                        print(Fore.GREEN + f"Stock {stock_name} updated." + Style.RESET_ALL)
                    else:
                        print(Fore.RED + f"Stock {stock_name} not found." + Style.RESET_ALL)
                elif choice == "2":
                    stock_name = input("Enter the stock name (Ticker): ").strip()  # remove leading and trailing spaces
                    if stock_name in stocks_data:
                        stocks_data[stock_name]['owned'] = 0
                        save_stocks_file(stocks_data)
                        print(Fore.GREEN + f"Stock {stock_name} removed." + Style.RESET_ALL)
                    else:
                        print(Fore.RED + f"Stock {stock_name} not found." + Style.RESET_ALL)
                elif choice == "3":
                    clear_console()
                    print_status(save_data)
                    break # go back to main menu
                else:
                    print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
                time.sleep(1)

        elif choice == "10": # exit
            break
        
        else: # if a number is invalid exit the save editor
            print("Invalid choice. Please enter a valid option.")
    
    save_save_file(save_data)
    print("Changes saved.")

if __name__ == "__main__":
    main()
