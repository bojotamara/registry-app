from datetime import date, datetime
import input_util
import re


class RegistryAgent:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def register_birth(self, username):
        print()
        print("Registering a birth")

        first_name = input_util.read_name("Please enter baby's first name: ")
        last_name = input_util.read_name("Please enter baby's last name: ")

        self.cursor.execute(
            """
            SELECT *
            FROM births b, persons p
            WHERE (b.fname LIKE ?
            AND b.lname LIKE ?) OR
            (p.fname LIKE ?
            AND p.lname LIKE ?);
        """,
            (first_name, last_name, first_name, last_name),
        )

        if self.cursor.fetchone() is not None:
            print("\nPerson with same name already exists. Cancelling registration...")
            return

        gender = None
        while True:
            gender = input_util.read_string("Please enter baby's gender (M/F): ")
            if (
                gender.casefold() == "m".casefold()
                or gender.casefold() == "f".casefold()
            ):
                break
            print("Gender must either be m or f, please try again")

        while True:
            birth_date = input_util.read_date("Please enter baby's birth date: ")
            bday_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
            if bday_date > date.today():
                print("Baby can't be born in the future.")
            else:
                break

        birth_place = input_util.read_string("Please enter baby's birth place: ")
        mother_fname = input_util.read_name("Please enter mother's first name: ")
        mother_lname = input_util.read_name("Please enter mother's last name: ")
        father_fname = input_util.read_name("Please enter father's first name: ")
        father_lname = input_util.read_name("Please enter father's last name: ")
        registration_date = date.today().strftime("%Y-%m-%d")

        self.cursor.execute(
            """
            SELECT city
            FROM users
            WHERE uid LIKE ?;
        """,
            (username,),
        )
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

        self.__add_person(
            first_name, last_name, birth_date, birth_place, address, phone
        )

        self.cursor.execute(
            """
            INSERT INTO births
            VALUES((SELECT MAX(regno) + 1 FROM births), ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
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

        print("Birth registered.")

    def register_marriage(self, username):
        print()
        print("Registering a marriage.")

        p1_first_name = input_util.read_name(
            "Please enter first partner's first name: "
        )
        p1_last_name = input_util.read_name("Please enter first partner's last name: ")
        p2_first_name = input_util.read_name(
            "Please enter second partner's first name: "
        )
        p2_last_name = input_util.read_name("Please enter second partner's last name: ")

        partner_1 = self.__get_person(p1_first_name, p1_last_name)
        if partner_1 is None:
            print(
                "First partner does not exist in database, please enter optional details."
            )
            self.__add_person(fname=p1_first_name, lname=p1_last_name)
        else:
            p1_first_name = partner_1[0]
            p1_last_name = partner_1[1]

        partner_2 = self.__get_person(p2_first_name, p2_last_name)
        if partner_2 is None:
            print(
                "Second partner does not exist in database, please enter optional details."
            )
            self.__add_person(fname=p2_first_name, lname=p2_last_name)
        else:
            p2_first_name = partner_2[0]
            p2_last_name = partner_2[1]

        self.cursor.execute(
            """
            SELECT city
            FROM users
            WHERE uid LIKE ?;
        """,
            (username,),
        )
        (city,) = self.cursor.fetchone()
        reg_date = date.today().strftime("%Y-%m-%d")

        self.cursor.execute(
            """
            INSERT INTO marriages
            VALUES((SELECT MAX(regno) + 1 FROM marriages), ?, ?, ?, ?, ?, ?);
        """,
            (reg_date, city, p1_first_name, p1_last_name, p2_first_name, p2_last_name),
        )
        self.connection.commit()

        print("Marriage registered.")

    def renew_vehicle_registration(self):
        print()
        print("Renewing a vehicle registration.")

        registration_number = input_util.read_int(
            "Please enter the vehicle registration number: "
        )
        self.cursor.execute(
            """
            SELECT expiry
            FROM registrations
            WHERE regno = ?;
        """,
            (registration_number,),
        )

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
            expiry_date + (
                date(expiry_date.year + 1, 1, 1) - date(expiry_date.year, 1, 1)
            )

        self.cursor.execute(
            """
            UPDATE registrations
            SET expiry = ?
            WHERE regno = ?;
        """,
            (expiry_date, registration_number),
        )
        self.connection.commit()

        print("Vehicle registration renewed.")

    def process_bill_of_sale(self):
        print()
        print("Processing a bill of sale.")

        vin = input_util.read_string("Please enter vehicle identification number: ")
        self.cursor.execute(
            """
            SELECT regno, vin, fname, lname
            FROM registrations r
            WHERE r.vin LIKE ?
            ORDER BY regdate DESC;
        """,
            (vin,),
        )

        current_registration = self.cursor.fetchone()
        if current_registration is None:
            print("The vehicle identification number does not exist.")
            return

        current_fname = input_util.read_name(
            "Please enter current owner's first name: "
        )
        current_lname = input_util.read_name("Please enter current owner's last name: ")

        registered_fname = current_registration[2].lower()
        registered_lname = current_registration[3].lower()
        if (
            registered_fname != current_fname.lower()
            or registered_lname != current_lname.lower()
        ):
            print("The vehicle is owned by someone else, transaction cannot be done.")
            return

        new_fname = input_util.read_name("Please enter new owner's first name: ")
        new_lname = input_util.read_name("Please enter new owner's last name: ")

        new_owner = self.__get_person(new_fname, new_lname)
        if new_owner is None:
            print("New owner does not exist in database, transaction cannot be done.")
            return

        plate = input_util.read_string("Please enter plate number: ")

        self.cursor.execute(
            """
            UPDATE registrations
            SET expiry = DATE('now')
            WHERE regno = ?;
        """,
            (current_registration[0],),
        )
        self.cursor.execute(
            """
            INSERT INTO registrations
            VALUES ((SELECT MAX(regno) + 1 FROM registrations), DATE('now'), DATE('now', '+1 year'), ?, ?, ?, ?);
        """,
            (plate, current_registration[1], new_owner[0], new_owner[1]),
        )
        self.connection.commit()

        print("Bill of sale processed.")

    def process_payment(self):
        print()
        print("Processing a payment.")

        while True:
            ticket_number = input_util.read_int("Please enter ticket number: ")

            self.cursor.execute(
                """
                SELECT fine
                FROM tickets
                WHERE tno = ?;
            """,
                (ticket_number,),
            )

            row = self.cursor.fetchone()
            if row is None:
                print("Ticket doesn't exist, please try again.")
            else:
                (fine,) = row

                self.cursor.execute(
                    """
                    SELECT pdate
                    FROM payments
                    WHERE tno = ?
                    ORDER BY pdate DESC
                    LIMIT 1;
                """,
                    (ticket_number,),
                )
                latest_payment = self.cursor.fetchone()
                if latest_payment is not None:
                    (latest_payment,) = latest_payment

                if latest_payment == date.today().strftime("%Y-%m-%d"):
                    print(
                        "A payment was already made today for this ticket, cancelling..."
                    )
                    return

                self.cursor.execute(
                    """
                    SELECT sum(amount)
                    FROM payments
                    WHERE tno = ?;
                """,
                    (ticket_number,),
                )

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
        self.cursor.execute(
            """
            INSERT INTO payments
            VALUES(?, ?, ?);
        """,
            (ticket_number, pay_date, amount),
        )
        self.connection.commit()

        print("Ticket payment processed.")

    def get_driver_abstract(self):
        print()
        print("Getting a driver abstract.")

        first_name = input_util.read_name("Please enter first name: ")
        last_name = input_util.read_name("Please enter last name: ")
        data = {"fname": first_name, "lname": last_name}

        self.cursor.execute(
            """
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
        """,
            data,
        )

        result = self.cursor.fetchone()

        print(
            "Lifetime: "
            + str(result[0])
            + " tickets, "
            + str(result[1])
            + " demerit notices, "
            + str(result[2])
            + " demerit points"
        )
        print(
            "Last two years: "
            + str(result[3])
            + " tickets, "
            + str(result[4])
            + " demerit notices, "
            + str(result[5])
            + " demerit points"
        )

        if result[0] == 0:
            return

        self.cursor.execute(
            """
            SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model
            FROM tickets t, registrations r, vehicles v
            WHERE r.fname LIKE :fname AND r.lname LIKE :lname AND
                  v.vin = r.vin AND r.regno = t.regno
            ORDER BY t.vdate DESC;
        """,
            data,
        )
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
                    print(
                        "More tickets not shown, please select show tickets to show more."
                    )
            elif choice == "2":
                break
            else:
                print("Invalid choice, please try again.")

    def __get_person(self, fname, lname):
        self.cursor.execute(
            """
            SELECT *
            FROM persons
            WHERE fname LIKE ? AND
                  lname LIKE ?;
        """,
            (fname, lname),
        )
        return self.cursor.fetchone()

    def __add_person(
        self,
        fname: str = "",
        lname: str = "",
        bdate: str = "",
        bplace: str = "",
        address: str = "",
        phone: str = "",
    ):
        text = "Enter the person's"
        if fname == "":
            fname = input_util.read_name(text + " first name: ")
        if lname == "":
            lname = input_util.read_name(text + " last name: ")
        if bdate == "":
            bdate = input_util.read_date(text + " birth date: ", optional=True)
        if bplace == "":
            bplace = input_util.read_string(text + " birth place: ", optional=True)
        if address == "":
            address = input_util.read_string(text + " address: ", optional=True)

        phone_regex = re.compile(r"\d{3}-\d{3}-\d{4}$")
        if phone == "":
            phone = None
            while phone is None:
                phone = input_util.read_string(
                    text + " phone number (XXX-XXX-XXXX): ", optional=True
                )
                if phone is None:  # optional
                    break
                if not phone_regex.match(phone):
                    phone = None
                    print(
                        "Phone number entered in wrong format, please try again, or leave blank"
                    )

        self.cursor.execute(
            """
            INSERT INTO persons
            VALUES(?, ?, ?, ?, ?, ?);
        """,
            (fname, lname, bdate, bplace, address, phone),
        )
