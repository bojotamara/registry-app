from datetime import datetime

def read_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Try again.")

def read_date(message, optional=False):
    if optional:
        message = "(Optional) " + message
    while True:
        user_input = input(message)
        if user_input == "" and optional:
            return None
        try:
            datetime.strptime(user_input, "%Y-%m-%d")
            return user_input
        except ValueError:
            print("Try again.")

def read_string(message, optional=False):
    if optional:
        message = "(Optional) " + message
    while True:
        user_input = input(message)
        if user_input == "" and optional:
            return None
        elif user_input != "":
            return user_input
        else:
            print("Input required.")