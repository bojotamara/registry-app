#!/usr/bin/env python3

from getpass import getpass
from os import path
import sqlite3
import sys
import re

from registry_agent import RegistryAgent
from traffic_officer import TrafficOfficer

connection = None
cursor = None


def connect(absolute_path):
    global connection, cursor

    connection = sqlite3.connect(absolute_path)
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    connection.commit()


def login(username, password):
    """Returns the user type if user exists"""
    if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
        cursor.execute(
            """
            SELECT utype
            FROM users 
            WHERE uid LIKE ? AND pwd = ?;
        """,
            (username, password),
        )
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
    try:
        username = input("Username: ")
        password = getpass("Password: ")
    except KeyboardInterrupt:
        print("\nLogin cancelled.")
        exit(1)

    user_data = login(username, password)
    if user_data is None:
        print("Login failed.")
        exit(0)
    elif user_data[0] == "a":
        registry_agents_main(username)
    elif user_data[0] == "o":
        traffic_officers_main()
    else:
        print("Database corrupted, utype is not valid.")
        exit(1)

    print()
    print("See you next time!")
    connection.close()


def registry_agents_main(username):
    registry_agent = RegistryAgent(connection, cursor)
    while True:
        print()
        print("Welcome back, registry agent!")
        print("Press CTRL-C at any time to return to this menu.")
        print("1. Register a birth")
        print("2. Register a marriage")
        print("3. Renew a vehicle registration")
        print("4. Process a bill of sale")
        print("5. Process a payment")
        print("6. Get a driver abstract")
        print("7. Logout and exit")

        try:
            choice = input("Please choose an option: ")
            if choice == "1":
                registry_agent.register_birth(username)
            elif choice == "2":
                registry_agent.register_marriage(username)
            elif choice == "3":
                registry_agent.renew_vehicle_registration()
            elif choice == "4":
                registry_agent.process_bill_of_sale()
            elif choice == "5":
                registry_agent.process_payment()
            elif choice == "6":
                registry_agent.get_driver_abstract()
            elif choice == "7":
                break
            else:
                print("Invalid choice, please try again.")
        except KeyboardInterrupt:
            connection.rollback()
            print()
            print("Current function exited, going back to main menu.")


def traffic_officers_main():
    traffic_officer = TrafficOfficer(connection, cursor)
    while True:
        print()
        print("Welcome back, traffic officer!")
        print("Press CTRL-C at any time to return to this menu.")
        print("1. Issue a ticket")
        print("2. Find a car owner")
        print("3. Logout and exit")

        try:
            choice = input("Please choose an option: ")
            if choice == "1":
                traffic_officer.issue_ticket()
            elif choice == "2":
                traffic_officer.find_car_owner()
            elif choice == "3":
                break
            else:
                print("Invalid choice, please try again.")
        except KeyboardInterrupt:
            connection.rollback()
            print()
            print("Current function exited, going back to main menu.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please provide .db file.")
    elif len(sys.argv) > 2:
        print("Only 1 argument to the .db file permitted.")
    else:
        main(sys.argv[1])
