from menu_objs import disp_menu, is_valid_postcode, clear, check_valid_date

menu_name = 'Modify User'

# Similar in operation to creating a new User, however input calls print current values, and only new text/changed
# values are pushed to the data store.
def mod_menu(user_items):
    while True:
        disp_menu(user_items, menu_name)
        for key, value in user_items.items():
            clear()
            disp_menu(user_items, menu_name)
            if key in 'Phone Number':  # for Phone Number only permit integer values.
                while True:
                    new_option = input(key + ': ')
                    if new_option.isdigit():
                        user_items.update({key: new_option})
                        break
                    else:
                        input("Input is invalid. Please try again. - Press Key to Continue")
                        clear()
                        disp_menu(user_items, menu_name)
            elif key in 'Employee Grade':  # For Employee Grade only accept values 1-4 (in int or roman numerals)
                valid_options = ["I", "II", "III", "IV", "1", "2", "3", "4"]
                while True:
                    new_option = input(key + " - Input value Between 1 - 4 (or I - IV)" + ': ')
                    if new_option in valid_options:
                        user_items.update({key: new_option})
                        break
                    else:
                        input("Input is invalid. Please try again. - Press Key to Continue")
                        clear()
                        disp_menu(user_items, menu_name)
            elif key == 'Postcode':  # For postcode, carry out postcode validation
                new_option = is_valid_postcode(value=value)
                user_items.update({key: new_option})
            elif key == 'Start Date':  # For Start Date, validate it is a plausible date.
                new_option = check_valid_date('Mod', value=value)
                user_items.update({key: new_option})
            else:
                new_option = input(key + ' (' + value + '): ')
                if len(new_option) > 0:
                    user_items.update({key: new_option})
                else:
                    pass
        return user_items
