import subprocess as sp
import pymysql
import pymysql.cursors
import hashlib
import logging
from getpass import getpass
from datetime import datetime
from typing import Optional, Dict, Any
import os
import time

# Configure logging
logging.basicConfig(
    filename='financial_system.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SecurityException(Exception):
    """Custom exception for security-related issues"""
    pass

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, username: str, password: str) -> bool:
        try:
            self.connection = pymysql.connect(
                host='localhost',
                port=3306,
                user=username,
                password=password,
                db='BANK_SYSTEM',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            logging.error(f"Database connection error: {str(e)}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

class SecurityManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """Generate secure hash of password"""
        salt = os.urandom(32)  # Generate a random salt
        return hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode('utf-8'), 
            salt, 
            100000  # Number of iterations
        ).hex()

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        """Verify password against stored hash"""
        return SecurityManager.hash_password(provided_password) == stored_password

class FinancialSystem:
    def __init__(self):
        self.db = DatabaseConnection()
        self.security = SecurityManager()
        self.last_activity = time.time()
        self.SESSION_TIMEOUT = 300  # 5 minutes


    def check_session_timeout(self):
        """Check if session has timed out"""
        if time.time() - self.last_activity > self.SESSION_TIMEOUT:
            raise SecurityException("Session timed out. Please log in again.")
        self.last_activity = time.time()


    def verify_transaction_password(self, national_id: str) -> bool:
        """Verify transaction password for sensitive operations"""
        try:
            self.check_session_timeout()
            query = "SELECT Password FROM Person WHERE NationalID = %s"
            self.db.cursor.execute(query, (national_id,))
            result = self.db.cursor.fetchone()
            
            if not result:
                return False
                
            transaction_password = getpass("Enter transaction password: ")
            return self.security.verify_password(result['Password'], transaction_password)
        except Exception as e:
            logging.error(f"Transaction password verification failed: {str(e)}")
            return False


    def view_all_persons(self):
        """Securely retrieve all persons from database"""
        try:
            self.check_session_timeout()
            query = """
                SELECT NationalID, FirstName, MiddleName, LastName, 
                       DateOfBirth, Nationality 
                FROM Person
            """
            self.db.cursor.execute(query)
            persons = self.db.cursor.fetchall()
            
            if not persons:
                print("No persons found in database.")
                return
                
            for person in persons:
                print(person)
                
        except Exception as e:
            logging.error(f"Error viewing persons: {str(e)}")
            print("An error occurred while retrieving person data.")


    def add_person(self):
        """Securely add new person to database"""
        try:
            self.check_session_timeout()
            print("Enter new person's details:")
            
            # Collect data with input validation
            person_data = {
                'nationality': input("Nationality: ").strip(),
                'national_id': input("National ID: ").strip(),
                'password': self.security.hash_password(getpass("Transaction Password: ")),
                'first_name': input("First Name: ").strip(),
                'middle_name': input("Middle Name: ").strip(),
                'last_name': input("Last Name: ").strip(),
                'dob': None
            }

            # Validate date format
            while True:
                try:
                    dob_input = input("Date of Birth (YYYY-MM-DD): ").strip()
                    person_data['dob'] = datetime.strptime(dob_input, '%Y-%m-%d')
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD")

            query = """
                INSERT INTO Person (
                    Nationality, NationalID, Password, FirstName, 
                    MiddleName, LastName, DateOfBirth
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.db.cursor.execute(query, (
                person_data['nationality'],
                person_data['national_id'],
                person_data['password'],
                person_data['first_name'],
                person_data['middle_name'],
                person_data['last_name'],
                person_data['dob']
            ))
            self.db.connection.commit()
            logging.info(f"New person added: {person_data['national_id']}")
            print("Person added successfully.")
            
        except pymysql.err.IntegrityError:
            self.db.connection.rollback()
            print("Error: National ID already exists.")
            logging.warning(f"Attempted to add duplicate National ID: {person_data['national_id']}")
        except Exception as e:
            self.db.connection.rollback()
            logging.error(f"Error adding person: {str(e)}")
            print("Failed to add person.")


    def make_transaction(self):
        """Process secure financial transaction"""
        try:
            self.check_session_timeout()
            sender_id = input("Enter sender's National ID: ").strip()
            
            if not self.verify_transaction_password(sender_id):
                raise SecurityException("Invalid transaction password.")
                
            receiver_id = input("Enter receiver's National ID: ").strip()
            amount = float(input("Enter amount to transfer: ").strip())
            
            if amount <= 0:
                raise ValueError("Amount must be positive.")

            # Start transaction with proper isolation
            self.db.cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
            self.db.cursor.execute("START TRANSACTION")

            # Check sender's balance with row locking
            self.db.cursor.execute(
                "SELECT Balance FROM BankAccount WHERE OwnerID = %s FOR UPDATE",
                (sender_id,)
            )
            sender_account = self.db.cursor.fetchone()

            if not sender_account or sender_account['Balance'] < amount:
                raise ValueError("Insufficient funds or invalid account.")

            # Perform transfer
            update_queries = [
                "UPDATE BankAccount SET Balance = Balance - %s WHERE OwnerID = %s",
                "UPDATE BankAccount SET Balance = Balance + %s WHERE OwnerID = %s"
            ]
            
            for query in update_queries:
                self.db.cursor.execute(query, (amount, sender_id if "- %s" in query else receiver_id))

            # Record transaction
            transaction_query = """
                INSERT INTO Transactions (
                    SenderID, ReceiverID, Amount, TransactionDate, Status
                ) VALUES (%s, %s, %s, NOW(), 'COMPLETED')
            """
            self.db.cursor.execute(transaction_query, (sender_id, receiver_id, amount))

            self.db.connection.commit()
            logging.info(f"Transaction completed: {sender_id} -> {receiver_id}, Amount: {amount}")
            print("Transaction completed successfully.")
            
        except SecurityException as se:
            self.db.connection.rollback()
            logging.warning(f"Security violation in transaction: {str(se)}")
            print(f"Security Error: {str(se)}")
        except Exception as e:
            self.db.connection.rollback()
            logging.error(f"Transaction failed: {str(e)}")
            print("Transaction failed. Please try again.")


    def view_account_details(self):
        """View details of a specific bank account"""
        try:
            self.check_session_timeout()
            account_number = input("Enter Account Number: ").strip()
            
            query = """
                SELECT ba.*, p.FirstName, p.LastName
                FROM BankAccount ba
                JOIN Person p ON ba.User_Nationality = p.Nationality 
                    AND ba.User_NationalID = p.NationalID
                WHERE ba.AccountNumber = %s
            """
            self.db.cursor.execute(query, (account_number,))
            account = self.db.cursor.fetchone()
            
            if account:
                print("\nAccount Details:")
                print(f"Account Number: {account['AccountNumber']}")
                print(f"Account Holder: {account['FirstName']} {account['LastName']}")
                print(f"Balance: ${account['Balance']:.2f}")
                print(f"Creation Date: {account['CreationDate']}")
            else:
                print("Account not found.")
                
        except Exception as e:
            logging.error(f"Error viewing account details: {str(e)}")
            print("Failed to retrieve account details.")


    def view_transaction_history(self):
        """View transaction history for an account"""
        try:
            self.check_session_timeout()
            account_number = input("Enter Account Number: ").strip()
            
            query = """
                SELECT * FROM Transaction 
                WHERE SenderAccNum = %s OR ReceiverAccNum = %s
                ORDER BY TransactionDate DESC, TransactionTime DESC
            """
            self.db.cursor.execute(query, (account_number, account_number))
            transactions = self.db.cursor.fetchall()
            
            if transactions:
                print("\nTransaction History:")
                for trans in transactions:
                    print(f"\nTransaction ID: {trans['TransactionID']}")
                    print(f"Date: {trans['TransactionDate']} {trans['TransactionTime']}")
                    print(f"Amount: ${trans['Amount']:.2f}")
                    print(f"{'Sent to' if trans['SenderAccNum'] == int(account_number) else 'Received from'}: "
                        f"Account #{trans['ReceiverAccNum'] if trans['SenderAccNum'] == int(account_number) else trans['SenderAccNum']}")
            else:
                print("No transactions found.")
                
        except Exception as e:
            logging.error(f"Error viewing transaction history: {str(e)}")
            print("Failed to retrieve transaction history.")


    def view_savings_goals(self):
        """View savings goals for a user"""
        try:
            self.check_session_timeout()
            nationality = input("Enter Nationality: ").strip()
            national_id = input("Enter National ID: ").strip()
            
            query = """
                SELECT * FROM SavingsGoals
                WHERE User_Nationality = %s AND User_NationalID = %s
            """
            self.db.cursor.execute(query, (nationality, national_id))
            goals = self.db.cursor.fetchall()
            
            if goals:
                print("\nSavings Goals:")
                for goal in goals:
                    progress = (goal['CurrentSaving'] / goal['TargetAmount']) * 100
                    print(f"\nGoal: {goal['GoalName']}")
                    print(f"Target: ${goal['TargetAmount']:.2f}")
                    print(f"Current: ${goal['CurrentSaving']:.2f}")
                    print(f"Progress: {progress:.1f}%")
                    print(f"Deadline: {goal['DeadlineDate']} {goal['DeadlineTime']}")
            else:
                print("No savings goals found.")
                
        except Exception as e:
            logging.error(f"Error viewing savings goals: {str(e)}")
            print("Failed to retrieve savings goals.")


    def view_budgets(self):
        """View budgets for a user"""
        try:
            self.check_session_timeout()
            nationality = input("Enter Nationality: ").strip()
            national_id = input("Enter National ID: ").strip()
            
            query = """
                SELECT * FROM Budgets
                WHERE User_Nationality = %s AND User_NationalID = %s
            """
            self.db.cursor.execute(query, (nationality, national_id))
            budgets = self.db.cursor.fetchall()
            
            if budgets:
                print("\nBudgets:")
                for budget in budgets:
                    usage = (budget['CurrentExpend'] / budget['BudgetLimit']) * 100
                    print(f"\nCategory: {budget['Category']}")
                    print(f"Limit: ${budget['BudgetLimit']:.2f}")
                    print(f"Spent: ${budget['CurrentExpend']:.2f}")
                    print(f"Usage: {usage:.1f}%")
                    print(f"Duration until: {budget['DurationDate']} {budget['DurationTime']}")
            else:
                print("No budgets found.")
                
        except Exception as e:
            logging.error(f"Error viewing budgets: {str(e)}")
            print("Failed to retrieve budgets.")

def main():
    financial_system = FinancialSystem()

    print("""



░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓███████▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░  
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░░▒▓██████▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
                                                                                                                             
                                                                                                                            


        """)
    
    while True:
        try:
            sp.call('clear', shell=True)
            username = input("Username: ").strip()
            password = getpass("Password: ")

            if financial_system.db.connect(username, password):
                print("Connected to the database.")
                
                while True:
                    try:
                        financial_system.check_session_timeout()
                        
                        print("\n1. View All Persons")
                        print("2. Add a Person")
                        print("3. Make Transaction")
                        print("4. View Transaction History")
                        print("5. Logout")

                        choice = int(input("\nEnter your choice: ").strip())
                        
                        if choice == 5:
                            financial_system.db.disconnect()
                            print("Logged out successfully.")
                            break
                            
                        # Execute chosen operation
                        operations = {
                            1: financial_system.view_all_persons,
                            2: financial_system.add_person,
                            3: financial_system.make_transaction,
                            4: financial_system.view_transaction_history
                        }
                        
                        if choice in operations:
                            operations[choice]()
                        else:
                            print("Invalid choice.")
                            
                    except ValueError:
                        print("Please enter a valid number.")
                    except SecurityException as se:
                        print(f"Security Error: {str(se)}")
                        break
                    except Exception as e:
                        logging.error(f"Operation error: {str(e)}")
                        print("An error occurred. Please try again.")
                        
            else:
                print("Failed to connect to database. Please check credentials.")
                
        except Exception as e:
            logging.error(f"System error: {str(e)}")
            print("System error occurred. Please try again.")

if __name__ == "__main__":
    main()