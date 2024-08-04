import connection


# Main Menu
def main_menu():
    while True:
        user_input = input("SYSTEM: Press Enter to Login | Input q to Quit: \n")
        if user_input == "":
            # function call
            user_log_in()
        elif user_input == "q":
            print("SYSTEM: Quitting")
            return
        else:
            print("SYSTEM: Invalid input !")


# Login
def user_log_in():
    while True:
        uId = input("Enter your Account ID: ")
        print("")
        if uId.isdigit():
            query = f"SELECT * FROM `user` WHERE `id`='{uId}'"
            resultset = connection.search(query)

            if len(resultset) == 1:
                password = input("Enter your password: ")
                # function call
                password_verification(uId, password)
            else:
                print("SYSTEM: No account exist with that Account ID !\n")
        else:
            print("SYSTEM: Invalid Account ID !\n")


# Password Check
def password_verification(uId, password):
    while True:
        # Search Query
        query = f"SELECT * FROM `accounts` WHERE `account_id` = '{uId}'"
        resultset = connection.search(query)

        if len(resultset) == 1:
            # accid uid password
            accId = resultset[0][0]  # account_id
            stored_password = resultset[0][2]  # password
            if stored_password == password:
                # function call
                user_screen(accId)
                break
            else:
                print("\nSYSTEM: Wrong password. Please try again !")
                password = input("Password: ")
        else:
            print("\nSYSTEM: Account not found or multiple accounts found !\n")
            break


# Main User Screen
def user_screen(accId):
    # Search Query
    username = connection.search(f"SELECT * FROM `user` WHERE `id`='{accId}'")
    user = username[0][1]
    while True:
        print("\nWelcome to Ami Bank")
        print(f"User:{user}")
        print("What Would You Like To Do?\n")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Transfer Money")
        print("4. Check Your Balance\n")

        operation = input("Enter the operation number : #")
        if operation.isdigit():
            operation = int(operation)
            if operation == 1:
                # function call
                user_deposit_transaction(accId)
            elif operation == 2:
                # function call
                user_withdraw_transaction(accId)
            elif operation == 3:
                # function call
                user_transfer_transaction(accId)
            elif operation == 4:
                # function call
                user_balance_check(accId)
            else:
                print("\nSYSTEM: Enter a Valid Operation Number !")
        else:
            print("\nSYSTEM: Enter a Valid Operation Number !")

# Deposit Transaction
def user_deposit_transaction(accId):
    print("\nMoney Deposit Section")
    print("Enter 0 to go back\n")

    while True:
        deposit = input("How much would you like to deposit: $")
        if deposit.isdigit():
            deposit = int(deposit)
            if deposit == 0:
                # function call
                user_screen(accId)
                break
            else:
                resultset = connection.search(
                    f"SELECT * FROM `balance` WHERE `accId` = '{accId}'"
                )
                balance = resultset[0][1]  # current_balance
                balance = int(balance)

                final_balance = balance + deposit
                transOperation = "Deposit"

                # Update Query
                connection.iud(
                    f"UPDATE `balance` SET `balance`='{final_balance}' WHERE `accId` = '{accId}'"
                )

                # Insert Query
                connection.iud(
                    f"INSERT INTO `transactions` (`accId`,`transOperation`,`amount`) VALUES ('{accId}','{transOperation}','{deposit}')"
                )

                print("\nSYSTEM: Money Deposited Successfully")
                break

        else:
            print("SYSTEM: Enter a valid amount !")


# Withdraw Transaction
def user_withdraw_transaction(accId):
    print("\nMoney Withdraw Section")
    print("Enter 0 to go back\n")

    while True:
        withdraw = input("How much would you like to withdraw: $")
        if withdraw.isdigit():
            withdraw = int(withdraw)
            if withdraw == 0:
                # function call
                user_screen(accId)
                break
            else:
                resultset = connection.search(
                    f"SELECT * FROM `balance` WHERE `accId` = '{accId}'"
                )
                balance = resultset[0][1]
                balance = int(balance)

                final_balance = balance - withdraw
                transOperation = "Withdraw"

                # Update Query
                connection.iud(
                    f"UPDATE `balance` SET `balance`='{final_balance}' WHERE `accId` = '{accId}'"
                )

                # Insert Query
                connection.iud(
                    f"INSERT INTO `transactions` (`accId`,`transOperation`,`amount`) VALUES ('{accId}','{transOperation}','{withdraw}')"
                )

                print("\nSYSTEM: Money withdrawn Successfully")
                break

        else:
            print("SYSTEM: Enter a valid amount")


# Transfer Section
def user_transfer_transaction(accId):
    print("\nMoney Transfer Section")
    print("Enter 0 to go back\n")

    while True:
        recId = input("Enter the receiver account ID: ")
        if recId.isdigit():
            recId = int(recId)
            if recId == 0:
                # function call
                user_screen(accId)
                break
            else:
                if recId == accId:
                    print("\nSYSTEM: You can't send money to yourself.\n")
                else:
                    # Search Query
                    resultset = connection.search(
                        f"SELECT * FROM `accounts` WHERE `account_id` = {recId}"
                    )

                    if resultset:
                        recieverId = resultset[0][0]
                        recieverId = int(recieverId)
                        while True:
                            amount = input("\nHow much do you want to transfer: $")
                            if amount.isdigit():
                                amount = int(amount)

                                # Search Query
                                resultset1 = connection.search(
                                    f"SELECT * FROM `balance` WHERE `accId` = '{accId}'"
                                )

                                # Search Query
                                resultset2 = connection.search(
                                    f"SELECT * FROM `balance` WHERE `accId` = '{recId}'"
                                )

                                # sender_balance
                                sender_balance = int(resultset1[0][1])
                                # receiver_balance
                                receiver_balance = int(resultset2[0][1])

                                sender_final_balance = sender_balance - amount
                                reciever_final_balance = receiver_balance + amount

                                # Update Query
                                connection.iud(
                                    f"UPDATE `balance` SET `balance`='{sender_final_balance}' WHERE `accId` = '{accId}'"
                                )
                                # Update Query
                                connection.iud(
                                    f"UPDATE `balance` SET `balance`='{reciever_final_balance}' WHERE `accId` = '{recId}'"
                                )
                                # Insert Query
                                connection.iud(
                                    f"INSERT INTO `transfers` (`senderId`, `recieverId`, `amount`) VALUES ('{accId}', '{recId}', '{amount}')"
                                )

                                print("\nSYSTEM: Money transferred successfully.")
                                break
                            else:
                                print("SYSTEM: Enter a valid amount!")
                        break
                    else:
                        print("\nSYSTEM: Account ID not found!\n")
        else:
            print("\nSYSTEM: Enter a valid account ID!\n")


def user_balance_check(accId):
    # Search Query
    resultset = connection.search(f"SELECT * FROM `balance` WHERE `accId`='{accId}'")

    balance = resultset[0][1]  # current_balance
    balance = int(balance)
    print(f"\nSYSTEM: Your account balance is: {balance}$")


# Main Method
def main():
    main_menu()


main()
