import sqlite3
import sys

connection = None
cursor = None

def connect(path):
    global connection, cursor
        
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
  
def login(username, password):
    #Should return user type
    pass

def main(dbname):
    print("Welcome to the Registry!")
    username = input("Username: ")
    password = input("Password: ")

    path = "./" + dbname
    connect(path)
   
    connection.commit()
    connection.close()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please provide .db file.")
    elif len(sys.argv) > 2:
        print("Only 1 argument to the .db file permitted.")
    else:
        main(sys.argv[1])