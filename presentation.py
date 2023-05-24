""" A module for the presentation layer """

import os
from commands import Command


class Option:
    def __init__(self, name:str, command:Command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call # for commands that needs data input
    
    def choose(self): 
        # a method through which we choose the command
        data = self.prep_call() if self.prep_call else None
        result = self.command.execute(data) if data else self.command.execute()
        if isinstance(result, list):
            for line in result:
                print(line)
        else:
            print(result)

    def __str__(self):
        return self.name


def print_options(options: dict):
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
    print()


def option_choice_is_valid(choice: str, options: dict) -> bool:
    result = choice in options or choice.upper() in options
    return result


def get_option_choice(options: dict):
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice")
        choice = input("Choose an option: ")
    return options[choice.upper()]


def get_user_input(label:str):
    value = input(f"{label}: ") or None
    while not value:
        #if value was not read (enter), enter a value 
        value = input(f"{label}: ") or None
    return value


def get_new_expense_data():
    result = {
        "good": get_user_input("Good"),
        "price":get_user_input("Price"),
        "date": get_user_input("Date")
    }

    return result

def get_update_expense_data():
    expense_id = int(get_user_input("Enter an ID to edit"))
    column = get_user_input("Choose name of column (good, price, date)")
    new_value = get_user_input(f"Enter a new value for {column}")

    return {"id": expense_id,"update":{column:new_value}}

def get_date_expense():
    result = {
        "start_date": get_user_input("Start date"),
        "end_date": get_user_input("End date")
    }
    
    return result

def get_price_and_operator():
    result = {
        "price": int(get_user_input("Price")),
        "comparison_operator": get_user_input("Operator (>, = , <)"),
        "start_date": get_user_input("Start date"),
        "end_date": get_user_input("End date")
    }
    
    return result 

def get_good_value():
    result = {
        "good": get_user_input("Good"),
        "start_date": get_user_input("Start date"),
        "end_date": get_user_input("End date")
    }
    return result


def get_expense_id():
    result = int(get_user_input("Enter an expense ID"))
    return result


def get_file_name() -> str:
    file_name = get_user_input(
        "Please type in the name of the Excel file where you want to save"
    )
    return file_name

def clear_screen():
    # for both linux and windows
    clear_command = "cls" if os.name == "nt" else "clear"
    os.system(clear_command)