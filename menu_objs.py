# Import for handling Regular Expression (regex) handling for strings
import re

# Import OS information for clear functions
from os import system, name

# PyFiglet makes cool text art
from pyfiglet import Figlet

# Used to identify max/min values for string lengths.
from math import ceil, floor

# Define basic setting for Figlet headings
f = Figlet(width=80, justify='center')


# Clear Function for cross-platform compatibility.
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


# Check if year is a leap-year for check_valid_date
def is_leap_year(year):
    year = int(year)
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    else:
        return False


# Perform validation of dates entered in date fields
def check_valid_date(called_by=None, value=None):
    # Check if script has been called by the new_user functions to adapt input prompt.
    while True:
        if called_by == 'New':
            input_date = input("Enter Start Date in the format dd/mm/yyyy: ")
        elif called_by == 'Mod':
            input_date = input("Enter Start Date in the format dd/mm/yyyy (" + value + "):")
        else:
            input_date = input("Enter Payroll Date in the format dd/mm/yyyy: ")
        # Validate dates, whether char lengths are appropriate, month can't be greater than 12, day can't exceed 31,
        # and cannot be set to 31 for specified months. February has additional handing to ensure that it is able to
        # set valid values for Leap Years using the is_leap_year function.
        try:
            day, month, year = input_date.split("/")
            if len(year) != 4 or len(month) != 2 or len(day) != 2:
                raise ValueError("Invalid date format")
            elif int(month) > 12:
                raise ValueError("Invalid date format")
            elif int(day) > 31:
                raise ValueError("Invalid date format")
            elif int(day) == 31 and month in ('04', '09', '07', '11'):
                raise ValueError("Invalid date format")
            elif int(month) == 2 and int(day) >= 29:
                ok_year = is_leap_year(year)
                print(ok_year)
                if is_leap_year(year):
                    return input_date
                else:
                    if int(day) > 29:
                        raise ValueError("Invalid date value")
            else:
                return input_date
        except ValueError:
            print("Invalid Date Values or Format")


# Validates the Postcode field meets the expected syntax for a UK Postcode. Spaces are removed.
def is_valid_postcode(called_by=None, value=None):
    postcode_pattern = r'^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$'
    while True:
        if called_by == 'New':
            postcode = input("Post Code: ")
        else:
            postcode = input("Post Code (" + value + "):")
            if len(postcode) == 0:
                postcode = value
        postcode = postcode.upper().replace(' ', '')
        if re.match(postcode_pattern, postcode):
            return postcode
        else:
            input("Postcode Not Valid")

# Generates a box around text pushed as "msg" using format_line to generate start and end characters for lines.
# Used for menus and subheadings.
def boxed_msg(msg):
    lines = msg.split('\n')
    max_length = max([len(line) for line in lines])
    head_foot = '+' + '-' * (max_length + 2) + '+'
    res = '{:^80}'.format(head_foot) + '\n'
    for i in lines:
        curr_line = format_line(i, max_length)
        res += curr_line
    res += '{:^80}'.format(head_foot) + '\n'
    return res


# Used to add line start and end for boxed_msg lines.
def format_line(line, max_length):
    half_dif = (max_length - len(line)) / 2
    curr_line = '{:^80}'.format('| ' + ' ' * ceil(half_dif) + line + ' ' * floor(half_dif) + ' |')
    curr_line = curr_line + '\n'
    return curr_line


# Outputs Menu data to screen.
def disp_menu(menu_options, menu_name):
    clear()
    menu_list = ''
    print(f.renderText('CT5057 Payroll'))  # Prints App Heading
    print(boxed_msg(menu_name))  # Prints Menu Name in a Box
    # The below will supress a Menu Box if not required and iterate through menu items if presented. Allowing the
    # user to interact using Key values.
    if menu_name == 'Employee Search' or menu_name == 'Print Payslip' or menu_name == 'Employee List':
        pass
    else:
        for key, value in menu_options.items():
            if menu_name == 'New Employee' and key == 'Removed':
                continue
            else:
                if len(menu_list) == 0:
                    menu_list = menu_list + str(key + ': ' + str(value))
                else:
                    menu_list = menu_list + str('\n' + key + ': ' + str(value))
        print(boxed_msg(menu_list))


'''
def disp_input(menu_name):
    clear()
    print(f.renderText('CT5057 Payroll'))
    print(boxed_msg(menu_name))
    employee_no = input('Employee Number:')
    return employee_no
'''

# Outputs pithy text using Figlet styling on Quit.
def quit_menu():
    print(f.renderText('Thanks For'))
    print(f.renderText('Playing'))
