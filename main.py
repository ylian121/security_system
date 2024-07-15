def menu():
    print("Welcome to The GUARDIAN INTERACTIVE SECURITY SYSTEM")




    print("Please set up an ADMIN user profile:")
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    
    print(f"\nUsername: {username}")
    print("Password: " + "*" * len(password))  
    print("Is this correct?")

    print("Type the number 1 for YES or 2 for NO")
    correct = input("Enter number: ")

    if correct == '1':
        print("Perfect!! Welcome to the GISS")

    elif correct == '2':
        print("Sorry about that! Please enter your information again:")
        #create admin menu System. 

menu()