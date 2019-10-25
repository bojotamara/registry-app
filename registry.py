from getpass import getpass
from os import path
import sqlite3
import sys
import re

connection = None
cursor = None


def connect(absolute_path):
    global connection, cursor

    connection = sqlite3.connect(absolute_path)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    connection.commit()


def login(username, password):
    # Should return the user type if user exists
    if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
        cursor.execute('SELECT utype FROM users WHERE uid LIKE ? AND pwd = ?;', (username, password))
        return cursor.fetchone()
    else:
        return None


def main(dbname):
    absolute_path = path.abspath(dbname)
    if not path.exists(absolute_path):
        print("Provided .db file does not exist.")
        exit(1)
    connect(absolute_path)

    print("Welcome to the Registry!")

    print("Please login.")
    username = input("Username: ")
    password = getpass("Password: ")

    user_data = login(username, password)
    if user_data is None:
        print("Login failed.")
    elif user_data[0] == "a":
        registry_agents_main()
    elif user_data[0] == "o":
        traffic_officers_main()
    else:
        print("Database corrupted: utype is not valid.")
        exit(1)

    connection.commit()
    connection.close()


def registry_agents_main():
    while True:
        print("Welcome back, registry agent!")
        print("1. Register a birth")
        print("2. Register a marriage")
        print("3. Logout")
        choice = input("Please chose an option: ")

        if choice == "1":
            print("TODO: Not implemented")
        elif choice == "2":
            print("TODO: Not implemented")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def traffic_officers_main():
    while True:
        print("Welcome back, traffic officer!")
        print("1. Issue a ticket")
        print("2. Find a car owner")
        print("3. Logout")
        choice = input("Please chose an option: ")

        if choice == "1":
            print("TODO: Not implemented")
        elif choice == "2":
            print("TODO: Not implemented")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please provide .db file.")
    elif len(sys.argv) > 2:
        print("Only 1 argument to the .db file permitted.")
    else:
        main(sys.argv[1])
