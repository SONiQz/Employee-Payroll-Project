import io
import contextlib
from menu_objs import disp_menu, check_valid_date
from fpdf import FPDF

lines = []

# Menu Name to Print to Screen
menu_name = 'Print Payslip'

# Dictionary of values to parse for creating Pay Slip.
fiscalinfo = {'Date': '',
              'Days Worked': '',
              'Hours Overtime': '',
              'Basic': '',
              'Loan': '',
              'House Allowance': '',
              'Travel': '',
              'Health': '',
              'Deductions': '',
              'NET': '',
              }


# Define a new nested dictionary index value key, if previous fiscal records don't exist create them and set nested
# key value to 1. Else find the max current value and + 1
def fiscal_key(fiscal_table, selected_user):
    if selected_user not in fiscal_table:
        fiscal_table[selected_user] = {}
    fiscal_dict = fiscal_table[selected_user]
    fiscal_keys = fiscal_dict.keys()
    if fiscal_keys:
        max_key = max(fiscal_keys, key=lambda k: int(k))
        max_key = int(max_key) + 1
    else:
        max_key = 1
    return max_key


# Pretty up the input so it can be displayed to the user whilst inputting the data.
# This allows it to be easily readable.
def print_info(user_info, add_fiscal):
    def print_data(header, curr_user_info, curr_fiscal):
        print(header)
        print(f"|{'Employee Data'.center(78)}|")
        print(header)
        for key, value in curr_user_info.items():
            print("| {:<20} | {:<54}|".format(key, value))
        print(header)
        print(f"|{'Fiscal Data'.center(78)}|")
        print(header)
        for key, value in curr_fiscal.items():
            print("| {:<20} | {:<54}|".format(key, value))
        print(header)

    fiscal_header = "+" + "-" * 78 + "+"
    print_data(fiscal_header, user_info, add_fiscal)
    with io.StringIO() as output_buffer, contextlib.redirect_stdout(output_buffer):
        print(f"{'CT5057 - Payslip'.center(80)}")
        print_data(fiscal_header, user_info, add_fiscal)
        output_string = output_buffer.getvalue()
        new_lines = output_string.strip().split('\n')
    return new_lines


# Create data, so it can be output to PDF using FPDF and define the output filename.
def print_lines(fiscal_lines, add_fiscal, selected_user, user):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font("Courier", size=10)
    for line in fiscal_lines:
        pdf.cell(200, 10, txt=line, ln=1)
    file_date = add_fiscal['Date'].replace('/', '')
    filename = file_date + " - " + str(selected_user) + str(user['Surname']) + str(user['First Name'])
    pdf.output(filename+".pdf")


# Iterate through the fiscalinfo dictionary, whilst prepending values from the employee user table.
def print_menu(selected_user, user, payroll, add_fiscal):
    for key in add_fiscal:
        add_fiscal[key] = ''
    # Backfilling employee information
    surname = str(user['Surname'])
    firstname = str(user['First Name'])
    designation = str(user['Employee Designation'])
    grade = str(user['Employee Grade'])
    user_info = {"Employee ID": selected_user,
                 "Employee Name": surname + ", " + firstname,
                 "Employee Designation": designation,
                 "Employee Grade": grade,
                 }
    disp_menu("", menu_name)
    print_info(user_info, add_fiscal)
    # Iterate through the fiscalinfo dict.
    for key, values in add_fiscal.items():
        if key == 'Date':  # Ensure Date is valid
            new_option = check_valid_date()
            add_fiscal.update({key: new_option})
        # Allow Loan value to be displayed as float to 2 decimal places, adjust payroll loan value based on input value.
        elif key == 'Loan':
            new_option = input(key + ': ')
            add_fiscal['Loan'] = "%.2f" % float(new_option)
            if len(payroll['Employee Loan']) is None:
                payroll.update['Employee Loan'] = "%.2f" % float(add_fiscal['Loan'])
            else:
                current_loan = "%.2f" % float(payroll['Employee Loan'])
                loan_adj = "%.2f" % float(add_fiscal['Loan'])
                current_loan = float(current_loan) + float(loan_adj)
                payroll.update({'Employee Loan': current_loan})
            add_fiscal.update({key: new_option})
        # House Allowance calculation based on basic * percentage stored in payroll data.
        elif key == 'House Allowance':
            add_fiscal['House Allowance'] = "%.2f" % ((float(add_fiscal['Basic'])/100) * float(payroll['House Allowance']))
        # Travel defined as fixed value of 100.
        elif key == 'Travel':
            add_fiscal['Travel'] = '100'
        # Health is basic * percentage from payroll data.
        elif key == 'Health':
            add_fiscal['Health'] = "%.2f" % ((float(add_fiscal['Basic'])/100) * float(payroll['Health Allowance']))
        # Deductions is basic * 0.2 (or 20%)
        elif key == 'Deductions':
            add_fiscal['Deductions'] = "%.2f" % ((float(add_fiscal['Basic'])/100) * 20)
        # NET is Basic, plus Allowances, minus deductions.
        elif key == 'NET':
            add_fiscal['NET'] = "%.2f" % (float(add_fiscal['Basic']) + float(add_fiscal['House Allowance'])
                                          + float(add_fiscal['Travel']) + float(add_fiscal['Health'])
                                          - float(add_fiscal['Deductions']))
        # Catch other values - This shouldn't be reached, but allows debugging without failure if dictionaries are
        # extended.
        else:
            new_option = input(key + ': ')
            if len(new_option) > 0:
                add_fiscal.update({key: new_option})
            else:
                add_fiscal.update({key: '0'})
        disp_menu('', menu_name)
        print_info(user_info, add_fiscal)

    # Allows verification of correct data being input before saving and creating the PDF.
    while True:
        disp_menu('', menu_name)
        print_info(user_info, add_fiscal)
        option = input("Please confirm the above figures are correct (Y/N)")
        if option.upper() == 'Y':
            disp_menu('', menu_name)
            print_info(user_info, add_fiscal)
            print("Generating PDF of Payslip")
            new_lines = print_info(user_info, add_fiscal)
            print_lines(new_lines, add_fiscal, selected_user, user)
            return add_fiscal

        # Bails on operation, not writing any data.
        if option.upper() == 'N':
            print_menu(selected_user, user, payroll, fiscalinfo)
        else:
            input("Invalid Option - Press any key to retry")
