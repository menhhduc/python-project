# Connect to MongoDB and run the GUI

import os
import sys

from frontend.gui import Login, Signup
from frontend.helpers import *
from models import Company, Employee, BenefitPlan, Department
from dotenv import load_dotenv
from database.mongo import employee_repo, benefit_repo, department_repo
import tkinter.messagebox as msgbox

from test.randomize_db import generate_random_data_into_db

load = load_dotenv()

the_company = Company()


def initialize_data():
    os.environ["HRMGR_DB"] = "TRUE"

    if not employee_repo.find({}):
        pass
    else:
        for employee in employee_repo.find({}):
            the_company.employees.append(Employee.parse_obj(employee))

    if not department_repo.find({}):
        pass
    else:
        for department in department_repo.find({}):
            the_company.departments.append(Department.parse_obj(department))

    if not benefit_repo.find({}):
        pass
    else:
        for benefit in benefit_repo.find({}):
            the_company.benefits.append(BenefitPlan.parse_obj(benefit))


def main_gui():
    # client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    # db = client[os.getenv("MONGO_DB")]

    if not os.getenv("MONGO_USER") or not os.getenv("MONGO_PASS") or not os.getenv("MONGO_URI"):
        os.environ["HRMGR_DB"] = "FALSE"
        msgbox.showinfo(
            "Error",
            "It seems like your environment variables are not set up. The program will now run in memory-only mode. Press OK to continue",
            type="ok",
        )
    else:
        initialize_data()

    # ======================
    #  Welcome to the GUI
    # ======================

    # Database newly created
    if len(the_company.employees) == 0:
        msgbox.showinfo("Welcome", "Welcome to HR Manager! It seems like you are new here. Please create an account to get started.", type="ok")
        window1 = Signup(the_company)
        window1.mainloop()

    # Validate the first account
    else:
        first_account_is_admin = the_company.employees[0].is_admin
        first_account_name_is_owner = the_company.employees[0].name == "Owner"
        only_one_owner = len([employee for employee in the_company.employees if employee.name == "Owner"]) == 1
        if not first_account_is_admin:
            msgbox.showerror("Error", "First account is not an admin! Contact the IT department immediately!")
            raise KeyboardInterrupt
        elif not first_account_name_is_owner:
            msgbox.showerror("Error", "First account name is not 'Owner'! Contact the IT department immediately!")
            raise KeyboardInterrupt
        elif not only_one_owner:
            msgbox.showerror("Error", "There are more than one 'Owner' account! Contact the IT department immediately!")
            raise KeyboardInterrupt
        msgbox.showinfo("Welcome", "Welcome back to HR Manager! Please log in to continue.", type="ok")

        if len(the_company.employees) < 10:
            confirm = msgbox.askyesno("Confirm", "Do you want to generate random data into the database?")
            if confirm:
                generate_random_data_into_db()

        window = Login(the_company)
        window.mainloop()


if __name__ == "__main__":
    try:
        main_gui()
    except KeyboardInterrupt:
        sys.exit(0)
    except ValueError as e:
        msgbox.showerror("Error", f"{e}")
