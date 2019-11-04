import input_util


class TrafficOfficer:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def issue_ticket(self):
        print()
        print("Issuing a ticket.")
        registration_number = input_util.read_int("Please enter registration number: ")

        self.cursor.execute(
            """
            SELECT r.fname, r.lname, v.make, v.model, v.year, v.color
            FROM registrations r, vehicles v
            WHERE r.regno = ? AND r.vin = v.vin;
        """,
            (registration_number,),
        )
        row = self.cursor.fetchone()

        if row is None:
            print("Record not found.")
            return
        print("|".join(str(elem) for elem in row))

        violation_date = input_util.read_date(
            "Please enter violation date: ", optional=True
        )
        violation_text = input_util.read_string("Please enter violation text: ")
        fine_amount = input_util.read_int("Please enter fine amount: ")

        self.cursor.execute(
            """
            INSERT INTO tickets 
            VALUES ((SELECT max(tno) + 1 FROM tickets), ?, ?, ?, IFNULL(?, DATE('now')));
        """,
            (registration_number, fine_amount, violation_text, violation_date),
        )
        self.connection.commit()

        print("Ticket Issued.")

    def find_car_owner(self):
        print()
        print("Finding a car owner.")

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

        self.cursor.execute(
            """
            SELECT vin, make, model, year, color, plate
            FROM (
                  SELECT regno, vin, make, model, year, color, plate
                  FROM vehicles LEFT OUTER JOIN registrations USING (vin)
                  UNION
                  SELECT regno, vin, make, model, year, color, plate
                  FROM registrations LEFT OUTER JOIN vehicles USING (vin)
            )
            WHERE make LIKE ? AND
                  model LIKE ? AND
                  year LIKE ? AND
                  color LIKE ? AND
                  IFNULL(plate, '') LIKE ?;
        """,
            (make, model, year, color, plate),
        )
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            print("No result.")
        elif len(rows) >= 4:
            for i in range(len(rows)):
                print(
                    str(i)
                    + ". "
                    + "|".join(self.__normalize_vehicle_summary(rows[i][1:]))
                )

            choice = input_util.read_int(
                "Please choose a result to see full information: "
            )
            if choice < 0 or choice >= len(rows):
                print("Invalid choice.")
                return

            self.__print_row(rows[choice])
        else:
            for row in rows:
                self.__print_row(row)

    def __normalize_vehicle_summary(self, row):
        data = list(row)
        for i in range(len(data)):
            if data[i] is None:
                data[i] = "<this car has no plate number>"
            else:
                data[i] = str(data[i])
        return data

    def __print_row(self, row):
        self.cursor.execute(
            """
            SELECT regdate, expiry, fname, lname
            FROM registrations
            WHERE vin = ?
            ORDER BY regdate DESC
            LIMIT 1;
        """,
            (row[0],),
        )
        full_row = self.cursor.fetchone()

        print("|".join(self.__normalize_vehicle_summary(row[1:])), end="|")
        if full_row is None:
            print("<this car has no owner>")
        else:
            print("|".join(str(elem) for elem in full_row))
