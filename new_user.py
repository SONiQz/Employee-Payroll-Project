from menu_objs import clear, disp_menu, check_valid_date, is_valid_postcode

# Menu Name that is printed to screen.
menu_name = 'New Employee'

# Dictionary used to generate User records.
userinfo = {'First Name': '',
            'Surname': '',
            'Address Ln 1': '',
            'Address Ln 2': '',
            'City': '',
            'County': '',
            'Postcode': '',
            'Phone Number': '',
            'Start Date': '',
            'Employee Designation': '',
            'Employee Grade': '',
            'Removed': 'N',
            }

# Dictionary used to generate Payroll Values.
payroll = {'Employee Loan': '',
           'House Allowance': '',
           'Travel Allowance': '',
           'Health Allowance': ''
           }


# Calculates if a user table contains a key value, if not sets the key value to 1, if so, finds the
# highest value and + 1
def new_key(user_table):
    if len(user_table) is None:
        max_key = 1
    else:
        max_key = max(user_table, key=lambda k: int(k))
        max_key = int(max_key) + 1
    return max_key


# function to create a new user
def user_add_loop(add_list, curr_menu_name):
    # displays values to be entered and current defined values
    disp_menu(add_list, curr_menu_name)
    # Iterates through the appropriate dictionary of values to create
    for key, value in add_list.items():
        if curr_menu_name == 'New Employee' and key in 'Removed':  # Stops new users being set to removed
            continue
        elif key in ('First Name', 'Surname', 'City', 'County'):  # for common values set input to value for defined key
            clear()
            disp_menu(add_list, curr_menu_name)
            while True:
                new_option = input(key + ': ')
                if new_option.isalpha():
                    add_list.update({key: new_option})
                    break
                else:
                    print("Input is invalid. Please try again.")
        elif key in 'Phone Number':  # for Phone Number only permit integer values.
            while True:
                clear()
                disp_menu(add_list, curr_menu_name)
                new_option = input(key + ': ')
                if new_option.isdigit():
                    add_list.update({key: new_option})
                    break
                else:
                    print("Input is Invalid. Please try again")
        elif key in 'Employee Grade':  # For Employee Grade only accept values 1-4 (in int or roman numerals)
            valid_options = ["I", "II", "III", "IV", "1", "2", "3", "4"]
            while True:
                new_option = input(key + " - Input value Between 1 - 4 (or I - IV)" + ': ')
                if new_option in valid_options:
                    add_list.update({key: new_option})
                    break
                else:
                    print("Input is invalid. Please try again.")
        elif key == 'Postcode':  # For postcode, carry out postcode validation
            clear()
            disp_menu(add_list, curr_menu_name)
            new_option = is_valid_postcode(called_by="New")
            clear()
            add_list.update({key: new_option})
        elif key == 'Start Date':  # For Start Date, validate it is a plausible date.
            clear()
            disp_menu(add_list, curr_menu_name)
            new_option = check_valid_date('New')
            add_list.update({key: new_option})
        # If a Keys Value contains a value, allow this to be displayed to screen. Largely unused due to changes in menus.
        elif len(value) > 0:
            clear()
            disp_menu(add_list, curr_menu_name)
            new_option = input(key + ' (' + value + '): ')
            clear()
            add_list.update({key: new_option})
        # If a Key/Value isn't covered above, use the default operation to allow input and set key-value pair.
        else:
            clear()
            disp_menu(add_list, curr_menu_name)
            new_option = input(key + ': ')
            clear()
            add_list.update({key: new_option})
    return add_list
