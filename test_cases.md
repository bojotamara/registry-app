# Manual test cases:
✅ - works
❌ - broken
🤷 - #todo, not tested yet
❓ - unsure, need clarification on what is expected.

## Login
- ✅registry agent
- ✅ traffic officer
- ✅ invalid login
- ❓ ^C exits the program but results in a stacktrace

## General
- ✅ case insensitivity

## Registry Agents

1. Register a birth
- ❓ are characters like ?\*! allowed for first/last name
- ❌ gender not restricted to M/F
- 🤷 mother doesn't exist 
- 🤷 father doesn't exist
- 🤷 both parents don't exist
- 🤷 both parents exist
- ❌ baby's name shouldn't already exist in persons table. If so, warn the user
     - results in a stacktrace (unique integrity constraint fails in the db),
       and user is not warned
  🤷 and don't do the registration
- ❌ person's phone number allows for invalid phone numbers to be entered.
- 🤷 data in the table looks good

comments: I think we should prompt the user on the input date format i.e.
YYYY-MM-DD

2. Register a marriage
- 🤷 first partner doesn't exist
- 🤷 second partner doesn't exist
- 🤷 both partners exist
- ❌ person's phone number allows for invalid phone numbers to be entered.
- 🤷 data in the table looks good

3. Renew a vehicle registration
- ✅ only accepts numerical input
- ❌ no error when a nonexistent registration number is entered
- 🤷 data in the table looks good

4.
- ❌ no error when a nonexistent registration number is entered 
- 🤷 if the name of the current owner (that is provided) does not match the
  name of the most recent owner of the car int eh system, the transfer cannot
  be made
- 🤷 When the transfer can be made, the expiry date of the current registration
  is set to today's date and a new registration under the new owner's name is
  recorded with the registration date and the expiry date set by the system to
  today's date and a year after today's date respectively. 
- 🤷 a unique registration number should be assigned by the system to the new
  registration

5. Process a payment
- ✅ if a ticket number does not exist, we're told it's invalid
- ❌ warn the user that only one payment can be made per day on a ticket.
  (right now, we get a stack trace on the db's unique integrity constraint
  failing.)
- ✅ warning if payment amount exceeds fine
- ✅ warning if a ticket is already payed
- ❓ should decimal input be allowed? i.e. paying $13.50 

comments: maybe if a ticket number is not found, we tell the user that it does
not exist instead of saying it's invalid, and we say it's invalid if they enter
non-numerical input

6.
- 🤷 number of tickets, the number of demerit notices, the total number of
  demerit points received both within the past two years and within the
  lifetime
- ✅ user given the option to virw the tickets from latest to oldest
- 🤷 tickets displayed correctly
- 🤷 if there are more than 5 tickets, at most 5 will be shown at a time, and
  the user has an option to see more

