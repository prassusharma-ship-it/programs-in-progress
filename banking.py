from datetime import datetime
import re
import random
import mysql.connector as myconn
mydb = myconn.connect(host="localhost", user="root", password="enter your own passowrd", database="banking")
db_cursor = mydb.cursor()

def create_account():
    Name=input("enter the name")
    todays_date = datetime.now()
    default_pin=random.randint(1000,9999)
    chance1=3
    while chance1>0:
        try:
            Date_of_birth=datetime.strptime(input("enter the date of birth (DD-MM-YYYY): "), "%d-%m-%Y")
            if Date_of_birth < datetime.now():
                print("valid date of birth")
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
    default_account_no=1000000000
    account_no=default_account_no+random.randint(1,999999999)
    chance2=3
    while chance2>0:
        try:
            Phone_no=int(input("enter the phone number"))
            pattern = r'^[6-9]\d{9}$'
            if re.match(pattern, str(Phone_no)):
                print("valid phone number")
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
                print("valid email id")
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
                print("valid aadhar number")
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
                print("valid pan number")
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
                print("you have selected savings account")
                break
            elif Account_type==2:
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
    db_cursor.close()
    mydb.close()

create_account()
