import connection

# Main Menu
def main_menu():
    while True:
        user_input = input("Press Enter to Login | Input q to Quit: ")
        if user_input == "":
            # Prompt the user Login Function
            user_log_in()
        elif user_input == "q":
            print("Quitting")
            return
        else:
            print("Invalid Input")
            
# Login
def user_log_in():
    while True:
        bId = input("Enter your Bank ID: ")
        if bId.isdigit():
            query = f"SELECT * FROM `user` WHERE `id`='{bId}'"
            resultset = connection.search(query)
            
            
            if len(resultset) == 1:
                print("Enter Password")
                password = input("Password: ")
                # Password Verification Function
                password_verification(bId,password)
            else:
                print("Invalid Bank ID or multiple records found.")
        else:
            print("Invalid Bank ID. Please enter a numeric value.")

# Password Check
def password_verification(bId, password):
    while True:
        query = f"SELECT * FROM `accounts` WHERE `account_id` = '{bId}'"
        resultset = connection.search(query)

        if len(resultset) == 1:
            # accid bid password
            accId = resultset[0][0]
            stored_password = resultset[0][2]
            if stored_password == password:
                user_screen(accId)
                break
            else:
                print("Wrong Password. Please try again.")
                password = input("Password: ")
        else:
            print("Account not found or multiple accounts found")
            break

# Main User Screen
def user_screen(accId):
    print("Welcome to Ami Bank")
    print("What Would You Like To Do?")
    print("")    
    print("1. Deposit Money")
    print("2. Withdraw Money")
    print("3. Transfer Money")
    print("4. Check Your Balance")
    
    while True:
        operation = input("Enter the operation number : ")
        if operation.isdigit():
            operation = int(operation)
            if (operation == 1):
                user_deposit_transaction(operation)
            elif (operation == 2):
                print("2")
            elif (operation == 3):
                print("3")
            elif (operation == 4):
                print("4") 
            else:
                print("Enter a Valid Operation")
        else:
            print("Enter a Valid Operation Number")
            operation = input("Enter the operation number : ")
        
# deposit_transaction
def user_deposit_transaction(operation):
    print ("Money Deposit Section")
    print ("Enter 0 to go back")
    
    while True:
        deposit = input("How Much Would You Like To Deposit? :")
            



# Main Method
def main():
    main_menu()

main()