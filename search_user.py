import main
import list_users
import itertools
from menu_objs import clear, disp_menu

# Menu Name to print to screen
menu_name = 'Employee Search'
# Menu Options is a sub heading that is displayed.
menu_options = 'Enter Employee Name or ID to get Started'


# Extracts the Parent Key for results that match the search values.
def find_parent_keys(nested_dict, search_key, search_value):
    # Creates stack from Nested Dictionary.
    stack = [(nested_dict, [])]
    results = []
    # This splits the values into a tuple of the content and a list of the key. If the search term is then matched
    # against the Key-Value pair, the parent key is appended to the results list.
    while stack:
        current_dict, parents = stack.pop()
        for key, value in current_dict.items():
            if isinstance(value, dict):
                stack.append((value, parents + [key]))
            elif key == search_key[0] and value.lower() == search_value.lower():
                if search_key == [key] and search_value.lower() == value.lower():
                    results.append(parents)
                else:
                    continue

    return results


# Prompts for a Employee Surname or ID
def search_menu(user_table):
    # Clears any defined current_user - for debugging.
    current_users = []
    while True:
        disp_menu(menu_options, menu_name)
        option = input("Enter Name or Employee Number: ")
        if len(option) == 0:
            print("Enter Valid Name or Number")
            continue
        # If value is a numerical value, the value is matched against parent keys on the user table.
        elif option.isdigit():
            if option in user_table:
                matching_keys = user_table[option]
                if isinstance(matching_keys, dict):
                    return option

        # If value is a Alphabetic string, the below method is used.
        elif option.isalpha():
            user_range = []
            # Calling the find_parent_keys function, to search the user_table by surname with the input value.
            values = find_parent_keys(user_table, ["Surname"], option.lower())
            if len(values) == 0:
                continue
            else:
                # flattens the returned values list to a single list instead of a list of lists.
                current_users = list(itertools.chain(*values))
            data = []
            # For returned values, fetch whole record data and append to "data" so it, so it can be called.
            if len(current_users) > 0:
                for user in current_users:
                    user_range = {'Employee Number': str(user)}
                    user_range.update(user_table[user])
                    data.append(user_range)
            # Safe escape if nothing happens to match
            else:
                option = input("No results found - Press Key to Retry or (Q) to Quit")
                if option.upper() == 'Q':
                    main.main_menu()
                else:
                    search_menu(user_table)
            while True:
                # pushes the collated data into a prettytable and prompts for a user to be selected
                # so all user data can be displayed
                if bool(user_range):
                    try:
                        list_users.print_table(data, 'Employee Number')
                        option = input("Select Required User by Employee Number:")
                        if user_range['Employee Number']:
                            matching_keys = option
                            return matching_keys
                    except ValueError:
                        print("Not a valid choice")


# A rather unglamourous method for outputting the returned data (inc. Payslip data) to screen. Its manually wrapped as
# formatting from boxed_msg depended on centering the box and text, whereas we want to make the best use of 80 cols.
def output_results(user, payroll, fiscal):
    clear()
    print()
    # Employee Base Information Block
    header = "+" + "-" * 78 + "+"
    print(header)
    name_print = "     Name: {} {}".format(user['First Name'], user['Surname'])
    phone_print = " Telephone: {}".format(user['Phone Number'])
    print("|{:<39}|{:<38}|".format(name_print, phone_print))

    address_print1 = "  Address: {}".format(user['Address Ln 1'])
    startdate_print = " Start Date: {}".format(user['Start Date'])
    print("|{:<39}|{:<38}|".format(address_print1, startdate_print))

    address_print2 = "           {}".format(user['Address Ln 2'])
    empdesig_print = " Employee Designation: {}".format(user['Employee Designation'])
    print("|{:<39}|{:<38}|".format(address_print2, empdesig_print))

    address_print3 = "     City: {}".format(user['City'])
    empgrade_print = " Employee Grade: {}".format(user['Employee Grade'])
    print("|{:<39}|{:<38}|".format(address_print3, empgrade_print))
    address_print4 = " Postcode: {}".format(user['Postcode'])
    print("|{:<39}|{:<38}|".format(address_print4, ""))
    print(header)
    print("| {:<18}| {:<17}| {:<18}| {:<18}|".format("Employee Loan", "House Allowance",
                                                     "Travel Allowance", "Health Allowance"))
    print("| {:<18}| {:<17}| {:<18}| {:<18}|".format(payroll['Employee Loan'], payroll['House Allowance'],
                                                     payroll['Travel Allowance'], payroll['Health Allowance']))

    # Pay Slip History Information
    print(header)
    if fiscal:
        for rows in fiscal.values():
            for key, value in rows.items():
                if isinstance(value, float):
                    rows[key] = "{:.2f}".format(value)
            print(header)
            print("| {:<76} |".format("Date:" + rows['Date']))
            print(header)
            print("| {:<76} |".format("Allowances:"))
            print(header)
            print("| {:<23} | {:<24} | {:<23} |".format("House", "Travel", "Health"))
            print(header)
            print("| {:<23} | {:<24} | {:<23} |".format(rows['House Allowance'], rows['Travel'], rows['Health']))
            print(header)
            print("| {:<76} |".format("Deductions: "))
            print(header)
            print("| {:<36} | {:<37} |".format("Deductions", "Loan"))
            print(header)
            print("| {:<36} | {:<37} |".format(rows['Deductions'], rows['Loan']))
            print(header)
            print("| {:<76} |".format("Net: "))
            print(header)
            print("| {:<76} |".format(rows['NET']))
            print(header)
            print()
