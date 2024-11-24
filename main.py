import subprocess as sp
import pymysql
import pymysql.cursors

def initialize_database_via_connection(con):
    try:
        with open("creator.sql", "r") as file:
            sql_commands = file.read()
            with con.cursor() as cur:
                for command in sql_commands.split(";"):
                    if command.strip():  # Skip empty commands
                        cur.execute(command)
            con.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print("Error initializing database:", e)
        con.rollback()


def viewAllPersons():
    try:
        query = "SELECT * FROM Person"
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Error fetching data:", e)

def addPerson():
    try:
        print("Enter new person's details:")
        nationality = input("Nationality: ")
        nationalID = input("National ID: ")
        password = input("Password: ")
        first = input("First Name: ")
        middle = input("Middle Name: ")
        last = input("Last Name: ")
        dob = input("Date of Birth (YYYY-MM-DD): ")

        query = f"""
        INSERT INTO Person (Nationality, NationalID, Password, FirstName, MiddleName,LastName, DateOfBirth)
        VALUES ('{nationality}', '{nationalID}', '{password}', '{first}', '{middle}', '{last}', '{dob}')
        """
        cur.execute(query)
        con.commit()
        print("Person added successfully.")
    except Exception as e:
        con.rollback()
        print("Failed to add person:", e)

def viewAllBankAccounts():
    try:
        query = "SELECT * FROM BankAccount"
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Error fetching data:", e)

def updateBankBalance():
    try:
        account_number = int(input("Enter Account Number: "))
        new_balance = float(input("Enter New Balance: "))

        query = f"UPDATE BankAccount SET Balance = {new_balance} WHERE AccountNumber = {account_number}"
        cur.execute(query)
        con.commit()
        print("Balance updated successfully.")
    except Exception as e:
        con.rollback()
        print("Failed to update balance:", e)

def deletePerson():
    try:
        nationalID = input("Enter National ID of the person to delete: ")
        query = f"DELETE FROM Person WHERE NationalID = '{nationalID}'"
        cur.execute(query)
        con.commit()
        print("Person deleted successfully.")
    except Exception as e:
        con.rollback()
        print("Failed to delete person:", e)

def chooser(choice):
    if choice == 1:
        viewAllPersons()
    elif choice == 2:
        addPerson()
    elif choice == 3:
        viewAllBankAccounts()
    elif choice == 4:
        updateBankBalance()
    elif choice == 5:
        deletePerson()
    else:
        print("Invalid option.")

while True:
    tmp = sp.call('clear', shell=True)
    username = input("Username: ")
    password = input("Password: ")

    try:
        con = pymysql.connect(
            host='localhost',
            port=3306,
            user=username,
            password=password,
            db='BANK_SYSTEM',
            cursorclass=pymysql.cursors.DictCursor
        )

        if con.open:
            print("Connected to the database.")
        else:
            print("Failed to connect to the database.")

        with con.cursor() as cur:
            initialize_database_via_connection(con)

        tmp = input("Press any key to continue>")

        with con.cursor() as cur:
            while True:
                tmp = sp.call('clear', shell=True)
                print("1. View All Persons")
                print("2. Add a Person")
                print("3. View All Bank Accounts")
                print("4. Update Bank Balance")
                print("5. Delete a Person")
                print("6. Logout")

                choice = int(input("Enter your choice: "))
                tmp = sp.call('clear', shell=True)

                if choice == 6:
                    exit()
                else:
                    chooser(choice)
                    tmp = input("Press any key to continue>")

    except Exception as e:
        print("Connection error:", e)
        tmp = input("Press any key to retry>")
