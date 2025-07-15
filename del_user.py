import main
import write_file


# Called by the Delete Menu operation, this allows R or D Inputs to set a user to Removed or to actually Deletes record.
def delete_action(user, selected_user, user_table, payroll_table, fiscal_table):
    option = input("Set this user to (R)emoved or ACTUALLY (D)ELETE"
                   "(DELETION IS NOT RECOVERABLE - or (Q) to Quit) (R/D/Q):")
    while True:
        try:
            if option.upper() == 'R':
                user['Removed'] = 'Y'
                print("Updating Records")
                write_file.write_file(user_table, payroll_table, fiscal_table)
            elif option.upper() == 'D':
                del user_table[selected_user]
                print("User Deleted")
                write_file.write_file(user_table, payroll_table, fiscal_table)
            elif option.upper() == 'Q':
                print("ABORTED")
                main.main_menu()
            main.main_menu()
        except ValueError:
            print("Not a valid option")
