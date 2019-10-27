from datetime import datetime
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


def read_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Try again.")


def read_date(message):
    while True:
        user_input = input(message)
        try:
            datetime.strptime(user_input, "%Y-%m-%d")
            return user_input
        except ValueError:
            print("Try again.")


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
        exit(0)
    elif user_data[0] == "a":
        registry_agents_main()
    elif user_data[0] == "o":
        traffic_officers_main()
    else:
        print("Database corrupted: utype is not valid.")
        exit(1)

    print()
    print("See you next time!")
    connection.commit()
    connection.close()


def registry_agents_main():
    while True:
        print()
        print("Welcome back, registry agent!")
        print("1. Register a birth")
        print("2. Register a marriage")
        print("3. Renew a vehicle registration")
        print("4. Process a bill of sale")
        print("5. Process a payment")
        print("6. Get a driver abstract")
        print("7. Logout")
        choice = input("Please chose an option: ")

        if choice == "1":
            print("TODO: Not implemented")
        elif choice == "2":
            print("TODO: Not implemented")
        elif choice == "3":
            print("TODO: Not implemented")
        elif choice == "4":
            print("TODO: Not implemented")
        elif choice == "5":
            print("TODO: Not implemented")
        elif choice == "6":
            print("TODO: Not implemented")
        elif choice == "7":
            break
        else:
            print("Invalid choice.")


def traffic_officers_main():
    while True:
        print()
        print("Welcome back, traffic officer!")
        print("1. Issue a ticket")
        print("2. Find a car owner")
        print("3. Logout")
        choice = input("Please chose an option: ")

        if choice == "1":
            traffic_officers_issue_ticket()
        elif choice == "2":
            print("TODO: Not implemented")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def traffic_officers_issue_ticket():
    global connection, cursor

    print()
    print("Issuing a ticket.")
    registration_number = read_int("Registration number: ")

    cursor.execute('''
        SELECT r.fname, r.lname, v.make, v.model, v.year, v.color
        FROM registrations r, vehicles v
        WHERE r.regno = ? AND r.vin = v.vin;
    ''', (registration_number,))
    row = cursor.fetchone()

    if row is None:
        print("Record not found.")
        return
    print("|".join(str(elem) for elem in row))

    violation_date = read_date("Violation date: ")
    violation_text = input("Violation text: ")
    fine_amount = read_int("Fine amount: ")

    cursor.execute(
        '''INSERT INTO tickets VALUES ((SELECT max(tno) + 1 FROM tickets), ?, ?, ?, ?);''',
        (registration_number, fine_amount, violation_text, violation_date)
    )
    connection.commit()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please provide .db file.")
    elif len(sys.argv) > 2:
        print("Only 1 argument to the .db file permitted.")
    else:
        main(sys.argv[1])
