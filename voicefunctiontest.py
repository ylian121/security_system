from voice import enroll_speaker
# from recognize_speaker import recognize_speaker
from voice import delete_speaker
# testing

def main_menu():
    while True:
        print("\nGuardian Interactive Security System")
        print("1. Enroll New Speaker")
        # print("2. Recognize Speaker")
        print("3. Delete speaker")
        print("4. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            print("Starting enrollment process...")
            enroll_speaker()
        # elif choice == '2':
        #     print("Starting recognition process...")
        #     recognize_speaker()
        elif choice == '3':
            print("Delete user.")
            delete_speaker("Briana")
        elif choice == '4':
            print("Exiting system.")
            break
        else:
            print("Invalid choice, please choose again.")

if __name__ == "__main__":
    main_menu()