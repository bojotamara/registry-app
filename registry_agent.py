from datetime import date, datetime
import input_util


class RegistryAgent:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def register_birth(self, username):
        print()
        print("Registering a birth")

        first_name = input_util.read_string("Please enter baby's first name: ")
        last_name = input_util.read_string("Please enter baby's last name: ")
        gender = input_util.read_string("Please enter baby's gender (M/F): ")  # TODO: Validation
        birth_date = input_util.read_date("Please enter baby's birth date: ")
        birth_place = input_util.read_string("Please enter baby's birth place: ")
        mother_fname = input_util.read_string("Please enter mother's first name: ")
        mother_lname = input_util.read_string("Please enter mother's last name: ")
        father_fname = input_util.read_string("Please enter father's first name: ")
        father_lname = input_util.read_string("Please enter father's last name: ")
        registration_date = date.today().strftime("%Y-%m-%d")

        self.cursor.execute("""
            SELECT city
            FROM users
            WHERE uid LIKE ?;
        """, (username,))
        (city,) = self.cursor.fetchone()

        mother = self.__get_person(mother_fname, mother_lname)
        if mother is None:
            print("Mother does not exist in database, please enter her details.")
            self.__add_person(fname=mother_fname, lname=mother_lname)
            mother = self.__get_person(mother_fname, mother_lname)

        father = self.__get_person(father_fname, father_lname)
        if father is None:
            print("Father does not exist in database, please enter his details.")
            self.__add_person(fname=father_fname, lname=father_lname)
            father = self.__get_person(father_fname, father_lname)

        address = mother[4]
        phone = mother[5]
        if address is None:
            address = "NULL"
        if phone is None:
            phone = "NULL"

        self.__add_person(first_name, last_name, birth_date, birth_place, address, phone)

        self.cursor.execute("""
            INSERT INTO births
            VALUES((SELECT MAX(regno) + 1 FROM births), ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            first_name,
            last_name,
            registration_date,
            city,
            gender,
            father[0],
            father[1],
            mother[0],
            mother[1]
        ))
        self.connection.commit()

        print("Birth registered.")

    def register_marriage(self, username):
        print()
        print("Registering a marriage.")

        p1_first_name = input_util.read_string("Please enter first partner's first name: ")
        p1_last_name = input_util.read_string("Please enter first partner's last name: ")
        p2_first_name = input_util.read_string("Please enter second partner's first name: ")
        p2_last_name = input_util.read_string("Please enter second partner's last name: ")

        partner_1 = self.__get_person(p1_first_name, p1_last_name)
        if partner_1 is None:
            print("First partner does not exist in database, please enter optional details.")
            self.__add_person(fname=p1_first_name, lname=p1_last_name)
        else:
            p1_first_name = partner_1[0]
            p1_last_name = partner_1[1]

        partner_2 = self.__get_person(p2_first_name, p2_last_name)
        if partner_2 is None:
            print("Second partner does not exist in database, please enter optional details.")
            self.__add_person(fname=p2_first_name, lname=p2_last_name)
        else:
            p2_first_name = partner_2[0]
            p2_last_name = partner_2[1]

        self.cursor.execute("""
            SELECT city
            FROM users
            WHERE uid LIKE ?;
        """, (username,))
        (city,) = self.cursor.fetchone()
        reg_date = date.today().strftime("%Y-%m-%d")

        self.cursor.execute("""
            INSERT INTO marriages
            VALUES((SELECT MAX(regno) + 1 FROM marriages), ?, ?, ?, ?, ?, ?);
        """, (
            reg_date,
            city,
            p1_first_name,
            p1_last_name,
            p2_first_name,
            p2_last_name
        ))
        self.connection.commit()

        print("Marriage registered.")

    def renew_vehicle_registration(self):
        print()
        print("Renewing a vehicle registration.")

        registration_number = input_util.read_int("Please enter the vehicle registration number: ")
        self.cursor.execute("""
            SELECT expiry
            FROM registrations
            WHERE regno=?;
        """, (registration_number,))

        row = self.cursor.fetchone()
        if row is None:
            print("Record not found.")
            return

        expiry_date = datetime.strptime(row[0], "%Y-%m-%d").date()
        if expiry_date <= date.today():
            expiry_date = date.today()

        try:
            expiry_date = expiry_date.replace(year=expiry_date.year + 1)
        except ValueError:  # in case of a leap year
            expiry_date + (date(expiry_date.year + 1, 1, 1) - date(expiry_date.year, 1, 1))

        self.cursor.execute("""
            UPDATE registrations
            SET expiry=?
            WHERE regno=?;
        """, (expiry_date, registration_number))
        self.connection.commit()

        print("Vehicle registration renewed.")

    def process_bill_of_sale(self):
        print()
        print("Processing a bill of sale.")

        vin = input_util.read_int("Please enter vehicle registration number: ")

    def process_payment(self):
        print()
        print("Processing a payment.")

        while True:
            ticket_number = input_util.read_int("Please enter ticket number: ")

            self.cursor.execute("""
                SELECT fine
                FROM tickets
                WHERE tno=?;
            """, (ticket_number,))

            row = self.cursor.fetchone()
            if row is None:
                print("Invalid ticket number, please try again.")
            else:
                (fine,) = row
                self.cursor.execute("""
                    SELECT sum(amount)
                    FROM payments
                    WHERE tno=?;
                """, (ticket_number,))

                (payment_sum,) = self.cursor.fetchone()
                if payment_sum is None:
                    payment_sum = 0

                if payment_sum >= fine:
                    print("Ticket is already payed, please try again.")
                else:
                    break

        print("Fine: " + str(fine))
        print("Amount paid: " + str(payment_sum))
        while True:
            amount = input_util.read_int("Please enter the payment amount: ")
            if amount <= 0:
                print("Amount should be greater than 0, please try again.")
            elif amount + payment_sum > fine:
                print("Payment amount exceeds fine, please try again.")
            else:
                break

        pay_date = date.today().strftime("%Y-%m-%d")
        self.cursor.execute("""
            INSERT INTO payments
            VALUES(?, ?, ?);
        """, (ticket_number, pay_date, amount))
        self.connection.commit()
        print("Ticket payment processed.")

    def get_driver_abstract(self):
        print()
        print("Getting a driver abstract.")

        first_name = input_util.read_string("Please enter first name: ")
        last_name = input_util.read_string("Please enter last name: ")
        data = {'fname': first_name, 'lname': last_name}

        self.cursor.execute("""
            SELECT ticket_lifetime.tickets_count,
                   demerit_lifetime.demerit_count, demerit_lifetime.demerit_sum,
                   ticket_two_years.tickets_count,
                   demerit_two_years.demerit_count, demerit_two_years.demerit_sum
            FROM (
                SELECT COUNT(t.tno) AS tickets_count
                FROM registrations r, tickets t
                WHERE r.fname LIKE :fname AND r.lname LIKE :lname AND
                      r.regno = t.regno
            ) as ticket_lifetime, (
                SELECT COUNT(*) AS demerit_count, IFNULL(SUM(d.points), 0) AS demerit_sum
                FROM demeritNotices d
                WHERE d.fname LIKE :fname AND d.lname LIKE :lname
            ) as demerit_lifetime, (
                SELECT COUNT(t.tno) AS tickets_count
                FROM registrations r, tickets t
                WHERE r.fname LIKE :fname AND r.lname LIKE :lname AND
                      r.regno = t.regno AND
                      t.vdate >= DATE('now', '-2 years')
            ) as ticket_two_years, (
                SELECT COUNT(*) AS demerit_count, IFNULL(SUM(d.points), 0) AS demerit_sum
                FROM demeritNotices d
                WHERE d.fname LIKE :fname AND d.lname LIKE :lname AND
                      d.ddate >= DATE('now', '-2 years')
            ) as demerit_two_years;
        """, data)

        result = self.cursor.fetchone()

        print(f"Lifetime: {result[0]} tickets, {result[1]} demerit notices, {result[2]} demerit points")
        print(f"Last two years: {result[3]} tickets, {result[4]} demerit notices, {result[5]} demerit points")

        if result[0] == 0:
            return

        self.cursor.execute("""
            SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model
            FROM tickets t, registrations r, vehicles v
            WHERE r.fname LIKE :fname AND r.lname LIKE :lname AND
                  v.vin = r.vin AND r.regno = t.regno
            ORDER BY t.vdate DESC;
        """, data)
        consumed = 0

        while consumed < result[0]:
            print("1. Show tickets")
            print("2. Exit")
            choice = input("Please choose an option: ")

            if choice == "1":
                printed = 0
                while printed < 5 and consumed < result[0]:
                    print("|".join(str(elem) for elem in self.cursor.fetchone()))
                    printed += 1
                    consumed += 1
                if consumed < result[0]:
                    print("More tickets not shown, please select show tickets to show more.")
            elif choice == "2":
                break
            else:
                print("Invalid choice, please try again.")

    def __get_person(self, fname, lname):
        self.cursor.execute("""
            SELECT *
            FROM persons
            WHERE fname LIKE ? AND
                  lname LIKE ?;
        """, (fname, lname))
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

        self.cursor.execute("""
            INSERT INTO PERSONS
            VALUES(?, ?, ?, ?, ?, ?);
        """, (fname, lname, bdate, bplace, address, phone))
