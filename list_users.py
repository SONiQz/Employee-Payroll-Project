from prettytable import PrettyTable
from menu_objs import clear
import main


# Allow user to select what to order the User by.
def list_menu(users):
    option = input(
        "Sort Data By (E)mployee Number, (F)irst Name, (S)urname, (D)esignation, (G)rade or (Q)uit (E/F/S/D/G/Q): ")
    if option.upper() == 'E':
        print_table(users, 'ID')
    if option.upper() == 'F':
        print_table(users, 'First Name')
    if option.upper() == 'S':
        print_table(users, 'Surname')
    if option.upper() == 'D':
        print_table(users, 'Employee Designation')
    if option.upper() == 'G':
        print_table(users, 'Employee Grade')
    if option.upper() == 'Q':
        main.main_menu()
    else:
        list_menu(users)


# Quicksort function will ascertain whether each value is greater or less than the pivot value.
# This creates new lists and concatenates them before returning to print them.
def quicksort_dict_by_key(current_dict, sort_key):
    if len(current_dict) <= 1:
        return current_dict

    pivot = current_dict[0]
    if sort_key.upper() in ('ID', 'Employee Grade', 'Employee Designation'):
        less = [x for x in current_dict if int(x[sort_key]) < int(pivot[sort_key])]
        equal = [x for x in current_dict if int(x[sort_key]) == int(pivot[sort_key])]
        greater = [x for x in current_dict if int(x[sort_key]) > int(pivot[sort_key])]
    else:
        less = [x for x in current_dict if x[sort_key].lower() < pivot[sort_key].lower()]
        equal = [x for x in current_dict if x[sort_key].lower() == pivot[sort_key].lower()]
        greater = [x for x in current_dict if x[sort_key].lower() > pivot[sort_key].lower()]

    return quicksort_dict_by_key(less, sort_key) + equal + quicksort_dict_by_key(greater, sort_key)


# Function to push the returned values into a PrettyTable - to reduce the amount of manual formatting.
def print_table(data, sort_key=None):
    clear()
    table = PrettyTable()
    sorted_keys = []
    for values in data:
        for k in values:
            if k not in sorted_keys:
                sorted_keys.append(k)
            else:
                continue
    table.field_names = sorted_keys
    if sort_key is not None:
        data = quicksort_dict_by_key(data, sort_key)
    for row in data:
        table.add_row(list(row.values()))
    print(table)


# Is used to flatten the dictionaries as the ID needs to be a value within the dict to parse IDs for sorting without
# multiple passes.
def flatten_dict_with_parent(nested_dict):
    output = []
    for key, value in nested_dict.items():
        items = {'ID': key}
        items.update(value)
        output.append(items)
    return output
