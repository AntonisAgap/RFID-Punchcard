#!/usr/bin/env python

import datetime
import pymongo
import colorama
import sys
from cv2 import *
import termcolor
from termcolor import colored
from pushover import init,Client
import smtplib,ssl
import os
from PyQt5 import QtWidgets
from PyQt5 import QtWidgets, QtGui, QtCore
import base64
from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

myclient = pymongo.MongoClient()
colorama.init()

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
        except:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Wrong Credentials...')

app = QtWidgets.QApplication(sys.argv)

login = Login()
icon = get_tray_icon()
login.setWindowIcon(icon)
login.setFixedSize(300, 250)
if login.exec_() == QtWidgets.QDialog.Accepted:

    mydb = myclient.aqua_storage_db
    employees_collection = mydb.employees_code
    work_log_collection = mydb.work_log_code
    temp_work_log_collection = mydb.temp_work_log_code
    config_collection = mydb.config

    #Load settings for the application
    cursor = config_collection.find({})
    for d in list(cursor):
        send_email = d["send_email"]
        email_receiver = d["email_receiver"]
        send_pushover = d["send_pushover"]
        pushover_token = d["pushover_token"]
        pushover_user_key = d["pushover_user_key"]
        use_webcam = d["use_webcam"]
        webcam_index = d["number_of_webcam"]
        
        webcam_index = int(webcam_index)
        use_webcam = int(use_webcam)
        send_pushover = int(send_pushover)
        send_email = int(send_email)

    path = os.path.dirname(os.path.abspath(__file__))
    path = path+"\img.png"

    #rfid reader object creation
    #creating client to send messages with pushover
    pushover_client = Client(pushover_user_key,api_token=pushover_token)
    #configuring email settings
    port = 587  # For starttls
    smtp_server = ""
    sender_email = ""
    password = ""

    def CheckForCamera():
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
            return index
    
    def GetScreenshot():
        try:
            cam = VideoCapture(0,CAP_DSHOW)
            sleep(0.3)   # 0 -> index of camera
            s, img = cam.read()
            # frame captured without any errors
            imwrite(path,img)
            cam.release()
            destroyAllWindows()
        except Exception as e:
            print(colored("Could\'t capture image...","red"))
            print(e)

    def SendPushover(name,check_string):
        global pushover_client
        pushover_client.send_message(name+" just "+check_string)

    def SendPushover_Screenshot(name,check_string):
        global pushover_client
        with open(path, 'rb') as image:
            pushover_client.send_message(name+" just "+check_string, attachment=image)
        try:
            os.remove(path)
        except:
            print(colored("Error deleting cache...","red")) 

    def SendEmail(name,check_string):
        global port
        global smtp_server
        global sender_email
        global email_receiver

        message = """\

        """+name+""" just """+check_string
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server,port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, email_receiver, message)
            

    def get_code():
        reader = SimpleMFRC522()
        while True:
            try:
                print(colored("Enter your code below: ","yellow"))
                code, _ = reader.read()
                print ("\033[A                             \033[A")
            finally:
                 GPIO.cleanup()
            if code == "":
                print(colored("No code entered","red"))
            else:
                return code

    def get_duration(list_of_tags,value_of_tag):
        times=[]
        for d in list_of_tags:
            if value_of_tag in d.values():
                times.append(d.get("datetime"))
        duration = times[1] - times[0]
        duration = duration.total_seconds() / 3600
        duration = round(duration,2)
        return duration
    
    #function to check how many times a tag exists
    def check_tag_incidents(list_of_tags,value_of_tag):
        count = 0
        t1 = datetime.datetime.now()
        for d in list_of_tags:
            if value_of_tag in d.values():
                count = count + 1
                t1 = d['datetime']
        return count,t1

    def get_name_of_rfid_user(employees,value_of_tag):
        cursor = employees.find({"code": value_of_tag})
        for d in list(cursor):
            name = d["name"]
        return name

    def get_names_of_all_unsaved_users():
        global get_name_of_rfid_user
        global employees_collection
        global temp_work_log_collection
        names = []
        codes = []
        cursor = temp_work_log_collection.find({})
        for d in list(cursor):
            codes.append(d["code"])
        for code_tmp in codes:
            name = get_name_of_rfid_user(employees_collection,code_tmp)
            names.append(name)
        return names



    # Checking for a camera
    if CheckForCamera() == 0:
        use_webcam = 0
    local_tags = []
    if temp_work_log_collection.count_documents({}) > 0:
        while True:
            names = get_names_of_all_unsaved_users()
            print(colored("These users didn't checked out: ","yellow"))
            for name in names:
                print(name)
            answer = input("Do you want to load saved data? (Y/N)")
            if answer == "Y" or answer == "y":
                local_tags = list(temp_work_log_collection.find())
                break
            elif answer == "N" or answer == "n":
                temp_work_log_collection.delete_many({})
                break
            else:
                print(colored("Wrong option...","red"))
    #storing tags to a local list(if=1->1st time entering,if=2->2nd time entering)
    # time a rfid is entered, and delete from db

    # os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        tag = get_code()
        #checking if employee exists
        if employees_collection.count_documents({"code":tag}, limit = 1):
            #if the user exists and its the first time the user scans, welcome the user
            if check_tag_incidents(local_tags,tag)[0] == 0:
                name = get_name_of_rfid_user(employees_collection,tag)
                now = datetime.datetime.now()
                print(colored("Checking in","green")+"("+name+")... "+now.strftime("%H:%M:%S"))
                #creating a dictionary to add
                tmp_dict = {
                    "code" : tag,
                    "datetime" : datetime.datetime.now()
                }
                #Use permission for webcam
                if use_webcam == 1:
                    GetScreenshot()

                local_tags.append(tmp_dict)
                temp_work_log_collection.insert_one(tmp_dict)
                #Use permission for sending e-mail
                if send_email == 1:
                    try:
                        SendEmail(name,"checked in.")
                    except:
                        print(colored("Email wasn't sent","red"))
                #Use permission to send pushover
                if send_pushover == 1:
                    try:
                        #Use permission to send pushover with images
                        if use_webcam == 1:
                            SendPushover_Screenshot(name,"checked in.")
                        else:
                            SendPushover(name,"checked in.")
                    except:
                        print(colored("Pushover wasn't sent","red"))

            elif check_tag_incidents(local_tags,tag)[0] == 1:
                # checking for double checking ins
                time_start = check_tag_incidents(local_tags,tag)[1]
                time_end = datetime.datetime.now()
                timeDiff = time_end - time_start
                if timeDiff.total_seconds() < 30:
                    print("Wait for "+str(round(30 - timeDiff.total_seconds(),2))+" seconds to check out.")
                else: 
                    #TODO: Ask user if he was paid?
                    #if the user scans again, store the data (hours worked etc.) to the db collection
                    name = get_name_of_rfid_user(employees_collection,tag)
                    print(colored("Checking out","red")+"("+name+")...")
                    tmp_dict = {
                        "code" : tag,
                        "datetime" : datetime.datetime.now()
                    }
                    #Use webcam permission
                    if use_webcam == 1:
                        GetScreenshot()
                    local_tags.append(tmp_dict)
                    temp_work_log_collection.insert_one(tmp_dict)
                    #calculate duration time
                    hours_worked = get_duration(local_tags,tag)
                    #inserting the doc in work_log
                    work_log_document = {"name": name,"code" : tag,"hours_worked" : hours_worked, "date" : datetime.datetime.today(), "paid" : 0}
                    work_log_collection.insert_one(work_log_document)
                    #deleting the temporal rfid_tag
                    temp_work_log_collection.delete_many({"code" : tag})
                    for d in reversed(local_tags):
                        if d["code"] == tag:
                            local_tags.remove(d)
                    #Use email permission
                    if send_email == 1:
                        try:
                            SendEmail(name,"checked out.")
                        except:
                            print(colored("Email wasn't sent","red"))
                    #Use pushover permission
                    if send_pushover == 1:
                        try:
                            #Use permission to send image with pushover
                            if use_webcam == 1:
                                SendPushover_Screenshot(name,"checked out.")
                            else:
                                SendPushover(name,"checked out.")
                        except:
                            print(colored("Pushover wasn't sent","red"))
            else:
                #the user scans more than 2 times
                print(colored("Code: "+str(tag)+" has already been stored...","red"))
        else:
            print(colored("Code: "+str(tag)+" doesnt exist in the database...","red"))
