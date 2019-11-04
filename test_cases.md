# Manual test cases:
✅ - works
❌ - broken
🔧 - fixed - plz test
🤷 - #todo, not tested yet
❓ - unsure, need clarification on what is expected.

## Login
- ✅registry agent
- ✅ traffic officer
- ✅ invalid login
- ✅ ^C exits the program but results in a stacktrace

## General
- ✅ case insensitivity

## Registry Agents

1. Register a birth
- 🔧 restricted name chars
- 🔧 gender not restricted to M/F
- ✅ mother doesn't exist
- ✅ father doesn't exist
- ✅ both parents don't exist
- ✅ both parents exist
- 🔧 baby's name shouldn't already exist in persons table. If so, warn the user
  ✅ and don't do the registration
- 🔧 person's phone number allows for invalid phone numbers to be entered.
- ✅ data in the table looks good
- 🔧 doesn't check persons table, only checks births for existing

comments: I think we should prompt the user on the input date format i.e.
YYYY-MM-DD

2. Register a marriage
- ✅ first partner doesn't exist
- ✅ second partner doesn't exist
- ✅ both don't exist
- ✅ both partners exist
- 🔧 person's phone number allows for invalid phone numbers to be entered.
- ✅ data in the table looks good

3. Renew a vehicle registration
- ✅ only accepts numerical input
- ✅ no error when a nonexistent registration number is entered
- ✅ data in the table looks good
- ✅ expiry date updates correctly if in past
- ✅ expiry date updates correctly if in future

4. Process a bill of sale
- 🔧 no error when a nonexistent registration number is entered 
- ✅ if the name of the current owner (that is provided) does not match the
  name of the most recent owner of the car in the system, the transfer cannot
  be made
- ✅ When the transfer can be made, the expiry date of the current registration
  is set to today's date and a new registration under the new owner's name is
  recorded with the registration date and the expiry date set by the system to
  today's date and a year after today's date respectively. 
- ✅ a unique registration number should be assigned by the system to the new
  registration
- ✅ data in the table looks good
- ✅ if the name of the new owener is not in the database, the transaction
  cannot be made

5. Process a payment
- ✅ if a ticket number does not exist, we're told it's invalid
- 🔧 warn the user that only one payment can be made per day on a ticket.
- ✅ warning if payment amount exceeds fine
- ✅ warning if a ticket is already payed
- ✅ data in the table looks good

6. Get a driver abstract
- 🤷 number of tickets, the number of demerit notices, the total number of
  demerit points received both within the past two years and within the
  lifetime
- ✅ user given the option to virw the tickets from latest to oldest
- 🤷 tickets displayed correctly
- 🤷 if there are more than 5 tickets, at most 5 will be shown at a time, and
  the user has an option to see more
- 🤷 the num of tickets, num of demerit notices, total number of demerit points
  received are computed for both the past 2 years and within the lifetime
- 🤷 data in the table looks good

## Traffic officers

1. Issue a ticket
- ✅ error for nonexistent registration number
- 🔧 violation text shouldn't be optional
- ✅ violation set to today's date if not provided.
- ✅ data in the table looks good


2. Find a car owner
- ✅ search by plate
- ✅ search by colour
- ✅ search by make
- ✅ search by model
- ✅ search by year
- 🤷 combinations of the above
- 🔧 when more than 4 results are returned, the menu isn't printed out, and
  "Please choose an option is printed, so the user can get confused. 
  i.e. for example:
  ```
  Please enter color: white
  1. Enter make
  2. Enter model
  3. Enter year
  4. Enter color
  5. Enter plate
  6. Execute search
  Please choose an option: 6
  0. Chevrolet|Camaro|1969|white|Z7F9J2
  1. Audi|A4|2012|white|Z7F9J2
  2. Chevrolet|Camaro|2012|white|Z7F9J2
  3. Audi|A4|2013|white|Z7F9J2
  4. Audi|A4|2014|white|Z7F9J2
  5. Audi|A4|2015|white|Z7F9J2
  6. Audi|A4|2016|white|Z7F9J2
  7. Audi|A4|2014|white|Z7F9J2
  8. Chevrolet|Camaro|2012|white|Z7F9J2
  Please choose an option:
  ```
- ❓when no search parameters are entered, all vehicles are returned. Is this
  what we want?
- 🔧 when 2 consecutive searches are done with empty parameters, sometimes we
  get 17 results (all vehicles, and when run again, we get 
  ```
  Kia|Cube|2013|red|Z7F9J2|1913-01-26|2018-07-25|Amalia|Kane
  ```
  , and then 17 results if we search again
- 🔧 overall pretty buggy when more than 4 results returned. Search can get
  executed even though 6 is not entered
  ```
  1. Enter make
  2. Enter model
  3. Enter year
  4. Enter color
  5. Enter plate
  6. Execute search
  Please choose an option: 6
  0. Chevrolet|Camaro|2012|black|M7F8J2
  1. Toyoto|Corolla|2012|red|Z7F9J2
  2. Toyoto|RAV4|2012|black|Z7F9J2
  3. Audi|A4|2012|white|Z7F9J2
  4. Chevrolet|Camaro|2012|white|Z7F9J2
  5. Chevrolet|Camaro|2012|white|Z7F9J2
  Please choose an option: 3
  Audi|A4|2012|white|Z7F9J2|2012-01-26|2008-07-25|Horace|Combs

  Welcome back, traffic officer!
  Press CTRL-C at any time to return to this menu.
  1. Issue a ticket
  2. Find a car owner
  3. Logout and exit
  Please choose an option:
  ```
- 🤷 if there are 4 or more results, then only show the make, model, year,
  colour,
  and plate
- 🤷 if a car has never been registered, then the output should indicate that
  the
  car has no owner

comments: 
- maybe after the user enters a search parameter, we replace the option with
  what they entered. i.e. they won't be able to edit a search parameter once
  entered
- counting from 0 might be confusing for the user for the search results
