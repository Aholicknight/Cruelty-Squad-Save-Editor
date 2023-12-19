import os
import datetime
import time
import json
import colorama
from colorama import Fore, Back, Style

colorama.init()

stocks_file_path = os.path.expandvars(r"%APPDATA%\Godot\app_userdata\Cruelty Squad\stocks.save") # Default stocks file path

def load_stocks_file():
    global stocks_file_path
    try:
        with open(stocks_file_path, "r") as file:
            stocks_data = file.read()
            return json.loads("{" + stocks_data.split("{", 1)[1])
    except FileNotFoundError: # If the save file is not found, ask the user to enter the path to the save file
        print(Fore.RED + f"File {stocks_file_path} not found." + Style.RESET_ALL)
        new_path = input("Please enter the path to the stocks.save file: ")
        try:
            with open(new_path, "r") as file:
                stocks_data = file.read()
                stocks_file_path = new_path  # Update the save file path
                return json.loads("{" + stocks_data.split("{", 1)[1])
        except FileNotFoundError:
            print(Fore.RED + f"File {stocks_file_path} not found." + Style.RESET_ALL)
            return None

def save_stocks_file(data):
    stocks_data = json.dumps(data, separators=(",", ":"))
    with open(stocks_file_path, "w") as file:
        file.write('{"' + stocks_data.split('{"', 1)[1])

def print_status():
    stocks_data = load_stocks_file()
    if stocks_data is None:
        return
    print("Cruelty Squad Stocks Editor created by Aholicknight")
    print(Fore.GREEN + f"File {stocks_file_path} loaded." + Style.RESET_ALL)
    print(f"Last modified: {datetime.datetime.fromtimestamp(os.path.getmtime(stocks_file_path)).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Last accessed: {datetime.datetime.fromtimestamp(os.path.getatime(stocks_file_path)).strftime('%Y-%m-%d %H:%M:%S')}")
    # print(f"Data: {stocks_data}")
    # Print the stock tickers
    tickers = [ticker for ticker in stocks_data.keys() if ticker not in ['fish_found', 'org_found']]
    tickers_str = ", ".join(tickers)
    print(f"Tickers: {tickers_str}")

def main():
    print_status()
    stocks_data = load_stocks_file()
    if stocks_data is None:
        return
    while True:
        print("What do you want to do?")
        print("1. Edit stock")
        print("2. Remove stocks")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            stock_name = input("Enter the stock name (Ticker): ")
            if stock_name in stocks_data:
                owned_stocks = input("Enter the number of owned stocks: ")
                stocks_data[stock_name]['owned'] = int(owned_stocks)
                save_stocks_file(stocks_data)
                print(Fore.GREEN + f"Stock {stock_name} updated." + Style.RESET_ALL)
            else:
                print(Fore.RED + f"Stock {stock_name} not found." + Style.RESET_ALL)
        elif choice == "2":
            stock_name = input("Enter the stock name (Ticker): ")
            if stock_name in stocks_data:
                stocks_data[stock_name]['owned'] = 0
                save_stocks_file(stocks_data)
                print(Fore.GREEN + f"Stock {stock_name} removed." + Style.RESET_ALL)
            else:
                print(Fore.RED + f"Stock {stock_name} not found." + Style.RESET_ALL)
        elif choice == "3":
            break
        else:
            print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
        time.sleep(1)

if __name__ == "__main__":
    main()