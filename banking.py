from datetime import datetime
import re
import random
import mysql.connector as myconn
mydb = myconn.connect(host="localhost", user="root", password="enter your own password", database="banking")
db_cursor = mydb.cursor()
def main():
    while True:
        print("\nWelcome to the ATM!")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice=int(input("Enter your choice: "))

        if choice==1:
            create_account()
        elif choice==2:
            login()
        elif choice==3:
            print("Thank you for using the ATM. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
def login():
    attempts = 3
    while attempts > 0:
        acc_no = int(input("Enter account number: "))
        pin = int(input("Enter PIN: "))

        query = "SELECT * FROM accounts WHERE account_no=%s AND pin=%s"
        db_cursor.execute(query,(acc_no,pin))
        result = db_cursor.fetchone()
        if result:
            print("Login successful!")
            break
        else:
            attempts -= 1
            print(f"Invalid account number or PIN. {attempts} attempts left.")
    if attempts == 0:
        print("Too many invalid attempts.")
        return
    # ATM MENU
    while True:
        print("\n1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Change PIN")
        print("6. Account Details")
        print("7. Logout")
        try:
            choice=int(input("Enter your choice: "))
        except:
            print("Invalid input")
            continue
        if choice == 1:
            print("Balance:", check_balance(acc_no))
        elif choice == 2:
            deposit_money(acc_no)
        elif choice == 3:
            withdraw_money(acc_no)
        elif choice == 4:
            transfer_money(acc_no)
        elif choice == 5:
            change_pin(acc_no)
        elif choice == 6:
            account_details(acc_no)
        elif choice == 7:
            print("Logging out...")
            break
        else:
            print("Invalid choice")
def check_balance(acc_no):
    query="SELECT balance FROM accounts WHERE account_no=%s"
    db_cursor.execute(query,(acc_no,))
    balance=db_cursor.fetchone()[0]
    return balance
def deposit_money(acc_no):
    attempts=3
    while attempts>0:
        try:
            amount=int(input("Enter amount to deposit: "))
        except:
            print("Invalid input")
            return
        if amount<=0:
            print("Invalid amount.")
        elif amount>1000000:
            print("Amount too large.")
        else:
            query="UPDATE accounts SET balance=balance+%s WHERE account_no=%s"
            db_cursor.execute(query,(amount,acc_no))
            mydb.commit()

            print("Deposit successful")
            print("New balance:", check_balance(acc_no))
            return
        attempts-=1
        print(f"You have {attempts} attempts left")
    print("Too many invalid attempts")
def withdraw_money(acc_no):
    attempts=3

    while attempts>0:
        try:
            amount=int(input("Enter withdraw amount: "))
        except:
            print("Invalid input")
            continue
        balance=check_balance(acc_no)
        if amount<=0:
            print("Invalid amount")
        elif amount>balance:
            print("Insufficient balance")
        else:
            query="UPDATE accounts SET balance=balance-%s WHERE account_no=%s"
            db_cursor.execute(query,(amount,acc_no))
            mydb.commit()

            print("Withdrawal successful")
            print("Remaining balance:", check_balance(acc_no))
            return

        attempts-=1
        print(f"You have {attempts} attempts left")

    print("Too many invalid attempts")
def transfer_money(acc_no):
    receiver_acc_no=int(input("Enter receiver account number: "))

    query="SELECT * FROM accounts WHERE account_no=%s"
    db_cursor.execute(query,(receiver_acc_no,))
    receiver_account=db_cursor.fetchone()

    if not receiver_account:
        print("Receiver account does not exist")
        return
    try:
        amount=int(input("Enter amount to transfer: "))
    except:
        print("Invalid input")
        return

    if amount <= 0:
        print("Invalid amount")
        return


    query="SELECT balance FROM accounts WHERE account_no=%s"
    db_cursor.execute(query,(acc_no,))
    sender_balance=db_cursor.fetchone()[0]

    if amount>sender_balance:
        print("Insufficient balance")
    else:
        query="UPDATE accounts SET balance=balance-%s WHERE account_no=%s"
        db_cursor.execute(query,(amount,acc_no))
        query="UPDATE accounts SET balance=balance+%s WHERE account_no=%s"
        db_cursor.execute(query,(amount,receiver_acc_no))
        mydb.commit()
        print("Transfer successful")
        print("Remaining balance:", check_balance(acc_no))
def change_pin(acc_no):
    new_pin=int(input("Enter new PIN: "))
    confirm_pin=int(input("Confirm new PIN: "))
    if new_pin!=confirm_pin:
        print("PINs do not match")
        return
    elif len(str(new_pin))!=4:
        print("PIN must be 4 digits")
        return
    else:
        query="UPDATE accounts SET pin=%s WHERE account_no=%s"
        db_cursor.execute(query,(new_pin,acc_no))
        mydb.commit()
        print("PIN changed successfully")
def account_details(acc_no):
    query="SELECT * FROM accounts WHERE account_no=%s"
    db_cursor.execute(query,(acc_no,))
    account=db_cursor.fetchone()

    print("Account Details:")
    print(f"Name: {account[0]}")
    print(f"Date of Birth: {account[3]}")
    print(f"Phone Number: {account[5]}")
    print(f"Email ID: {account[6]}")
    print(f"Aadhar Number: {account[7]}")
    print(f"Address: {account[8]}")
    print(f"Balance: {account[9]}")
    print(f"PAN Number: {account[10]}")
    print(f"Debit Card Number: {account[11]}")
    print(f"Debit Card Expiry Date: {account[12]}")
    print(f"IFSC Code: {account[15]}")
    print(f"Account Type: {account[16]}")
    print(f"Branch Name: {account[17]}")
    print(f"Branch Code: {account[18]}")
def create_account():
    Name=input("enter the name")

    todays_date = datetime.now()



    default_pin=random.randint(1000,9999)

    chance1=3
    while chance1>0:
        try:
            Date_of_birth=datetime.strptime(input("enter the date of birth (DD-MM-YYYY): "), "%d-%m-%Y")
            if Date_of_birth < datetime.now():
                break
            else:
                print("invalid date of birth")
        except:
            print("invalid format")
        chance1-=1
        print(f"you have {chance1} chances left")
    if chance1==0:
        print("Too many invalid attempts")
        return

    


    while True:
        account_no=random.randint(1000000000,9999999999)

        query="SELECT account_no FROM accounts WHERE account_no=%s"
        db_cursor.execute(query,(account_no,))

        if not db_cursor.fetchone():
            break




    chance2=3
    while chance2>0:
        try:
            Phone_no=int(input("enter the phone number"))
            pattern = r'^[6-9]\d{9}$'
            if re.match(pattern, str(Phone_no)):
                break
            else:
                print("invalid phone number")
        except:
            print("invalid phone number format")
        chance2-=1
        print(f"you have {chance2} chances left")
    if chance2==0:
        print("Too many invalid attempts")
        return

    
    


    chance3=3
    while chance3>0:
        try:
            Email_id=input("enter the email id")
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(pattern, Email_id):
                break
            else:
                print("invalid email id")
        except:
            print("invalid email id format")
        chance3-=1
        print(f"you have {chance3} chances left")
    if chance3==0:
        print("Too many invalid attempts")
        return
    



    chance4=3
    while chance4>0:
        try:

            aadhar_no=int(input("enter the aadhar number"))
            if len(str(aadhar_no))==12:
                break
            else:
                print("invalid aadhar number")
        except:
            print("invalid aadhar number format")
        chance4-=1
        print(f"you have {chance4} chances left")
    if chance4==0:
        print("Too many invalid attempts")
        return
    



    address=input("enter the address")




    balance=int(input("enter the balance"))





    chance5=3
    while chance5>0:
        try:
            pan_no=input("enter the pan number")
            pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
            if re.match(pattern, pan_no):
                break
            else:
                print("invalid pan number")
        except:
            print("invalid pan number format")
        chance5-=1
        print(f"you have {chance5} chances left")
    if chance5==0:
        print("Too many invalid attempts")
        return

    debit_card_no=random.randint(1000000000000000,9999999999999999)

    expiry_date_debit_card= todays_date.replace(year=todays_date.year+5)
    




    cvv=random.randint(100,999)




    ifsc_code="MEDUINTEL26"




    chance6=3
    while chance6>0:
        try:
            Account_type=int(input("select the account type \n 1.savings account \n 2.current account"))
            if Account_type==1:
                Account_type="Savings"
                print("you have selected savings account")
                break
            elif Account_type==2:
                Account_type="Current"
                print("you have selected current account")
                break
            else:
                print("invalid account type")
        except:
            print("invalid input")
        chance6-=1
        print(f"you have {chance6} chances left")
    if chance6==0:
        print("Too many invalid attempts")
        return

    default_debit_card_pin=random.randint(1000,9999)


    Branch_name="medicaps_university"



    Branch_code="MDU123"




    print("account created successfully")
    print(f"your name is {Name}")
    print(f"today's date is {todays_date}")
    print(f"your date of birth is {Date_of_birth}")
    print(f"your phone number is {Phone_no}")
    print(f"your email id is {Email_id}")
    print(f"your aadhar number is {aadhar_no}")
    print(f"your address is {address}")
    print(f"your balance is {balance}")
    print(f"your pan number is {pan_no}")
    print(f"your debit card number is {debit_card_no}")
    print(f"your debit card expiry date is {expiry_date_debit_card}")
    print(f"your default debit card pin is {default_debit_card_pin} please, remember it for future use")
    print(f"your debit card cvv is {cvv}")
    print(f"your ifsc code is {ifsc_code}")
    print(f"your account type is {Account_type}")
    print(f"your account number is {account_no}")
    print(f"your branch name is {Branch_name}")
    print(f"your branch code is {Branch_code}")
    print(f"your default pin is {default_pin} please, remember it for future use")

    query = """
    INSERT INTO accounts (
        Name,
        todays_date,
        pin,
        Date_of_birth,
        account_no,
        Phone_no,
        Email_id,
        aadhar_no,
        address,
        balance,
        pan_no,
        debit_card_no,
        expiry_date_debit_card,
        cvv,
        debit_card_pin,
        ifsc_code,
        Account_type,
        Branch_name,
        Branch_code
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """
    
    values=(
        Name,
        todays_date,
        default_pin,
        Date_of_birth,
        account_no,
        Phone_no,
        Email_id,
        aadhar_no,
        address,
        balance,
        pan_no,
        debit_card_no,
        expiry_date_debit_card,
        cvv,
        default_debit_card_pin,
        ifsc_code,
        Account_type, 
        Branch_name,
        Branch_code
    )

    db_cursor.execute(query, values)
    mydb.commit()
main()
db_cursor.close()
mydb.close()
print("thank you for using the banking. Goodbye!")
