from getpass import getpass
from os.path import abspath
import hashlib
import sqlite3
import sys
import re

connection = None
cursor = None


def hash_pass(username, password):
    """
    Hash a password, using username as salt.
    """
    salted = password + "$" + username

    m = hashlib.sha512()
    m.update(salted.encode("utf-8"))
    print(m.hexdigest())
    return m.hexdigest()


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    connection.commit()

    connection.create_function("hash_pass", 2, hash_pass)


def login(username, password):
    # Should return the user type if user exists
    if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
        hash_pass(username, password)
        cursor.execute(
            'SELECT utype FROM users WHERE uid LIKE ? AND pwd = hash_pass(?, ?);',
            (username, username, password)
        )


def main(dbname):
    print("Welcome to the Registry!")

    path = abspath(dbname)
    connect(path)

    while True:
        print("")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Please chose an option: ")

        if choice == "1":
            main_login()
        elif choice == "2":
            print("TODO: Not implemented")
        elif choice == "3":
            break
        else:
            print("Invalid choice")

    connection.commit()
    connection.close()


def main_login():
    username = input("Username: ")
    password = input("Password: ")  # getpass("Password: ")

    login(username, password)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please provide .db file.")
    elif len(sys.argv) > 2:
        print("Only 1 argument to the .db file permitted.")
    else:
        main(sys.argv[1])
