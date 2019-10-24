import sqlite3
import sys
import re

connection = None
cursor = None


def connect(path):
    global connection, cursor
        
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()

def login(username, password):
    # Should return the user type if user exists
    if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
        cursor.execute('SELECT utype FROM users WHERE uid=? AND pwd LIKE ?;', (username, password))

        

def main(dbname):
    print("Welcome to the Registry!")
    username = input("Username: ")
    password = input("Password: ")

    path = "./" + dbname
    connect(path)

    login(username, password)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please provide .db file.")
    elif len(sys.argv) > 2:
        print("Only 1 argument to the .db file permitted.")
    else:
        main(sys.argv[1])