#!/usr/bin/env python

from datetime import datetime, date
from getpass import getpass
from os import path
import sqlite3
import sys
import re

import uuid

connection = None
cursor = None


def connect(absolute_path):
    global connection, cursor

    connection = sqlite3.connect(absolute_path)
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    connection.commit()


def login(username, password):
    # Should return the user type if user exists
    if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
        cursor.execute(
            "SELECT utype FROM users WHERE uid LIKE ? AND pwd = ?;",
            (username, password),
        )
        return cursor.fetchone()
    else:
        return None


def read_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Try again.")


def read_date(message, optional=False):
    while True:
        user_input = input(message)
        if user_input == "" and optional:
            return None
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
        registry_agents_main(user_data)
    elif user_data[0] == "o":
        traffic_officers_main()
    else:
        print("Database corrupted: utype is not valid.")
        exit(1)

    print()
    print("See you next time!")
    connection.commit()
    connection.close()


def registry_agents_main(user_data):
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
        choice = input("Please choose an option: ")

        if choice == "1":
            registry_agent_register_birth(user_data)
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
        choice = input("Please choose an option: ")

        if choice == "1":
            traffic_officers_issue_ticket()
        elif choice == "2":
            traffic_officers_find_car_owner()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def traffic_officers_issue_ticket():
    global connection, cursor

    print()
    print("Issuing a ticket.")
    registration_number = read_int("Please enter registration number: ")

    cursor.execute(
        """
        SELECT r.fname, r.lname, v.make, v.model, v.year, v.color
        FROM registrations r, vehicles v
        WHERE r.regno = ? AND r.vin = v.vin;
    """,
        (registration_number,),
    )
    row = cursor.fetchone()

    if row is None:
        print("Record not found.")
        return
    print("|".join(str(elem) for elem in row))

    violation_date = read_date("Please enter violation date: ", optional=True)
    violation_text = input("Please enter violation text: ")
    fine_amount = read_int("Please enter fine amount: ")

    cursor.execute(
        """INSERT INTO tickets VALUES ((SELECT max(tno) + 1 FROM tickets), ?, ?, ?, IFNULL(?, DATE('now')));""",
        (registration_number, fine_amount, violation_text, violation_date),
    )
    connection.commit()


def traffic_officers_find_car_owner():
    global cursor

    print()
    print("Find a car owner.")

    make = "%"
    model = "%"
    year = "%"
    color = "%"
    plate = "%"

    while True:
        print("1. Enter make")
        print("2. Enter model")
        print("3. Enter year")
        print("4. Enter color")
        print("5. Enter plate")
        print("6. Execute search")
        choice = input("Please choose an option: ")

        if choice == "1":
            make = input("Please enter make: ")
        elif choice == "2":
            model = input("Please enter model: ")
        elif choice == "3":
            year = input("Please enter year: ")
        elif choice == "4":
            color = input("Please enter color: ")
        elif choice == "5":
            plate = input("Please enter plate: ")
        elif choice == "6":
            break
        else:
            print("Invalid choice.")

    cursor.execute(
        """
        SELECT v.vin, v.make, v.model, v.year, v.color, r.plate
        FROM vehicles v, registrations r
        WHERE v.vin = r.vin AND
              v.make LIKE ? AND
              v.model LIKE ? AND
              v.year LIKE ? AND
              v.color LIKE ? AND
              r.plate LIKE ?
    """,
        (make, model, year, color, plate),
    )
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No result.")
    elif len(rows) > 4:
        for i in range(len(rows)):
            print(str(i) + ". " + "|".join(str(elem) for elem in rows[i][1:]))

        choice = read_int("Please choose an option: ")
        if choice < 0 or choice >= len(rows):
            print("Invalid choice.")
            return

        traffic_officers_find_car_owner_print_row(rows[choice])
    else:
        for row in rows:
            traffic_officers_find_car_owner_print_row(row)


def traffic_officers_find_car_owner_print_row(row):
    global cursor

    cursor.execute(
        """
        SELECT regdate, expiry, fname, lname
        FROM registrations
        WHERE vin = ?
        ORDER BY regdate DESC
        LIMIT 1;
    """,
        (row[0],),
    )
    full_row = cursor.fetchone()

    print("|".join(str(elem) for elem in row[1:]), end="|")
    print("|".join(str(elem) for elem in full_row))


def registry_agent_register_birth(user_data):
    global cursor, connection

    print(user_data)
    print("Registering a birth")

    first_name = input("First name: ")
    last_name = input("Last name: ")
    gender = input("Gender: ")
    birth_date = read_date("Birth date: ")
    birth_place = input("Birth place: ")
    mother_fname = input("Mother first name: ")
    mother_lname = input("Mother last name: ")
    father_fname = input("Father first name: ")
    father_lname = input("Father last name: ")
    registration_date = date.today().strftime("%Y-%m-%d")

    cursor.execute(
        """SELECT city FROM users
    WHERE uid = ?""",
        user_data[0],
    )
    city = cursor.fetchone()

    regno = uuid.uuid1()

    mother = None
    father = None

    def getParent(parent: bool = True):  # mother is true, father is false
        cursor.execute(
            """SELECT fname, lname, address
        FROM persons
        WHERE
        fname=?
        AND
        lname=?
        """,
            (
                mother_fname if parent else father_fname,
                mother_lname if parent else father_lname,
            ),
        )
        if parent:
            mother = cursor.fetchone()
        else:
            father = cursor.fetchone()

    getParent(True)
    if mother is None:
        print("Mother does not exist in db, please enter her details: ")
        add_person(fname=mother_fname, lname=mother_lname)
        getParent(True)

    getParent(False)
    if father is None:
        print("Father does not exist in db, please enter his details: ")
        add_person(fname=father_fname, lname=father_lname)
        getParent(False)

    print("MOTHER: ", mother)
    address = mother[4]
    if addreess is None:
        address = input("Enter the baby's address: ")

    phone = mother[5]
    if phone is None:
        phone = input("Enter the baby's phone number: ")

    cursor.execute(
        """INSERT INTO births
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        regno,
        first_name,
        last_name,
        registration_date,
        city,
        gender,
        father[0],
        father[1],
        mother[0],
        mother[1],
    )
    connection.commit()


def add_person(
    fname: str = None,
    lname: str = None,
    bdate: str = None,
    bplace: str = None,
    address: str = None,
    phone: str = None,
):
    global cursor, connection

    text = "Enter the person's"
    if fname is None:
        fname = input(f"{text} first name: ")
    if lname is None:
        lname = input(f"{text} last name: ")
    if bdate is None:
        bdate = input(f"{text} birth date: ")
    if bplace is None:
        bplace = input(f"{text} birth place: ")
    if address is None:
        address = input(f"{text} address: ")
    if phone is None:
        phone = input(f"{text} phone number: ")

    # TODO values other then fname, lname can be set to null if not provided.
    cursor.execute(
        """INSERT INTO PERSONS
                        VALUES(?, ?, ?, ?, ?, ?)""",
        (fname, lname, bdate, bplace, address, phone),
    )
    connection.commit()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please provide .db file.")
    elif len(sys.argv) > 2:
        print("Only 1 argument to the .db file permitted.")
    else:
        main(sys.argv[1])
