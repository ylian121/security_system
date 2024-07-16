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
        print("Perfect!! Welcome to the GISS")

    elif correct == '2':
        print("Sorry about that! Please enter your information again:")
        #create admin menu System. 

def ADMIN_menu():
1. change permissions
2. change password
3. CALL OUR HELPLINE



def main_menu():
    print("Choose an activity:")
    print("1. Add a new user")
    print("2. Remove a user")
    print("3. Arm GISS")
    print("4. Disarm GISS")
    print("5. Access ADMIN Profile")

    desiredAction = input("Enter number: ")

    if desiredAction == '5':
        ADMIN_menu()
    elif desiredAction == '1':
       # ADMIN_menu()
    elif desiredAction == '2':
       # ADMIN_menu()
    elif desiredAction == '3':
       # ADMIN_menu()
    elif desiredAction == '4':
       # ADMIN_menu()


    else:
        print("ERROR! This function is still being developed. Please try again later!")

def addNewUser():



ADMIN_menu_SETUP()
main_menu()