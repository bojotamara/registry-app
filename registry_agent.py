import input_util
from datetime import date, datetime

class RegistryAgent:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def register_birth(self, username):
        print("Registering a birth")

        first_name = input_util.read_string("First name: ")
        last_name = input_util.read_string("Last name: ")
        gender = input_util.read_string("Gender: ")
        birth_date = input_util.read_date("Birth date: ")
        birth_place = input_util.read_string("Birth place: ")
        mother_fname = input_util.read_string("Mother first name: ")
        mother_lname = input_util.read_string("Mother last name: ")
        father_fname = input_util.read_string("Father first name: ")
        father_lname = input_util.read_string("Father last name: ")
        registration_date = date.today().strftime("%Y-%m-%d")

        self.cursor.execute(
            """SELECT city FROM users
            WHERE uid LIKE ?""",
            username,
        )
        (city,) = self.cursor.fetchone()

        mother = None
        father = None

        mother = self.__get_person(mother_fname, mother_lname)
        if mother is None:
            print("Mother does not exist in db, please enter her details: ")
            self.__add_person(fname=mother_fname, lname=mother_lname)
            mother = self.__get_person(mother_fname, mother_lname)

        father = self.__get_person(father_fname, father_lname)
        if father is None:
            print("Father does not exist in db, please enter his details: ")
            self.__add_person(fname=father_fname, lname=father_lname)
            father = self.__get_person(father_fname, father_lname)

        address = mother[4]
        phone = mother[5]
        if address is None:
            address = "NULL"
        if phone is None:
            phone = "NULL"

        self.__add_person(first_name, last_name, birth_date, birth_place, address, phone)

        self.cursor.execute(
            """INSERT INTO births
                VALUES((SELECT MAX(regno) + 1 FROM births), ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                first_name,
                last_name,
                registration_date,
                city,
                gender,
                father[0],
                father[1],
                mother[0],
                mother[1],
            ),
        )
        self.connection.commit()

        print()
        print("Birth registered!")


    def register_marriage(self, username):
        print("Registering a marriage.")
        p1_first_name = input_util.read_string("Partner 1 first name: ")
        p1_last_name = input_util.read_string("Partner 1 last name: ")
        p2_first_name = input_util.read_string("Partner 2 first name: ")
        p2_last_name = input_util.read_string("Partner 2 last name: ")

        partner_1 = self.__get_person(p1_first_name, p1_last_name)
        if partner_1 == None:
            print("Partner 1 does not exist in db, please enter optional details: ")
            self.__add_person(fname=p1_first_name, lname=p1_last_name)
        else:
            p1_first_name = partner_1[0]
            p1_last_name = partner_1[1]
        
        partner_2 = self.__get_person(p2_first_name, p2_last_name)
        if partner_2 == None:
            print("Partner 2 does not exist in db, please enter optional details: ")
            self.__add_person(fname=p2_first_name, lname=p2_last_name)
        else:
            p2_first_name = partner_2[0]
            p2_last_name = partner_2[1]

        self.cursor.execute(
            """SELECT city FROM users
            WHERE uid LIKE ?""",
            username,
        )
        (city,) = self.cursor.fetchone()
        reg_date = date.today().strftime("%Y-%m-%d")

        self.cursor.execute(
            """
            INSERT INTO marriages
            VALUES((SELECT MAX(regno) + 1 FROM marriages), ?, ?, ?, ?, ?, ?)
            """,
            (
                reg_date,
                city,
                p1_first_name,
                p1_last_name,
                p2_first_name,
                p2_last_name
            )
        )
        self.connection.commit()

        print()
        print("Marriage registered!")

    def renew_vehicle_registration(self):
        registration_number = input_util.read_int("Please enter the vehicle registration number: ")
        self.cursor.execute(
            """
            SELECT expiry
            FROM registrations
            WHERE regno=?;
            """,
            (registration_number,)
        )

        row = self.cursor.fetchone()
        if row is None:
            print("\nRecord not found.")
            return

        expiry_date = datetime.strptime(row[0], "%Y-%m-%d").date()
        if expiry_date <= date.today():
            expiry_date = date.today()

        try:
            expiry_date =  expiry_date.replace(year=expiry_date.year + 1)
        except ValueError: #in case of a leap year
            expiry_date + (date(expiry_date.year + 1, 1, 1) - date(expiry_date.year, 1, 1))

        self.cursor.execute(
            """
            UPDATE registrations
            SET expiry=?
            WHERE regno=?;
            """,
            (expiry_date, registration_number)
        )
        self.connection.commit()

        print("\nVehicle registration renewed.")
    
    
    def __get_person(self, fname, lname):
        self.cursor.execute(
            """
            SELECT *
            FROM persons
            WHERE
            fname LIKE ?
            AND
            lname LIKE ?
            """,
            (fname, lname)
        )
        return self.cursor.fetchone()

    def __add_person(
        self,
        fname: str = None,
        lname: str = None,
        bdate: str = None,
        bplace: str = None,
        address: str = None,
        phone: str = None,
    ):
        text = "Enter the person's"
        if fname is None:
            fname = input_util.read_string(f"{text} first name: ")
        if lname is None:
            lname = input_util.read_string(f"{text} last name: ")
        if bdate is None:
            bdate = input_util.read_date(f"{text} birth date: ", optional=True)
        if bplace is None:
            bplace = input_util.read_string(f"{text} birth place: ", optional=True)
        if address is None:
            address = input_util.read_string(f"{text} address: ", optional=True)
        if phone is None:
            phone = input_util.read_string(f"{text} phone number: ", optional=True)

        self.cursor.execute(
            """INSERT INTO PERSONS
                            VALUES(?, ?, ?, ?, ?, ?)""",
            (fname, lname, bdate, bplace, address, phone),
        )
        self.connection.commit()
