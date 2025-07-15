import json
import main


# Commit changes to the dictionary from memory to file. Possibly a little volatile, but it works.
def write_file(user_table, payroll_table, fiscal_table):
    new_add = input('Press (S) to Save, Enter for Further Changes or (Q) to Quit (S/Q): ')
    if new_add.upper() == 'S':
        print("Saving...")
        # calls data in. so we update the correct dict with the correct data.
        data = {"user": user_table,
                "payroll": payroll_table,
                "fiscal": fiscal_table,
                }
        # This is the bit that does the actual committing.
        with open("dicts.txt", "w+") as outfile:
            json.dump(data, outfile, indent=4)
            outfile.flush()
    # And the escape case, just in case things aren't right.
    if new_add.upper() == 'Q':
        main.main_menu()
