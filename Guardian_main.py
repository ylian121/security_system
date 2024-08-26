#import libraries for UI
from guizero import App, Box, TextBox, Window, Combo, Text, PushButton
#import encryption
import saving_passwords
#import files for voice
from enroll_speaker import enroll_speaker
from recognize_speaker import recognize_speaker
#import files for face
from new_user import capture_new_user, facial_recognition
from faceRec import face_recognition
import cv2
import os
from simple_facerec import SimpleFacerec

class user:
    def __init__(self):
        self.name = ""
        self.userPassword = ""
        self.permission_level = ""

    def set_profile(self, name, password, permission_level):
        self.name = name
        self.permission_level = permission_level
        self.userPassword = password


def ADMIN_menu_SETUP():
   message = Text(app, text="Welcome to the Guardian Interactive Security System!")
   message2 = Text(app, text="Please set up your ADMIN profile to get started:")

   #temp1 = user()

   ADMIN_username = app.question("Please type in a username", "USERNAME: ", initial_value=None)
   ADMIN_password = app.question("Please type in a password", "PASSWORD: ", initial_value=None)
   temp = app.question("Please re-enter your password", "RE-ENTER PASSWORD: ", initial_value=None)

   if temp == ADMIN_password:
   	temp1.set_profile(ADMIN_username, ADMIN_password, 1)
#	return temp1

   else:
#	message3 = Text(app, text="Please retry. The system will turn off now. Start back up the system to try again.")
#	close_gui()
        app.warn("Uh oh!", "You are almost out of biscuits!")

   message3 = Text(app, text="TEMP")

def logout():
    buttonsRESET()
    global button8
    button8 = PushButton(app, command=login, text="LOGIN", width=10,height=3)


def buttonsRESET():
    button1.visible = 0
    button2.visible = 0
    button3.visible = 0
    button4.visible = 0
    button5.visible = 0
    button6.visible = 0
    button7.visible = 0

def close_gui():
  sys.exit()

def say_my_name():
    message2.value = message3.value

def checker(inp, inp2):
    global USER1
    global USER2
    global USER3
    global USER4
    global USER5
    global admin

    if inp == admin.name and inp2 == admin.userPassword:
         print("YUH!")
         return admin
    elif inp == USER1.name and inp2 == USER1.userPassword:
         print("NO!")
         print(USER1.name)
         return USER1
    elif inp == USER2.name and inp2 == USER2.userPassword:
         print(USER2.name)
         return USER2
    elif inp == USER3.name and inp2 == USER3.userPassword:
         return USER3
    elif inp == USER4.name and inp2 == USER4.userPassword:
         return USER4
    elif inp == USER5.name and inp2 == USER5.userPassword:
         return USER5

def login():
    username = app.question("Please type in your username", "USERNAME: ", initial_value=None)
    password = app.question("Please type in your password", "PASSWORD: ", initial_value=None)
   # global temper
   # temper = user()
    temper = checker(username, password)

    if temper.permission_level == "1":
        ADMIN_menu()
    elif temper.permission_level == "2":
        main_menu_2()
    elif temper.permission_level == "3":
        main_menu_3()
    else:
        app.warn("Uh oh!", "That is incorrect. Please retry.")
        return
    button8.visible = 0


def create_new_user():
    global USER1
    global USER2
    global USER3
    global USER4
    global USER5

    x = user()
    x = addNewUser(x)
    if USER1.name == "":
       USER1 = x
    elif USER2.name == "":
       USER2 = x
    elif USER3.name == "":
       USER3 = x
    elif USER4.name == "":
       USER4 = x
    elif USER5.name == "":
       USER5 = x
    else: 
       app.warn("Uh oh!", "Sorry! No more space for new users. Remove a User to be able to add one.")
       return

    print(USER1.name)
    print(USER1.permission_level)

    print(USER2.name)
    print(USER2.permission_level)

#button1 = PushButton(app, command=create_new_user, text="Add a New User", width=10, height=3, visible = 1)

def ADMIN_menu():
     global button2
     global button3
     global button4
     global button5
     global button6
     global button7
     #x = user()
     #xy = user()
     #button1 = PushButton(app, command=addNewUser, text="Add a New User", args = x, width=10,height=3)
     #button1.visible = 1
     #button1 = PushButton(app, command=addNewUser, text="Add a New User", args=(x,), width=10, height=3)
     #xy = x
     global button1
     button1 = PushButton(app, command=create_new_user, text="Add a New User", width=10, height=3, visible = 1)
     #print(xy.name)

     button2 = PushButton(app, command=removeUser, text="Remove a User", width=10,height=3)
     button3 = PushButton(app, command=changePassword, text="Change Password", width=10,height=3)
     button4 = PushButton(app, command=changePermissions, text="Change Permissions", width=10,height=3)
     button5 = PushButton(app, command=ARM, text="ARM GISS", width=10,height=3)
     button6 = PushButton(app, command=DISARM, text="DISARM GISS", width=10,height=3)
     button7 = PushButton(app, command=logout, text="LOGOUT", width=10,height=3)


def main_menu_2(): 
     #button1 = PushButton(app, command=changePassword, text="Change Password", width=10,height=3)
    
     #button2 = PushButton(app, command=ARM, text="ARM GISS", width=10,height=3)
     #button3 = PushButton(app, command=DISARM, text="DISARM GISS", width=10,height=3)
     button3.visible = 1
     button5.visible = 1
     button6.visible = 1
     button7.visible = 1
def main_menu_3():
    # button1 = PushButton(app, command=changePassword, text="Change Password", width=10,height=3)
    button3.visible = 1
    button7.visible = 1
def addNewUser(tempUser):
    # button1.visible = 0
    username = app.question("Please type in a username", "USERNAME: ", initial_value=None)
    password = app.question("Please type in a password", "PASSWORD: ", initial_value=None)
    temp = app.question("Please re-enter your password", "RE-ENTER PASSWORD: ", initial_value=None)
    permLevelNEW = app.question("Please type in a permission level: ", "Permission Level (2 or 3): ", initial_value=None)    
    tempUser = user()

    if temp == password:
        tempUser.set_profile(username, password, permLevelNEW)
    print(tempUser.name)
    enroll_speaker()
    print("Speaker successfully enrolled")
    #app.warn("Speaker enrolled")
    capture_new_user()
    print("User's face enrolled")
    
    return tempUser

    #button2.visible = 0
def removeUser():
    #print("END")
    usernameRemove = app.question("Please type in the username of the user whom you would like to delete: ", "USERNAME: ", initial_value=None)
    if usernameRemove == USER1.name:
        USER1.set_profile("", "", "")
    elif usernameRemove == USER2.name:
        USER2.set_profile("", "", "")
    elif usernameRemove == USER3.name:
        USER3.set_profile("", "", "")
    elif usernameRemove == USER4.name:
        USER4.set_profile("", "", "")
    elif usernameRemove == USER5.name:
        USER5.set_profile("", "", "")
    else: 
        app.warn("Uh oh!", "No Users in system! Unable to Remove")
        return
def changePassword():
   # global temper
   # temper = user()
    typer = user()
    passwordCURRENT = app.question("Please type in your current password", "CURRENT PASSWORD: ", initial_value=None)
   # if temper.userPassword == passwordCURRENT:    
    if passwordCURRENT == admin.userPassword:
        typer = admin
    elif passwordCURRENT == USER1.userPassword:    
        typer = USER1
    elif passwordCURRENT == USER2.userPassword:
        typer = USER2
    elif passwordCURRENT == USER3.userPassword:
        typer = USER3
    elif passwordCURRENT == USER4.userPassword:
        typer = USER4
    elif passwordCURRENT == USER5.userPassword:
        typer = USER5
    else:
        app.warn("Uh oh!", "That is incorrect. Please retry.")
        return
   # else: 
    #        app.warn("Uh oh!", "Warning: attempted to change password of wrong account")
     #       return
    passwordNEW = app.question("Please type in your new password", "NEW PASSWORD: ", initial_value=None)
    passwordREENTER = app.question("Please re-enter your new password", "RE-ENTER NEW PASSWORD: ", initial_value=None)
    if passwordNEW == passwordREENTER:
        if typer == admin: 
           admin.userPassword = passwordNEW
        elif typer == USER1: 
           USER1.userPassword = passwordNEW
        elif typer == USER2:
           USER2.userPassword = passwordNEW
        elif typer == USER3:
           USER3.userPassword = passwordNEW
        elif typer == USER4:
           USER4.userPassword = passwordNEW
        elif typer == USER5:
           USER5.userPassword = passwordNEW

    else: 
       app.warn("Uh oh!", "That is incorrect. Please retry.")
       return

def changePermissions():
    permissionsRemove = app.question("Please type in the username of the user whom you would like to change permissions for: ", "USERNAME: ", initial_value=None)
    if permissionsRemove == USER1.name:
       permissionsNEW = app.question("Please type in the new permission level (2 or 3)", "NEW PERMISSION LEVEL: ", initial_value=None)
       USER1.permission_level = permissionsNEW
    elif permissionsRemove == USER2.name:
       permissionsNEW = app.question("Please type in the new permission level (2 or 3)", "NEW PERMISSION LEVEL: ", initial_value=None)
       USER2.permission_level = permissionsNEW
    elif permissionsRemove == USER3.name:
       permissionsNEW = app.question("Please type in the new permission level (2 or 3)", "NEW PERMISSION LEVEL: ", initial_value=None)
       USER3.permission_level = permissionsNEW
    elif permissionsRemove == USER4.name:
       permissionsNEW = app.question("Please type in the new permission level (2 or 3)", "NEW PERMISSION LEVEL: ", initial_value=None)
       USER4.permission_level = permissionsNEW
    elif permissionsRemove == USER5.name:
       permissionsNEW = app.question("Please type in the new permission level (2 or 3)", "NEW PERMISSION LEVEL: ", initial_value=None)
       USER5.permission_level = permissionsNEW
    else: 
       app.warn("Uh oh!", "That is an invalid username. Please retry.")
       return
def ARM():
    #print("Developing ... REQUIRES FACE ID AND VOICE RECOGNITION")
    app.warn("System armed!")
    recognize_speaker()
    face_recognition()
    '''Outline
    1. log out of their account
    2. turn on face and voice recognition
    3. When system is armed a person is detected:
        1. can we recognize their face?
            yes: no alarm
            no: go to step 2
                2. can we recognize their voice?
                    yes: return to system armed
                    no: set off alarm
                        3. user has 30 seconds to turn off alarm using pincode that will populate the LCD
    4. when the system is disarmed: log in screen populates the LCD
    '''
    
def DISARM():
   # print("Developing ... REQUIRES FACE ID AND VOICE RECOGNITION")
   app.warn("System Successfully Disarmed!")
    '''outline
    1. click diarm button on screen
    2. scan face
    3. if admin or authorized user: keypad will pop up
    4. else set off alarm
    '''
##################################################################
app = App(title="GISS")
message = Text(app, text="Guardian Interactive Security System!")
message2 = Text(app, text="Please set up your ADMIN profile to get started:")
#button1 = PushButton(app, command=addNewUser, text="Add a New User", width=10,height=3, visible =0)

global admin
global USER1
global USER2
global USER3
global USER4
global USER5

admin=user()
USER1 = user()
USER2 = user()
USER3 = user()
USER4 = user()
USER5 = user()

ADMIN_username = app.question("Please type in a username", "USERNAME: ", initial_value=None)
ADMIN_password = app.question("Please type in a password", "PASSWORD: ", initial_value=None)
temp = app.question("Please re-enter your password", "RE-ENTER PASSWORD: ", initial_value=None)

if temp == ADMIN_password:
    admin.set_profile(ADMIN_username, ADMIN_password, "1")
    message3 = Text(app, f"Hi {admin.name}!, Welcome to GISS! For security reasons we will make you login once again.", visible = 0)
    say_my_name()


else:
   # message3 = Text(app, text="Please retry. The system will turn off now. Start back up the system to try again.")
   # close_gui()
    app.warn("Uh oh!", "That is incorrect. Please retry. The system will turn off now. Start back up the system to try again.")

USERNAMELOGIN = app.question("Please type in your username", "USERNAME: ", initial_value=None)
PASSWORDLOGIN = app.question("Please type in a password", "PASSWORD: ", initial_value=None)

temp = checker(USERNAMELOGIN, PASSWORDLOGIN)

if temp.permission_level =="1":
    ADMIN_menu()
"""
elif temp.permission_level == 2:
    main_menu()
"""
#ADMIN_menu_SETUP(admin)

app.display()
