import mysql.connector
import sys


def login(count):
    count = count + 1
    acc = int(input("Enter account number"))
    pas = input("Enter your password")
    req = f"SELECT * FROM Customers WHERE AccountNumber={acc}"
    cursor.execute(req)
    data = cursor.fetchone()
    if pas == data[4]:
        print(f"Hi {data[1]}!")
        options(data)
    else:
        if count > 2:
            print("Incorrect Password\nTransaction Exited")
            sys.exit()
        print("Incorrect Password!")
        opr = int(input("Press 1 to try again \nAnything else to Exit"))
        if opr == 1 and count <= 3:
            if count == 2:
                print("Warning!!\nLast Attempt")
            login(count)
        else:
            sys.exit()


def withdraw(data):
    amount = int(input("How much amount do you want to withdraw?"))
    if amount <= data[3]:
        balance = data[3] - amount
        print(f"Transaction Successful.\nYour remaining balance is: {balance}")
        req = f"UPDATE Customers SET Balance = {balance} WHERE AccountNumber = {data[0]}"
        cursor.execute(req)
        connect.commit()
    else:
        print("Error!!\nYou don't have enough balance.")
    sys.exit()


def deposit(data):
    amount = int(input("How much money do you want to deposit?"))
    balance: int = data[3] + amount
    print(f"Transaction Successful.\nYour new balance is: {balance}")
    req = f"UPDATE Customers SET Balance = {balance} WHERE AccountNumber = {data[0]}"
    cursor.execute(req)
    connect.commit()
    sys.exit()


def change_password(data):
    newpass = input("Enter a new Password")
    renter = input("Re-enter your Password")
    if newpass == renter:
        req = f"UPDATE Customers SET Password = '{newpass}' WHERE AccountNumber = {data[0]}"
        cursor.execute(req)
        connect.commit()
        print("Password changed successfully\nThanks for the visit")
        sys.exit()
    else:
        print("Password doesn't match")
        change_password(data)


def transfer(data):
    anum = int(input("Enter Account Number"))
    fname = input("Enter Account holder's First name")
    lname = input("Enter Account holder's Last name")
    amount = int(input("Enter amount"))
    if amount <= data[3]:
        req = f" SELECT * FROM Customers WHERE AccountNumber = {anum}"
        cursor.execute(req)
        data2 = cursor.fetchone()
        if fname == data2[1] and lname == data2[2]:
            sbalance = data[3] - amount
            rbalance = data2[3] + amount
            req2 = f"UPDATE Customers SET Balance = {sbalance} WHERE AccountNumber = {data[0]}"
            req3 = f"UPDATE Customers SET balance = {rbalance} WHERE AccountNumber = {data2[0]}"
            cursor.execute(req2)
            cursor.execute(req3)
            connect.commit()
        else:
            print("Entered details are incorrect")
            sys.exit()
    else:
        print("You don't have sufficient balance")
        sys.exit()
    print(f"Remaining Balance is: {sbalance}")
            

def options(data):
    print("What do you want to do:\n"
          "1. Cash Withdraw \n"
          "2. Deposit Money \n"
          "3. Change Password\n"
          "4. Transfer Money")
    opr = int(input())
    if opr == 1:
        withdraw(data)
    if opr == 2:
        deposit(data)
    if opr == 3:
        change_password(data)
    if opr == 4:
        transfer(data)
    else:
        print("Invalid option")


if __name__ == "__main__":
    connect = mysql.connector.connect(host='localhost', database='Bank', user='root', password='root')

    if connect.is_connected():
        print("Welcome to KPCB Bank")
    else:
        print("Unexpected Error")
        sys.exit()
    data: tuple = ()
    cursor = connect.cursor()
    login(0)
