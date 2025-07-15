# Importing Libs from project that calls are made to
import del_user
import list_users
import menu_objs
import mod_user
import print_pay
import new_user
import search_user
import write_file
from menu_objs import clear, disp_menu

# JSON Library for File Syntax and writing
import json

# Used to manage Sleep operations to add manual delays to operations.
from time import sleep


# Set Globals for the table data to be held across operations.
global user_table
global payroll_table
global fiscal_table


# Open Dictionaries that function as Data Store for Program
# user_table is for employee data, payroll_table includes values for payroll routines
# fiscal_table includes all payslip information.
def open_dict():
    global user_table
    global payroll_table
    global fiscal_table
    try:
        with open("dicts.txt", "r") as file:  # Define file for dictionary/tables
            openfile = json.load(file)  # trigger file to open
            user_table = openfile['user']  # Define the location of User data
            payroll_table = openfile['payroll']  # Define the location of Payroll data
            fiscal_table = openfile['fiscal']  # Define the location of Fiscal data
            print("Opening Database")
    # Define exception handler if dictionary is missing or corrupt.
    except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError):
        # Set default layout
        data = {"user": {},
                "payroll": {},
                "fiscal": {},
                }
        make_json = json.dumps(data, indent=4)  # Set styling for JSON
        with open("dicts.txt", "w") as outfile:  # Write file
            outfile.write(make_json)
            outfile.flush()
    return user_table, payroll_table, fiscal_table  # Push dictionaries to the global variables.


# Define options for the Main Menu and prompt for user to select option.
def main_menu():
    clear()
    menu_name = 'Main Menu'
    menu_options = {
        'N': 'Add a (N)ew Employee',
        'M': '(M)odify a Existing Employee',
        'D': '(D)elete an Existing Employee',
        'P': '(P)rint Employee Payslip',
        'R': 'Search and Display (R)ecord',
        'L': 'Display (L)ist',
        'Q': '(Q)uit'
    }
    disp_menu(menu_options, menu_name)
    option = input('Enter your choice (N,M,D,P,R,L,Q): ')
    exec_menu(option)


# Use selected option to trigger operations of each Menu Item.
def exec_menu(option):
    clear()
    # The new_user functions will create an auto incrementing key, and iterate through the defined dictionary to append
    # a new record to the dictionary.
    if option.upper() == 'N':
        max_key = new_user.new_key(user_table)  # max_key calculates the next available 'key' value from the user dict.
        add_user = new_user.user_add_loop(new_user.userinfo, "New Employee")  # add_user calls New User for User values.
        user_table[max_key] = add_user  # Commits the User to the Dictionary in Memory
        add_payroll = new_user.user_add_loop(new_user.payroll, "New Payroll") # add_payroll calls New User for Payroll values.
        payroll_table[max_key] = add_payroll  # Commits the Payroll values to the Dictionary in Memory
        write_file.write_file(user_table, payroll_table, fiscal_table)  # Commits the Dictionaries in Memory to File.
        '''
        for key in add_user:
            add_user[key] = ''
        for key in add_payroll:
            add_payroll[key] = ''
        '''
        main_menu()

    elif option.upper() == 'M':
        # The Modify function will load an existing nested dictionary into memory and allow values to be updated.
        open_dict()  # Reloads dict from file, in the event subsequent routines have left a stale version in Memory
        selected_user = search_user.search_menu(user_table)  # Uses the search_user function to define the key to load.
        user = user_table.get(selected_user)  # Gets the User dictionary values for User Key above.
        payroll = payroll_table.get(selected_user)  # Gets the Payroll dictionary values for User Key above.
        mod_user.mod_menu(user)  # Iterates through existing User values to allow changes
        mod_user.mod_menu(payroll)  # Iterates through existing Payroll values to allow changes
        write_file.write_file(user_table, payroll_table, fiscal_table)  # Commits the Dictionaries in Memory to File.
        main_menu()

    elif option.upper() == 'R':
        # The Search and Display Records will initiate a Search routine and return any values that match
        # the defined search criteria.
        open_dict()  # Reloads dict from file, in the event subsequent routines have left a stale version in Memory
        selected_user = search_user.search_menu(user_table)
        user = user_table.get(selected_user)
        payroll = payroll_table.get(selected_user)
        fiscal = fiscal_table.get(selected_user)
        search_user.output_results(user, payroll, fiscal)
        print()
        input("Press Enter to Continue back to Main Menu")
        main_menu()

    elif option.upper() == 'D':
        # Uses a Dictionary Delete function to remove values, or will permit a user to set values to Removed, to avoid
        # new Payslips being generated for a user.
        open_dict()
        selected_user = search_user.search_menu(user_table)
        user = user_table.get(selected_user)
        del_user.delete_action(user, selected_user, user_table, payroll_table, fiscal_table)

    elif option.upper() == 'P':
        # Payslip functionality will load a record and allow for the creation of a new Payslip before exporting and
        # writing to file.
        open_dict()
        selected_user = search_user.search_menu(user_table)
        user = user_table.get(selected_user)
        if user['Removed'].upper() == 'Y':  # IF statement for handling Removed users.
            input('This User has been Removed - Enter Valid User or Reactivate User')
        else:  # Execute the print_pay functions to create Pay Slip.
            user = user_table.get(selected_user)
            payroll = payroll_table.get(selected_user)
            fiscal_data = print_pay.print_menu(selected_user, user, payroll, print_pay.fiscalinfo)
            fiscal_key = print_pay.fiscal_key(fiscal_table, selected_user)
            fiscal_table[selected_user][fiscal_key] = fiscal_data
            write_file.write_file(user_table, payroll_table, fiscal_table)
        main_menu()

    elif option.upper() == 'L':
        # Returns a tabulated list of all the user data.
        open_dict()
        users = list_users.flatten_dict_with_parent(user_table)
        list_users.list_menu(users)  # Call function to list all users.

    elif option.upper() == 'Q':
        # Makes quitting the application safe.
        print("Terminating Session...")
        sleep(2)
        clear()
        menu_objs.quit_menu()
        quit()
    else:
        # Loops the main menu if try catch fails, i.e. if a valid option isn't input.
        main_menu()


# It all starts here, technically, as this is where the Dictionaries are called, followed by the Menu.r
if __name__ == "__main__":
    open_dict()
    main_menu()
