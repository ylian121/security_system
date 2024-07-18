import keyring as kr

class user:
    def _init_(self, name, permission_level):
        self.name = name
        self.permission_level = permission_level

def ADMIN_menu_SETUP():
    print("Welcome to The GUARDIAN INTERACTIVE SECURITY SYSTEM")

    print("Please set up an ADMIN user profile:")
    ADMIN_username = input("Please enter your username: ")
    ADMIN_password = input("Please enter your password: ")
    
    print(f"\nUsername: {ADMIN_username}")
    print("Password: " + "*" * len(ADMIN_password))  
    print("Is this correct?")

    print("Type the number 1 for YES or 2 for NO")
    correct = input("Enter number: ")

    if correct == '1':

        kr.set_password("GISS", ADMIN_username, ADMIN_passsword)
        admin = user(ADMIN_username, 1)
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
        addNewUser()
    elif AdminInput == '2':
        removeUser()
    elif AdminInput == '3':
        print("Choose a User to change permissions for")
        #Display all users

    elif AdminInput == '4':
        changePassword()
    if AdminInput == '5':
        print("For additional help please contact our helpline at +1(123)456-789")

def changePassword():
    #pass in password
    print("Warning: If you do not remember your old password, please contact our helpline at +1(123)456-789")
    OldPassword = input("Please enter your OLD password: ")

    if OldPassword == OldPassword:
        NewPassword = input("Please enter your NEW password: ")
        #store this
        NewPassword2 = input("Please enter your NEW password again: ")

        if NewPassword == NewPassword2: 
            #store password
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
    if desiredAction == '1':
        changePassword()
    elif desiredAction == '2':
        ARM_GISS()
    elif desiredAction == '3':
        DISARM_GISS()
    elif desiredAction == '4':
        ADMIN_menu()
    elif desiredAction == '5':
        print("For additional help please contact our helpline at +1(123)456-789")

    #else:
       # print("ERROR! This function is still being developed. Please try again later!")

def addNewUser():
    userUsername = input("Please enter your username: ")
    userPassword = input("Please enter your password: ")
#store

def removeUser():
    #pass in username
    userUsername = input("Please enter the username of the profile you would like to delete: ")
    #verify this username exists

def ARM_GISS():
    print("ERROR! This function is still being developed. Please try again later!")

def DISARM_GISS():
    #ask for username and password
    print("ERROR! This function is still being developed. Please try again later!")

ADMIN_menu_SETUP()
main_menu()