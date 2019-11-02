# Manual test cases:
✅ - works
❌ - broken
🤷 - not tested yet
❓ - unsure what is expected

## Login
- ✅registry agent
- ✅ traffic officer
- ✅ invalid login
- ❓ ^C exits the program but results in a stacktrace

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

comments: I think we should prompt the user on the input date format i.e.
YYYY-MM-DD



