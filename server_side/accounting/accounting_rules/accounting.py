import sys
import init_tables
import login
def main():
    print("--- Welcome to ACTGen ---")

    isLoggedIn = False
    while True:      
        print("1. Login")
        print("2. Create User")
        print("3. Exit")
        userInput = input("Enter option (1-3):  ")
        
        if not userInput.isdigit():
            print("Please enter a number")
        else:
            userInput = int(userInput)

            options = {
                1: login.login,
                2: login.create_user,
                3: exit_program
            }
            option = options.get(userInput, None) # If invalid option ex: 4

            if option:
                option()
            else: 
                print("Invalid option entered")

def exit_program():
    print("Exiting the program.")
    sys.exit()

"""
Exit the program if this module is not being used as main
"""
if __name__ == "__main__":
    main()
else:
    print("accounting.py should be used as main")
    exit_program()


