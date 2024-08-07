from gpiozero import LED
from time import sleep
from guizero import App, Box, TextBox, Window, Combo, Text, PushButton
#from tkinter import Spinbox

import sys
import os

# check if 
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

'''import keyring.backend
#from keyring_pass import PasswordStoreBackend
#keyring.set_keyring(PasswordStoreBackend())

class TestKeyring(keyring.backend.KeyringBackend):
    """A test keyring which always outputs same password
    """
    def supported(self): return 0
    def set_password(self, servicename, username, password): return 0
    def get_password(self, servicename, username):
        return "password from TestKeyring"
    def delete_password(self, servicename, username, password): return 0

# set the keyring for keyring lib
import keyring as kr
keyring.set_keyring(TestKeyring())
'''

class user:
    def set_profile(self, name, password, permission_level):
        self.name = name
        self.permission_level = permission_level
        self.userPassword = password

def you_chose(selected_value):
    if selected_value == "Facial ID":
        result.value = "Please stand in front of the camera"
    elif selected.value == "Voice ID":
        result.value = "Please say, 'Hello, I am home!'"
    else:
        result.value = "Please enter your pincode now."


app = App(title="GUI Development")
message = Text(app, text="Welcome to the Guardian Interactive Security System")

def YES():
    message = Text(app, text="Great!")


def NO():
    Admin_menu_SETUP()

#def switch_on():
  #print("ON")

def close_gui():
  sys.exit()
def ADMIN_menu_SETUP():
    print("Welcome to The GUARDIAN INTERACTIVE SECURITY SYSTEM")

    print("Please set up an ADMIN user profile:")
    ADMIN_username = input("Please enter your username: ")
    ADMIN_password = input("Please enter your password: ")


    print(f"\nUsername: {ADMIN_username}")
    print("Password: " + "*" * len(ADMIN_password))
    print("Is this correct?")

    button16 = PushButton(app, command=YES, text="Yes", width=10,height=3)
    button17 = PushButton(app, command=NO, text="No", width=10,height=3, visible=1)
    
    print("Type the number 1 for YES or 2 for NO")
    correct = input("Enter number: ")

    if correct == '1':

        #kr.set_password("GISS", ADMIN_username, ADMIN_password)
        admin.set_profile(ADMIN_username, ADMIN_password, 1)
        print("Perfect!! Welcome to the GISS", admin.name)


    elif correct == '2':
        print("Sorry about that! Please enter your information again:")
        #create admin menu System.

    #return ADMIN_username, ADMIN_password


def ADMIN_menu():
    print("Hello! Please Login if you are the admin")
    #login and verify
    print ("1. Add new user")
    print ("2. Remove a user")
    print ("3. Change Permissions")
    print ("4. Change Password")
    print ("5. CALL OUR HELPLINE")

    AdminInput = input("Enter number: ")

    if AdminInput == '1':
       # addNewUser()
        button6 = PushButton(app, command=addNewUser, text="Add a New User", width=10,height=3)
    elif AdminInput == '2':
       # removeUser()
       button7 = PushButton(app, command=removeUser, text="Remove a User", width=10,height=3)
    elif AdminInput == '3':
        print("Choose a User to change permissions for")
        #Display all users

    elif AdminInput == '4':
       # changePassword()
        button8 = PushButton(app, command=changePassword, text="Add a New User", width=10,height=3)
    if AdminInput == '5':
        print("For additional help please contact our helpline at +1(123)456-789")
        return

def changePassword():
    #pass in password
    print("Warning: If you do not remember your old password, please contact our helpline at +1(123)456-789")
    verifyUsername = input("Please enter your username:")
    OldPassword = input("Please enter your OLD password: ")

    if OldPassword == OldPassword:
        NewPassword = input("Please enter your NEW password: ")
        #store this
        NewPassword2 = input("Please enter your NEW password again: ")

        if NewPassword == NewPassword2:
            #store password
            #kr.delete_password("GISS", verifyUsername, OldPassword)
            #kr.set_password("GISS", verifyUsername, NewPassword2)
            NewPassword2 = NewPassword2
        else:
            print("Sorry. That was incorrect. Please try again.")
            main_menu() #or admin menu



    
def main_menu():
    print("Choose an activity:")

    print("1. Change Password")
    print("2. Arm GISS")
    print("3. Disarm GISS")
    print("4. Access ADMIN Profile")
    print ("5. CALL OUR HELPLINE")


    desiredAction = input("Enter number: ")
#change based off of type of user
    if ((desiredAction == '1') and (admin.permission_level == 1 or admin.permission_level == 2)):
        changePassword()
        main_menu()
    elif ((desiredAction == '1') and (admin.permission_level == 3)):
        print("Permission denied")
        main_menu()
    elif desiredAction == '2':
        ARM_GISS()
    elif desiredAction == '3':
        DISARM_GISS()
    elif ((desiredAction == '4') and (admin.permission_level == 1)):
        ADMIN_menu()
    elif ((desiredAction == '4') and (admin.permission_level == 2 or user.permission_level == 3)):
        print("Permission denied")
        main_menu()
    elif desiredAction == '5':
        print("For additional help please contact our helpline at +1(123)456-789")
        return

    #else:
       # print("ERROR! This function is still being developed. Please try again later!")

def addNewUser():
    userUsername = input("Please enter your username: ")
    userPassword = input("Please enter your password: ")
    #kr.set_password = ("GISS", userUsername, userPassword)
    permission = input("What permission level would you like to grant this user? Press 2 for authorized user or 3 for alternate user")
    newUser = user(userUsername, permission)
    print("User added.")
    main_menu()
#store

def removeUser():
    #pass in username
    userUsername = input("Please enter the username of the profile you would like to delete: ")
    #verify this username exists
    #kr.delete_password("GISS", userUsername)
    print("User removed.")
    main_menu()

def ARM_GISS():
    print("ERROR! This function is still being developed. Please try again later!")
    main_menu()

def DISARM_GISS():
    #ask for username and password
    print("ERROR! This function is still being developed. Please try again later!")
    main_menu()

admin = user()
ADMIN_menu_SETUP()
#main_menu()

instructions = Text(app, text="Choose an identification method")
combo = Combo(app, options=["", "Facial ID", "Voice ID", "Passcode"], command=you_chose)
result = Text(app)

#name = TextBox(app, text="Laura")
#name.tk.config(cursor="target")

button1 = PushButton(app, command=ADMIN_menu, text="Admin Menu", width=10,height=3)
button2 = PushButton(app, command=main_menu, text="Main Menu", width=10,height=3)


#combo = Combo(app, options=["", "tue", "wed","thurs", "fri"])

button5 = PushButton(app, command=close_gui, text="Close", grid=[1,4])

#run_tkinter()
app.display()

