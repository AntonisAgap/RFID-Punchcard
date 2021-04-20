import colorama
from termcolor import colored
import pandas as pd
import datetime
import pymongo
import os
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtWidgets, QtGui, QtCore
import base64
from cv2 import *
colorama.init()
myclient = pymongo.MongoClient()


def get_tray_icon():
        base64_data = '''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'''
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(base64_data))
        icon = QtGui.QIcon(pm)
        return icon

class Login(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        font1 = QtGui.QFont()
        font1.setPointSize(8)
        font2 = QtGui.QFont()
        font2.setPointSize(10)
        self.setWindowTitle("Aqua Manager")
        self.labelName = QtWidgets.QLabel(self)
        self.labelName.setText("Username")
        self.labelName.setFont(font1)
        self.labelName.setGeometry(QtCore.QRect(110, 0, 100, 50))
        self.textName = QtWidgets.QLineEdit(self)
        self.textName.setFont(font2)
        self.labelPass = QtWidgets.QLabel(self)
        self.labelPass.setText("Password")
        self.labelPass.setFont(font1)
        self.labelPass.setGeometry(QtCore.QRect(110, 70, 100, 50))
        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setFont(font2)
        self.textPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)


    def handleLogin(self):
        global myclient
        try:
            connection = ""
            myclient = pymongo.MongoClient(connection)
            myclient.admin.command('ismaster')
            self.accept()
        except Exception as e:
            print(e)
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Wrong Credentials...')

app = QtWidgets.QApplication(sys.argv)

login = Login()
icon = get_tray_icon()
login.setWindowIcon(icon)
login.setFixedSize(300, 250)
if login.exec_() == QtWidgets.QDialog.Accepted:


    #creating connection and defining database and collections
    mydb = myclient.aqua_storage_db
    employees_collection = mydb.employees_code
    work_log_collection = mydb.work_log_code     
    temp_work_log_collection = mydb.temp_work_log_code
    config_collection = mydb.config
    os.system('cls' if os.name == 'nt' else 'clear')


#======= Functions to check Input =================
    def CheckIfInputisNotEmpty(input):
        if input == "":
            print(colored("Nothing was entered...","red"))
            return False
        else:
            return True

    def CheckIfNameExists(input):
        global employees_collection
        cursor = employees_collection.find({"name": input}, {"name": 1}).limit(1)
        return len(list(cursor))

    def CheckIfInputisAnEmail(input):
        if "@" in input:
            return True
        else:
            print(colored("Not a valid e-mail address...","red"))
            return False
#======================================================


    def get_name_of_rfid_user(employees,value_of_tag):
        cursor = employees.find({"code": value_of_tag})
        for d in list(cursor):
            name = d["name"]
        return name


    def give_code():
        code = ""
        while (code==""):
            reader = SimpleMFRC522()
            try:
                print("Give code: ")
                code, _ = reader.read()
            finally:
                GPIO.cleanup()
            print(colored("Code is : ","yellow")+colored(code,"green"))
            input("Press Enter to continue...")
        return code


    def menu():
        print(colored("               Menu                ",attrs=["bold","dark"]))
        print(colored("-----------------------------------","yellow"))
        print(colored("|                                 |","yellow"))
        print(colored("|","yellow") + "1. Insert Employee               "+colored("|","yellow"))
        print(colored("|","yellow") + "2. Delete Employee               "+colored("|","yellow"))
        print(colored("|","yellow") + "3. Edit Employee                 "+colored("|","yellow"))
        print(colored("|","yellow") + "4. Search Employee               "+colored("|","yellow"))
        print(colored("|","yellow") + "5. Pay Employee                  "+colored("|","yellow"))
        print(colored("|","yellow") + "6. Export Data to .xlsx file     "+colored("|","yellow"))
        print(colored("|","yellow") + "7. Settings                      "+colored("|","yellow"))
        print(colored("|","yellow") + "8. "+colored("Live","green")+"                          "+colored("|","yellow"))
        print(colored("|","yellow") + "9. "+colored("Exit","red")+"                          "+colored("|","yellow"))
        print(colored("|                                 |","yellow"))
        print(colored("-----------------------------------","yellow"))
        while True:
            available_options = ["1","2","3","4","5","6","7","8","9","debug"]
            option = input("\nEnter an option: ")
            if option in available_options:
                return option
            else:
                print(colored("Wrong option...","red"))

    def Insert_option():
        global employees_collection
        print("")
        while True:
            print(colored("Insert Employee","yellow",attrs=["bold","dark","underline"]))
            print(("0. "+colored("Back","red")))
            name = input("Enter the name of the employee: ")
            if name == "0":
                return False
            if CheckIfNameExists(name) > 0:
                print(colored("Name already exists in the database...","red"))
            else:
                if CheckIfInputisNotEmpty(name):
                    date_joined = datetime.datetime.now()
                    while True:
                        salary = input("Enter salary per hour: ")
                        if CheckIfInputisNotEmpty(salary):
                            if salary == "0":
                                break
                            code = give_code()
                            print(("Are you sure you want to insert "+name+" with a salary of "+salary+"? ("+colored("Y","green")+"/"+colored("N","red")+")"))
                            confirmation_answer = input("")
                            if (confirmation_answer == "Y" or confirmation_answer == "y"):
                                doc = {"name":name,
                                    "code":code,
                                    "date_joined":date_joined,
                                    "salary":float(salary),
                                    "ownedAmount":0,
                                    "depositDate":datetime.datetime.now()}
                                employees_collection.insert_one(doc)   
                                print(colored("Data inserted successfully...","green")) 
                                input("Press Enter to continue...")
                                os.system('cls' if os.name == 'nt' else 'clear')
                                break
                            else:
                                print(colored("Data wansn't inserted...","red"))
                                input("Press Enter to continue...")
                                os.system('cls' if os.name == 'nt' else 'clear')
                                break


    def Delete_option():
        global employees_collection
        global work_log_collection
        employees_names = []
        cursor = employees_collection.find()
        for d in list(cursor):
            employees_names.append(d["name"])
        try:
            print(colored("Delete Employee","yellow",attrs=["bold","dark","underline"]))
            for name in employees_names:
                print(str(employees_names.index(name))+". "+name)
            print(str(len(employees_names))+". "+colored("Exit","red"))
            option = input("Choose an employee to delete: ")
            if int(option) == len(employees_names):
                return False
            else:
                try:
                    print("Are you sure you want to delete "+employees_names[int(option)]+" from the database? ("+colored("Y","green")+"/"+colored("N","red")+")")
                    confirmation_answer = input("")
                    if confirmation_answer == "Y" or confirmation_answer == "y":
                        work_log_collection.delete_many({"name":employees_names[int(option)]})
                        employees_collection.delete_many({"name":employees_names[int(option)]})
                        print(colored("Employee deleted successfully...","green")) 
                    input("Press Enter to continue...")
                except:
                    print(colored("Wrong option...","red"))
                    input("Press Enter to continue...")
        except:
            print(colored("Wrong option...","red"))
            input("Press Enter to continue...")


    def Edit_option():
        new_name = ''
        flag = 1
        global employees_collection
        global work_log_collection
        while True:
            employees_names = []
            cursor = employees_collection.find()
            for d in list(cursor):
                employees_names.append(d["name"])
            try:
                print(colored("Edit Employee","yellow",attrs=["bold","dark","underline"]))
                for name in employees_names:
                    print(str(employees_names.index(name))+". "+name)
                print(str(len(employees_names))+". "+colored("Exit","red"))
                option = input("Choose an employee to edit: ")
                if int(option) == len(employees_names):
                    return False
                else:
                    while True:
                        try:
                            if flag:
                                cursor = employees_collection.find({"name":employees_names[int(option)]})
                                print(colored("Editing "+employees_names[int(option)],"yellow",attrs=["bold","dark","underline"]))
                            else:
                                cursor = employees_collection.find({"name":new_name})
                                print(colored("Editing "+new_name,"yellow",attrs=["bold","dark","underline"]))
                            for d in list(cursor):
                                id = d["_id"]
                                name = d["name"]
                                code = d["code"]
                                salary = d["salary"]
                            print("1.Name: "+name)
                            print("2.Code: "+str(code))
                            print("3.Salary per hour: "+str(salary))
                            print("4. "+(colored("Back","red")))
                            edit_option = input("Choose an option: ")
                            if edit_option == "1":
                                new_name = input("Enter a name: ")
                                employees_collection.update_one({"_id":id},{"$set":{"name":new_name}})
                                print(colored("Name changed successfully...","green"))
                                input("Press Enter to continue...")
                                flag = 0
                            elif edit_option == "2":
                                new_code = give_code()
                                if new_code:
                                    print(colored("Code changed successfully...","green"))
                                    input("Press Enter to continue...")
                                    employees_collection.update_one({"_id":id},{"$set":{"code":new_code}})
                            elif edit_option == "3":
                                new_salary = input("Enter a salary: ")
                                employees_collection.update_one({"_id":id},{"$set":{"salary":float(new_salary)}})
                                print(colored("Salary changed successfully...","green"))
                                input("Press Enter to continue...")
                            elif edit_option == "4":
                                break
                            else:
                                print(colored("Wrong Option...","red"))
                                input("Press Enter to continue...")
                        except:
                            print(colored("Wrong Option...","red"))
                            input("Press Enter to continue...")
            except:
                print(colored("Wrong Option...","red"))
                input("Press Enter to continue...")




    def Search_option():
        global employees_collection
        global work_log_collection
        employees_names = []
        cursor = employees_collection.find()
        print("")
        try:
            print(colored("Search Employee","yellow",attrs=["bold","dark","underline"]))
            for d in list(cursor):
                employees_names.append(d["name"])
            for name in employees_names:
                print(str(employees_names.index(name))+". "+name)
            print(str(len(employees_names))+". "+colored("Exit","red"))
            option = input("Choose an employee to search: ")
            if int(option) == len(employees_names):
                return False
            else:
                try:
                    #find employee's salary
                    cursor = employees_collection.find({"name":employees_names[int(option)]})
                    for d in list(cursor):
                        salary = d["salary"]
                    paid_days = []
                    non_paid_days = []
                    name = employees_names[int(option)]
                    cursor = work_log_collection.find({"name":name,"paid":1})
                    for d in list(cursor):
                        dict = {"date":d["date"].strftime("%d-%b-%Y"),
                                "salary":d["hours_worked"]*salary}
                        paid_days.append(dict)
                    cursor = work_log_collection.find({"name":name,"paid":0})
                    for d in list(cursor):
                        dict = {"date":d["date"].strftime("%d-%b-%Y"),
                                "salary":d["hours_worked"]*salary}
                        non_paid_days.append(dict)
                    print(colored("-Paid Days-","green",attrs=["bold"]))
                    sum = 0
                    for item in paid_days:
                        item["salary"] = round(item["salary"],2)
                        print("Received ",item["salary"],"€ on "+item["date"])
                        sum = sum + item["salary"]
                    print(colored("Total sum:","green"),round(sum,2),"€")
                    print(colored("-Non-Paid Days-","red",attrs=["bold"]))
                    sum = 0
                    for item in non_paid_days:
                        item["salary"] = round(item["salary"],2)
                        print("Needs to get ",item["salary"],"€ for "+item["date"])
                        sum = sum + item["salary"]
                    print(colored("Total sum:","red"),round(sum,2),"€")
                    input("Press Enter to continue...")  
                except:
                    print(colored("Wrong Option...","red"))
                    input("Press Enter to continue...")
        except:
            print(colored("Wrong Option...","red"))
            input("Press Enter to continue...")

    def Pay_option():
        global employees_collection
        global work_log_collection
        employees_names = []
        cursor = employees_collection.find()
        try:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                all_sum = 0
                # before all true
                print(colored("Loading data...","yellow"))
                employees_names = []
                cursor = employees_collection.find()
                for d in list(cursor):
                    employees_names.append(d["name"])
                names_to_delete = []
                all_days = []
                for name in employees_names:
                    #find employee's salary
                    cursor = employees_collection.find({"name":name})
                    for d in list(cursor):
                        salary = d["salary"]
                        ownedAmount = d["ownedAmount"]
                        depositDate = d["depositDate"].strftime("%d-%b-%Y")
                    non_paid_days = []
                    cursor1 = work_log_collection.find({"name":name,"paid":0})
                    work = list(cursor1)
                    if len(work) != 0:
                        non_paid_days = []
                        id_list = []
                        for d in list(work):
                            id_list = []
                            id_list.append(d["_id"])
                            dict = {"ids":id_list,
                                    "date":d["date"].strftime("%d-%b-%Y"),
                                    "salary":d["hours_worked"]*salary}
                            all_sum = all_sum + d["hours_worked"]*salary
                            non_paid_days.append(dict)
                        # TODO: ----- GROUPING START --------

                        days_to_delete = []
                        for i in range(len(non_paid_days)):
                            for j in range(i+1,len(non_paid_days)):
                                if non_paid_days[i]["date"] == non_paid_days[j]["date"]:
                                    non_paid_days[i]["salary"] = non_paid_days[i]["salary"] + non_paid_days[j]["salary"]
                                    non_paid_days[i]["ids"].append(non_paid_days[j]["ids"][0])
                                    days_to_delete.append(j)
                        # delete duplicate dates
                        days_to_delete = list(dict.fromkeys(days_to_delete))
                        for i in sorted(days_to_delete,reverse=True):
                            del non_paid_days[i]
                        tmp_dict = {"name":name,
                                    "days":non_paid_days,
                                    "sal":salary,
                                    "ownedAmount":ownedAmount,
                                    "depositDate":depositDate}
                        all_days.append(tmp_dict)
                    # else:
                        # employees_collection.update_one({"name":name},{"$set":{"ownedAmount":0}})

                        


                os.system('cls' if os.name == 'nt' else 'clear')
                print("")
                print(colored("Pay Employee","yellow",attrs=["bold","dark","underline"]))
                print(colored("Total Sum: ","blue"),round(all_sum,2),"€")
                for employee_dict in all_days:
                    print(str(all_days.index(employee_dict))+". "+employee_dict["name"])
                print(str(len(all_days))+". "+colored("Exit","red"))
                option = input("Choose an employee to pay: ")
                if int(option) == len(all_days):
                    break
                else:
                    while True:
                        salary_sum = 0 
                        non_paid_days = all_days[int(option)]["days"]
                        st_salary = all_days[int(option)]["sal"]
                        print(colored("-------- ","yellow")+all_days[int(option)]["name"]+"\'s unpaid days"+colored("-----------------","yellow"))
                        for item in non_paid_days:
                            item["salary"] = round(item["salary"],2)
                            salary_sum = salary_sum + item["salary"]
                            print(str(non_paid_days.index(item))+". ",item["salary"],"€ for "+item["date"]+" ("+str(round(item["salary"]/st_salary,2)),"hrs)")
                        print(len(non_paid_days),". "+colored("Total Sum: ","blue"),round(salary_sum,2),"€"+" ("+str(round(salary_sum/st_salary,2)),"hrs)")
                        ownedAmount = all_days[int(option)]["ownedAmount"]
                        depositDate = all_days[int(option)]["depositDate"]
                        print(len(non_paid_days)+1,". "+colored("Add Deposit","blue"))
                        if ownedAmount != 0:
                            print(colored("Deposit: ","green")+str(ownedAmount)+" € "+colored("Total owe: ","red")+str(round(salary_sum-ownedAmount,2))+" € in " + depositDate)
                        print(colored("--------------------------------------------------------","yellow"))
                        print(str(len(non_paid_days)+2)+". "+colored("Back","red"))
                        option2 = input("Choose an option: ")
                        option_list = option2.split(",")
                        break_flag = False
                        total_break_flag = False
                        menu_length = len(non_paid_days)
                        indexes = []
                        for option_ in option_list:
                            if int(option_) == menu_length+2:
                                break_flag = True
                                break
                            elif int(option_) == menu_length+1:
                                amount = int(input("Add amount: "))
                                employees_collection.update_one({"name":all_days[int(option)]["name"]},{"$set":{"ownedAmount":amount}})
                                employees_collection.update_one({"name": name}, {"$set": {"depositDate": datetime.datetime.now()}})
                                break_flag = True
                                break
                            elif int(option_) == menu_length:
                                for item in non_paid_days:
                                    object_ids = item["ids"]
                                    for object_id in object_ids:
                                        work_log_collection.update_one({"_id":object_id},{"$set":{"paid":1}})
                                all_days.remove(all_days[int(option)])
                                employees_collection.update_one({"name":all_days[int(option)]["name"]},{"$set":{"ownedAmount":0}})
                                break_flag = True
                                total_break_flag = True
                                break
                            else:
                                indexes.append(option_)
                                object_ids = non_paid_days[int(option_)]["ids"]
                                for object_id in object_ids:
                                    work_log_collection.update_one({"_id":object_id},{"$set":{"paid":1}})
                                total_break_flag = True
                        if (total_break_flag):
                            for index in sorted(indexes, reverse=True):
                                all_days[int(option)]["days"].remove(all_days[int(option)]["days"][int(index)])
                            if len(all_days[int(option)]["days"]) == 0:
                                employees_collection.update_one({"name":all_days[int(option)]["name"]},{"$set":{"ownedAmount":0}})
                                break_flag = True
                            print(colored("Employee paid successfully...","green"))
                            input("Press Enter to continue...")
                        if (break_flag):
                            break
        except Exception as ex:
            print(colored("Wrong Option...","red"))
            input("Press Enter to continue...")



    def Export_option():
        global employees_collection
        global work_log_collection
        print("")
        print(colored("Export Data","yellow",attrs=["bold","dark","underline"]))
        print("1. Employees data")
        print("2. Work Log data")
        print("3. "+colored("Exit","red"))
        option = input("Choose an option: ")
        if option == "1":
            cursor = employees_collection.find()    
            df =  pd.DataFrame(list(cursor))
            # Delete the _id
            if '_id' in df:
                del df['_id']
            df.to_excel("employees_output.xlsx")
            print(colored("Employees' data exported successfully...","green"))
            input("Press Enter to continue...")
        elif option == "2":
            cursor = work_log_collection.find()    
            df =  pd.DataFrame(list(cursor))
            # Delete the _id
            if '_id' in df:
                del df['_id']
            df.to_excel("work_log_output.xlsx")
            print(colored("Work log data exported successfully...","green"))
            input("Press Enter to continue...")
        elif option == "3":
            return False
        else:
            print("Wrong option")
            input("Press Enter to continue...")



    def Live_option():
        keep_going = True
        global temp_work_log_collection
        global get_name_of_rfid_user
        global employees_collection
        while True:
            offsite_name = []
            codes = []
            all_names = []
            onsite_names = []
            datetime = []
            onsite_sum = 0
            cursor = employees_collection.find({},{"name":1})
            temp_cursor = temp_work_log_collection.find({})
            for d in list(cursor):
                name = d["name"]
                all_names.append(name)
            for d in list(temp_cursor):
                codes.append(d["code"])
                datetime.append(d["datetime"])
                onsite_sum+=1
            print(colored("Onsite","green",attrs=["bold"])+":",colored(onsite_sum,"yellow"))
            for i in range(len(codes)):
                onsite_name= get_name_of_rfid_user(employees_collection,codes[i])
                onsite_names.append(onsite_name)
                print(onsite_name+" ("+datetime[i].strftime("%H:%M:%S")+")")
            offsite_names = list(set(all_names)-set(onsite_names))
            offsite_sum = len(offsite_names)
            print(colored("Offsite","red",attrs=["bold"])+":"+colored(offsite_sum,"yellow"))
            for name in offsite_names:
                print(name)
            print("1. "+colored("Refresh","green"))
            print("2. "+colored("Exit","red"))
            while True:
                option = input("Choose an option: ")
                if option not in ("1","2"):
                    print(colored("Wrong Option","red"))
                if option == "1":
                    break
                if option == "2":
                    return False
            os.system('cls' if os.name == 'nt' else 'clear')
        os.system('cls' if os.name == 'nt' else 'clear')


    def AquaBotSettings_option():
        available_options = ["0","1","2","3","4","5","6"]
        global config_collection
        while True:
            cursor = config_collection.find({})
            for d in list(cursor):
                send_email = d["send_email"]
                email_receiver = d["email_receiver"]
                send_pushover = d["send_pushover"]
                pushover_token = d["pushover_token"]
                pushover_user_key = d["pushover_user_key"]
                use_webcam = d["use_webcam"]
            print(colored("Email Settings","yellow",attrs=["bold","dark","underline"]))
            print(colored("-----------------------------------","green"))
            print("0. Receive e-mail notifications: "+str(send_email))
            print("1. E-mail notification receiver address: "+email_receiver)
            print(colored("Pushover Settings","yellow",attrs=["bold","dark","underline"]))
            print(colored("-----------------------------------","green"))
            print("2. Receive Pushover notifications: "+str(send_pushover))
            print("3. Pushover Token: "+pushover_token)
            print("4. Pushover User key: "+pushover_user_key)
            print(colored("Webcam Settings","yellow",attrs=["bold","dark","underline"]))
            print(colored("-----------------------------------","green"))
            print("5. Webcam usage: "+str(use_webcam))
            print(colored("-----------------------------------","green"))
            print("6. "+colored("Exit","red"))
            option = input("Choose an option to edit: ")
            if option in available_options:
                # E-mail notifications
                if option == "0":
                    print(colored("Send e-mail notifications","yellow",attrs=["bold","dark","underline"]))
                    answer = input("Do you want to receive e-mail notifications? (y/N)")
                    if answer == "y" or answer == "Y":
                        config_collection.update_one({},{"$set":{"send_email":1}})
                        print(colored("E-mail settings updated successfully...","green"))
                        input("Press Enter to continue...")
                    elif answer == "n" or answer == "N":
                        config_collection.update_one({},{"$set":{"send_email":0}})
                        print(colored("E-mail settings updated successfully...","green"))
                        input("Press Enter to continue...")
                    else:
                        print(colored("Wrong option...","red"))
                        input("Press Enter to continue...")
                # E-mail notification address
                if option == "1":
                    print(colored("E-mail notifications receiver address","yellow",attrs=["bold","dark","underline"]))
                    while True:
                        email_answer = input("Enter a valid e-mail address to receive notifications to: ")
                        if CheckIfInputisAnEmail(email_answer):
                            break
                    answer = input("Are you sure you want to use "+colored(email_answer,"red")+ "as a notifications receiver address? (y/N)")
                    if answer == "y" or answer == "Y":
                        config_collection.update_one({},{"$set":{"email_receiver":email_answer}})
                        print(colored("E-mail settings updated successfully...","green"))
                        input("Press Enter to continue...")
                # Pushover notifications
                if option == "2":
                    print(colored("Send Pushover notifications","yellow",attrs=["bold","dark","underline"]))
                    answer = input("Do you want to receive Pushover notifications? (y/N)")
                    if answer == "y" or answer == "Y":
                        config_collection.update_one({},{"$set":{"send_pushover":1}})
                        print(colored("Pushover settings updated successfully...","green"))
                        input("Press Enter to continue...")
                    elif answer == "n" or answer == "N":
                        config_collection.update_one({},{"$set":{"send_pushover":0}})
                        print(colored("Pushover settings updated successfully...","green"))
                        input("Press Enter to continue...")
                    else:
                        print(colored("Wrong option...","red"))
                        input("Press Enter to continue...")
                # Pushover Token
                if option == "3":
                    print(colored("Pushover token","yellow",attrs=["bold","dark","underline"]))
                    token_answer = input("Enter a valid Pushover API token: ")
                    answer = input("Are you sure you want to change the API token to "+colored(token_answer,"red")+ "? (y/N)")
                    if answer == "y" or answer == "Y":
                        config_collection.update_one({},{"$set":{"pushover_token":token_answer}})
                        print(colored("Pushover token settings updated successfully...","green"))
                        input("Press Enter to continue...")
                # Pushover User kEY
                if option == "3":
                    print(colored("Pushover User key","yellow",attrs=["bold","dark","underline"]))
                    user_key_answer = input("Enter a valid Pushover User key: ")
                    answer = input("Are you sure you want to change the User key to "+colored(user_key_answer,"red")+ "? (y/N)")
                    if answer == "y" or answer == "Y":
                        config_collection.update_one({},{"$set":{"pushover_user_key":user_key_answer}})
                        print(colored("Pushover token settings updated successfully...","green"))
                        input("Press Enter to continue...")
                # Webcam usage
                if option == "5":
                    print(colored("Webcam usage","yellow",attrs=["bold","dark","underline"]))
                    answer = input("Do you want to use a webcam? (y/N)")
                    if answer == "y" or answer == "Y":
                        config_collection.update_one({},{"$set":{"use_webcam":1}})
                        print(colored("Webcam settings updated successfully...","green"))
                        input("Press Enter to continue...")
                    elif answer == "n" or answer == "N":
                        config_collection.update_one({},{"$set":{"use_webcam":0}})
                        print(colored("Webcam settings updated successfully...","green"))
                    else:
                        print(colored("Wrong option...","red"))
                        input("Press Enter to continue...")
                if option == "6":
                    return False
            else:
                print(colored("Wrong Option...","red"))
                input("Press Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')

    def Debug_option():
        try:
            global config_collection
            index = 0
            arr = []
            while True:
                cap = VideoCapture(index,CAP_DSHOW)
                if not cap.read()[0]:
                    break
                else:
                    arr.append(index)
                cap.release()
                index += 1
            print(colored("-----------------------------------","green"))
            print(colored("            ΤΕΖΑ (debugging)       ","red"))
            print(colored("-----------------------------------","green"))
            print(colored("List of available webcams: ","yellow"))
            print(arr)
            while True:
                webcam = input("Enter the number of webcam to use (etc 0): ")
                if webcam in str(arr):
                    config_collection.update_one({},{"$set":{"number_of_webcam":int(webcam)}})
                    print(colored("Webcam number set to: ","green")+webcam)
                    input("Press Enter to continue...")
                    return False
                else:
                    print(colored("Wrong choice idiota","red"))
        except Exception as e:
            print(colored("Its worse than we thought","red"))
            print(e)
            input("Press Enter to continue...")
            return False
            


    while True:
        menu_option = menu()
        if menu_option == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            Insert_option()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif menu_option == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            Delete_option()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif menu_option == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            Edit_option()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif menu_option == "4":
            os.system('cls' if os.name == 'nt' else 'clear')
            Search_option()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif menu_option == "5":
            os.system('cls' if os.name == 'nt' else 'clear')
            Pay_option()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif menu_option == "6":
            os.system('cls' if os.name == 'nt' else 'clear')
            Export_option()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif menu_option == "7":
            os.system('cls' if os.name == 'nt' else 'clear')
            AquaBotSettings_option()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif menu_option == "8":
            os.system('cls' if os.name == 'nt' else 'clear')
            Live_option()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif menu_option == "debug":
            os.system('cls' if os.name == 'nt' else 'clear')
            Debug_option()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif menu_option == "9":
            break
        else:
            print(colored("Wrong option","red"))