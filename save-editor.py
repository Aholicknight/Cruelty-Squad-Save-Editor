import os
import json

save_file_path = os.path.expandvars(r"%APPDATA%\Godot\app_userdata\Cruelty Squad\savegame.save")

def load_save_file():
    try:
        with open(save_file_path, "r") as file:
            save_data = file.read()
            return json.loads("{" + save_data.split("{", 1)[1])
    except FileNotFoundError:
        print(f"File {save_file_path} not found.")
        new_path = input("Please enter the path to the savegame.save file: ")
        try:
            with open(new_path, "r") as file:
                save_data = file.read()
                return json.loads("{" + save_data.split("{", 1)[1])
        except FileNotFoundError:
            print(f"File {new_path} not found.")
            return None

def save_save_file(data):
    save_data = json.dumps(data, separators=(",", ":"))
    with open(save_file_path, "w") as file:
        file.write('{"' + save_data.split('{"', 1)[1])

def main():
    save_data = load_save_file()
    if save_data is None:
        return
    
    levels_unlocked = save_data["levels_unlocked"]
    weapons_unlocked = sum(save_data["weapons_unlocked"])
    money = save_data["money"]

    print("Cruelty Squad Save Editor")
    print("Current Levels Unlocked:", levels_unlocked)
    print("Number of Weapons Unlocked:", weapons_unlocked)
    print("Current Money:", money)
    
    while True:
        print("\nOptions:")
        print("1) Edit levels unlocked")
        print("2) Unlock all weapons")
        print("3) Edit money")
        print("4) Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            new_levels_unlocked = int(input("Enter new levels unlocked (1-19): "))
            if 1 <= new_levels_unlocked <= 19:
                save_data["levels_unlocked"] = new_levels_unlocked
                save_save_file(save_data)
                print("Levels unlocked updated.")
            else:
                print("Invalid input.")
        
        elif choice == "2":
            save_data["weapons_unlocked"] = [True] * len(save_data["weapons_unlocked"])
            save_save_file(save_data)
            print("All weapons unlocked.")
        
        elif choice == "3":
            new_money = int(input("Enter new money amount: "))
            save_data["money"] = new_money
            save_save_file(save_data)
            print("Money updated.")
        
        elif choice == "4":
            break
        
        else:
            print("Invalid choice. Please enter a valid option.")
    
    save_save_file(save_data)
    print("Changes saved.")

if __name__ == "__main__":
    main()
