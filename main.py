import logging
import os
import subprocess as sp
import time
from getpass import getpass
import pymysql
import pymysql.cursors

# Configure logging
logging.basicConfig(
    filename='banking_system.log',
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
                db='BankingSystem',
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


class BankingSystem:
    def __init__(self):
        self.db = DatabaseConnection()
        self.last_activity = time.time()
        self.SESSION_TIMEOUT = 300  # 5 minutes

    def check_session_timeout(self):
        if time.time() - self.last_activity > self.SESSION_TIMEOUT:
            raise SecurityException("Session timed out. Please log in again.")
        self.last_activity = time.time()

    # Selection Queries
    def view_user_transactions(self):
        """Retrieve all transactions for a specific user"""
        try:
            nationality = input("Enter user nationality: ").strip()
            national_id = input("Enter national ID: ").strip()

            query = """
                SELECT t1.TransactionID, t2.TransactionDate, t2.TransactionTime, 
                       t2.Amount, ba1.AccountNumber as SenderAccount, 
                       ba2.AccountNumber as ReceiverAccount
                FROM Transaction1 t1
                JOIN Transaction2 t2 ON t1.TransactionID = t2.TransactionID
                JOIN BankAccount ba1 ON t1.SenderAccNum = ba1.AccountNumber
                JOIN BankAccount ba2 ON t1.ReceiverAccNum = ba2.AccountNumber
                WHERE ba1.UserNationality = %s AND ba1.UserNationalID = %s
                   OR ba2.UserNationality = %s AND ba2.UserNationalID = %s
                ORDER BY t2.TransactionDate DESC, t2.TransactionTime DESC
            """
            self.db.cursor.execute(
                query, (nationality, national_id, nationality, national_id))
            transactions = self.db.cursor.fetchall()

            if transactions:
                print("\nTransaction History:")
                for trans in transactions:
                    print(f"\nTransaction ID: {trans['TransactionID']}")
                    print(f"Date: {trans['TransactionDate']} {
                          trans['TransactionTime']}")
                    print(f"Amount: ${trans['Amount']:,.2f}")
                    print(f"From Account: {trans['SenderAccount']}")
                    print(f"To Account: {trans['ReceiverAccount']}")
            else:
                print("\nNo transactions found.")

        except Exception as e:
            logging.error(f"Error viewing transactions: {str(e)}")
            print(f"\nError: {str(e)}")

    def view_branch_accounts(self):
        """Retrieve all accounts under a specific branch"""
        try:
            branch_code = input("Enter branch code: ").strip()
            bank_id = input("Enter bank ID: ").strip()

            query = """
                SELECT ba.AccountNumber, ba.Balance, 
                       p2.First, p2.Middle, p2.Last,
                       p1.Phone, bb1.BranchManagerNationality,
                       p3.First as ManagerFirst, p3.Last as ManagerLast
                FROM BankAccount ba
                JOIN Person1 p1 ON ba.UserNationality = p1.Nationality 
                    AND ba.UserNationalID = p1.NationalID
                JOIN Person2 p2 ON p1.Nationality = p2.Nationality 
                    AND p1.NationalID = p2.NationalID
                JOIN BankBranch1 bb1 ON ba.BranchCode = bb1.BranchCode 
                    AND ba.BankID = bb1.BankID
                JOIN Person2 p3 ON bb1.BranchManagerNationality = p3.Nationality 
                    AND bb1.BranchManagerNationalID = p3.NationalID
                WHERE ba.BranchCode = %s AND ba.BankID = %s
            """
            self.db.cursor.execute(query, (branch_code, bank_id))
            accounts = self.db.cursor.fetchall()

            if accounts:
                print(f"\nAccounts at Branch {branch_code}:")
                for acc in accounts:
                    print(f"\nAccount Number: {acc['AccountNumber']}")
                    print(f"Account Holder: {acc['First']} {
                          acc['Middle'] or ''} {acc['Last']}")
                    print(f"Balance: ${acc['Balance']:,.2f}")
                    print(f"Branch Manager: {acc['ManagerFirst']} {
                          acc['ManagerLast']}")
            else:
                print("\nNo accounts found in this branch.")

        except Exception as e:
            logging.error(f"Error viewing branch accounts: {str(e)}")
            print(f"\nError: {str(e)}")

    # Projection Queries
    def view_high_income_users(self):
        """List users with income above threshold"""
        try:
            threshold = float(input("Enter income threshold: ").strip())

            query = """
                SELECT p2.First, p2.Middle, p2.Last, p1.AnnualIncome, 
                       p1.Nationality, p1.Phone
                FROM Person1 p1
                JOIN Person2 p2 ON p1.Nationality = p2.Nationality 
                    AND p1.NationalID = p2.NationalID
                WHERE p1.AnnualIncome > %s
                ORDER BY p1.AnnualIncome DESC
            """
            self.db.cursor.execute(query, (threshold,))
            users = self.db.cursor.fetchall()

            if users:
                print(f"\nUsers with annual income above ${threshold:,.2f}:")
                for user in users:
                    print(f"\nName: {user['First']} {
                          user['Middle'] or ''} {user['Last']}")
                    print(f"Annual Income: ${user['AnnualIncome']:,.2f}")
                    print(f"Nationality: {user['Nationality']}")
                    print(f"Phone: {user['Phone']}")
            else:
                print("\nNo users found above the specified income threshold.")

        except Exception as e:
            logging.error(f"Error viewing high income users: {str(e)}")
            print(f"\nError: {str(e)}")

    def view_bank_branch_count(self):
        """Retrieve banks and their branch counts"""
        try:
            query = """
                SELECT rb1.BankName, COUNT(bb1.BranchCode) as BranchCount
                FROM RegisteredBank1 rb1
                LEFT JOIN BankBranch1 bb1 ON rb1.BankID = bb1.BankID
                GROUP BY rb1.BankID, rb1.BankName
                ORDER BY BranchCount DESC
            """
            self.db.cursor.execute(query)
            banks = self.db.cursor.fetchall()

            if banks:
                print("\nBank Branch Statistics:")
                for bank in banks:
                    print(f"\nBank: {bank['BankName']}")
                    print(f"Number of Branches: {bank['BranchCount']}")
            else:
                print("\nNo banks found in the system.")

        except Exception as e:
            logging.error(f"Error viewing bank branch counts: {str(e)}")
            print(f"\nError: {str(e)}")

    # Aggregate Functions
    def calculate_user_transactions(self):
        """Calculate sum of transactions for a user in a period"""
        try:
            nationality = input("Enter user nationality: ").strip()
            national_id = input("Enter national ID: ").strip()
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()

            query = """
                SELECT SUM(t2.Amount) as TotalAmount
                FROM Transaction1 t1
                JOIN Transaction2 t2 ON t1.TransactionID = t2.TransactionID
                JOIN BankAccount ba ON t1.SenderAccNum = ba.AccountNumber
                WHERE ba.UserNationality = %s AND ba.UserNationalID = %s
                AND t2.TransactionDate BETWEEN %s AND %s
            """
            self.db.cursor.execute(
                query, (nationality, national_id, start_date, end_date))
            result = self.db.cursor.fetchone()

            print(f"\nTotal transactions between {start_date} and {end_date}:")
            print(f"${result['TotalAmount']:,.2f}" if result['TotalAmount'] else "$0.00")

        except Exception as e:
            logging.error(f"Error calculating user transactions: {str(e)}")
            print(f"\nError: {str(e)}")

    def find_max_balance(self):
        """Find maximum balance across all accounts"""
        try:
            query = """
                SELECT ba.AccountNumber, ba.Balance,
                       p2.First, p2.Middle, p2.Last
                FROM BankAccount ba
                JOIN Person1 p1 ON ba.UserNationality = p1.Nationality 
                    AND ba.UserNationalID = p1.NationalID
                JOIN Person2 p2 ON p1.Nationality = p2.Nationality 
                    AND p1.NationalID = p2.NationalID
                WHERE ba.Balance = (SELECT MAX(Balance) FROM BankAccount)
            """
            self.db.cursor.execute(query)
            account = self.db.cursor.fetchone()

            if account:
                print("\nAccount with Maximum Balance:")
                print(f"Account Number: {account['AccountNumber']}")
                print(f"Holder: {account['First']} {
                      account['Middle'] or ''} {account['Last']}")
                print(f"Balance: ${account['Balance']:,.2f}")
            else:
                print("\nNo accounts found.")

        except Exception as e:
            logging.error(f"Error finding max balance: {str(e)}")
            print(f"\nError: {str(e)}")

    def get_country_expenditure(self):
        """Calculate average expenditure by country"""
        try:
            query = """
                SELECT Nationality, 
                       AVG(AnnualExpenditure) as AvgExpenditure,
                       COUNT(*) as UserCount
                FROM Person1
                GROUP BY Nationality
                ORDER BY AvgExpenditure DESC
            """
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()

            if results:
                print("\nAverage Annual Expenditure by Country:")
                for result in results:
                    print(f"\nCountry: {result['Nationality']}")
                    print(f"Average Expenditure: ${
                          result['AvgExpenditure']:,.2f}")
                    print(f"Number of Users: {result['UserCount']}")
            else:
                print("\nNo expenditure data found.")

        except Exception as e:
            logging.error(f"Error calculating country expenditure: {str(e)}")
            print(f"\nError: {str(e)}")

    # Search Queries
    def search_users(self):
        """Search users by name pattern"""
        try:
            pattern = input("Enter name pattern to search: ").strip()

            query = """
                SELECT p2.First, p2.Middle, p2.Last, 
                       p1.Nationality, p1.Phone, p1.AnnualIncome
                FROM Person2 p2
                JOIN Person1 p1 ON p2.Nationality = p1.Nationality 
                    AND p2.NationalID = p1.NationalID
                WHERE CONCAT(p2.First, ' ', COALESCE(p2.Middle, ''), ' ', p2.Last) 
                    LIKE %s
            """
            self.db.cursor.execute(query, (f"%{pattern}%",))
            users = self.db.cursor.fetchall()

            if users:
                print("\nMatching Users:")
                for user in users:
                    print(f"\nName: {user['First']} {
                          user['Middle'] or ''} {user['Last']}")
                    print(f"Nationality: {user['Nationality']}")
                    print(f"Phone: {user['Phone']}")
                    print(f"Annual Income: ${user['AnnualIncome']:,.2f}")
            else:
                print("\nNo matching users found.")

        except Exception as e:
            logging.error(f"Error searching users: {str(e)}")
            print(f"\nError: {str(e)}")

    def search_banks(self):
        """Search banks by name or branch address"""
        try:
            search_type = input(
                "Search by (1) Bank Name or (2) Branch Address? ").strip()
            pattern = input("Enter search pattern: ").strip()

            if search_type == '1':
                query = """
                    SELECT rb1.BankName, rb2.Country, rb2.Pincode,
                           COUNT(bb1.BranchCode) as BranchCount
                    FROM RegisteredBank1 rb1
                    JOIN RegisteredBank2 rb2 ON rb1.BankID = rb2.BankID
                    LEFT JOIN BankBranch1 bb1 ON rb1.BankID = bb1.BankID
                    WHERE rb1.BankName LIKE %s
                    GROUP BY rb1.BankID, rb1.BankName, rb2.Country, rb2.Pincode
                """
            else:
                query = """
                    SELECT rb1.BankName, l.Country, l.State, l.City, l.Pincode
                    FROM RegisteredBank1 rb1
                    JOIN BankBranch1 bb1 ON rb1.BankID = bb1.BankID
                    JOIN BankBranch2 bb2 ON bb1.BranchCode = bb2.BranchCode 
                        AND bb1.BankID = bb2.BankID
                    JOIN Locations l ON bb2.Country = l.Country 
                        AND bb2.Pincode = l.Pincode
                    WHERE CONCAT(l.City, ' ', l.State, ' ', l.Country) LIKE %s
                """

            self.db.cursor.execute(query, (f"%{pattern}%",))
            results = self.db.cursor.fetchall()

            if results:
                print("\nSearch Results:")
                for result in results:
                    if search_type == '1':
                        print(f"\nBank: {result['BankName']}")
                        print(f"Location: {result['Country']}")
                        print(f"Pincode: {result['Pincode']}")
                        print(f"Number of Branches: {result['BranchCount']}")
                    else:
                        print(f"\nBank: {result['BankName']}")
                        print(f"Address: {result['City']}, {result['State']}")
                        print(f"Country: {result['Country']}")
                        print(f"Pincode: {result['Pincode']}")
            else:
                print("\nNo matching results found.")

        except Exception as e:
            logging.error(f"Error searching banks: {str(e)}")
            print(f"\nError: {str(e)}")

    # Analysis Functions
    def analyze_expenditure_patterns(self):
        """Analyze users with high expenditure relative to income"""
        try:
            percentage = float(
                input("Enter expenditure percentage threshold (e.g., 75): ").strip())
            grouping = input("Group by (1) Country or (2) City? ").strip()

            if grouping == '1':
                query = """
                    SELECT p1.Nationality as Location, 
                           COUNT(*) as UserCount,
                           AVG(p1.AnnualExpenditure/p1.AnnualIncome * 100) as AvgExpendPercent
                    FROM Person1 p1
                    WHERE (p1.AnnualExpenditure/p1.AnnualIncome * 100) > %s
                    GROUP BY p1.Nationality
                    ORDER BY UserCount DESC
                """
                params = (percentage,)
            else:
                query = """
                    SELECT l.City as Location, 
                           COUNT(*) as UserCount,
                           AVG(p1.AnnualExpenditure/p1.AnnualIncome * 100) as AvgExpendPercent
                    FROM Person1 p1
                    JOIN BankAccount ba ON p1.Nationality = ba.UserNationality 
                        AND p1.NationalID = ba.UserNationalID
                    JOIN BankBranch2 bb2 ON ba.BranchCode = bb2.BranchCode 
                        AND ba.BankID = bb2.BankID
                    JOIN Locations l ON bb2.Country = l.Country 
                        AND bb2.Pincode = l.Pincode
                    WHERE (p1.AnnualExpenditure/p1.AnnualIncome * 100) > %s
                    GROUP BY l.City
                    ORDER BY UserCount DESC
                """
                params = (percentage,)

            self.db.cursor.execute(query, params)
            results = self.db.cursor.fetchall()

            if results:
                print(f"\nUsers with expenditure exceeding {
                      percentage}% of income:")
                for result in results:
                    print(f"\nLocation: {result['Location']}")
                    print(f"Number of Users: {result['UserCount']}")
                    print(f"Average Expenditure Percentage: {
                          result['AvgExpendPercent']:.2f}%")
            else:
                print("\nNo users found matching the criteria.")

        except Exception as e:
            logging.error(f"Error analyzing expenditure: {str(e)}")
            print(f"\nError: {str(e)}")

    def analyze_transaction_patterns(self):
        """Analyze transaction patterns for users"""
        try:
            min_transactions = int(
                input("Enter minimum number of transactions: ").strip())
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()

            query = """
                SELECT p2.First, p2.Middle, p2.Last,
                       COUNT(t1.TransactionID) as TransactionCount,
                       SUM(t2.Amount) as TotalAmount,
                       AVG(t2.Amount) as AvgAmount
                FROM Person1 p1
                JOIN Person2 p2 ON p1.Nationality = p2.Nationality 
                    AND p1.NationalID = p2.NationalID
                JOIN BankAccount ba ON p1.Nationality = ba.UserNationality 
                    AND p1.NationalID = ba.UserNationalID
                JOIN Transaction1 t1 ON ba.AccountNumber = t1.SenderAccNum
                JOIN Transaction2 t2 ON t1.TransactionID = t2.TransactionID
                WHERE t2.TransactionDate BETWEEN %s AND %s
                GROUP BY p1.Nationality, p1.NationalID, p2.First, p2.Middle, p2.Last
                HAVING COUNT(t1.TransactionID) >= %s
                ORDER BY TransactionCount DESC
            """
            self.db.cursor.execute(
                query, (start_date, end_date, min_transactions))
            results = self.db.cursor.fetchall()

            if results:
                print(f"\nTransaction Analysis ({start_date} to {end_date}):")
                for result in results:
                    print(f"\nUser: {result['First']} {
                          result['Middle'] or ''} {result['Last']}")
                    print(f"Number of Transactions: {
                          result['TransactionCount']}")
                    print(f"Total Amount: ${result['TotalAmount']:,.2f}")
                    print(f"Average Amount: ${result['AvgAmount']:,.2f}")
            else:
                print("\nNo users found with the specified transaction criteria.")

        except Exception as e:
            logging.error(f"Error analyzing transactions: {str(e)}")
            print(f"\nError: {str(e)}")

    # Modification Functions
    def add_bank_account(self):
        """Add a new bank account for an existing user"""
        try:
            print("\nNew Bank Account Creation")
            nationality = input("Enter user nationality: ").strip()
            national_id = input("Enter national ID: ").strip()

            # Verify user exists
            self.db.cursor.execute("""
                SELECT AnnualIncome FROM Person1 
                WHERE Nationality = %s AND NationalID = %s
            """, (nationality, national_id))
            user = self.db.cursor.fetchone()

            if not user:
                print("\nUser not found.")
                return

            account_type = input(
                "Enter account type (Current/Saving/Salary/Demat/FixedDeposit): ").strip().lower()
            branch_code = input("Enter branch code: ").strip()
            bank_id = input("Enter bank ID: ").strip()
            initial_balance = float(input("Enter initial balance: ").strip())

            # Check minimum balance requirement based on account type
            if account_type == 'current':
                min_balance = float(
                    input("Enter minimum balance requirement: ").strip())
                if initial_balance < min_balance:
                    print(
                        "\nInitial balance does not meet minimum balance requirement.")
                    return

            self.db.cursor.execute("START TRANSACTION")

            # Generate new account number
            self.db.cursor.execute(
                "SELECT MAX(AccountNumber) as max_acc FROM BankAccount")
            result = self.db.cursor.fetchone()
            account_number = (result['max_acc'] or 0) + 1

            # Insert into BankAccount
            self.db.cursor.execute("""
                INSERT INTO BankAccount (
                    AccountNumber, UserNationalID, UserNationality,
                    BranchCode, BankID, Balance, CreationDate
                ) VALUES (%s, %s, %s, %s, %s, %s, CURDATE())
            """, (account_number, national_id, nationality, branch_code, bank_id, initial_balance))

            # Insert into specific account type table
            if account_type == 'current':
                self.db.cursor.execute("""
                    INSERT INTO CurrentAccount (
                        AccountNumber, MinBalance, MonthlyTransactionLimit
                    ) VALUES (%s, %s, %s)
                """, (account_number, min_balance, input("Enter monthly transaction limit: ")))

            elif account_type == 'saving':
                self.db.cursor.execute("""
                    INSERT INTO SavingAccount (
                        AccountNumber, MinBalance, InterestRate, MonthlyWithdrawalLimit
                    ) VALUES (%s, %s, %s, %s)
                """, (
                    account_number,
                    float(input("Enter minimum balance: ")),
                    float(input("Enter interest rate: ")),
                    int(input("Enter monthly withdrawal limit: "))
                ))

            elif account_type == 'salary':
                self.db.cursor.execute("""
                    INSERT INTO SalaryAccount (
                        AccountNumber, OrganisationID, EmployeeID
                    ) VALUES (%s, %s, %s)
                """, (
                    account_number,
                    input("Enter organisation ID: "),
                    input("Enter employee ID: ")
                ))

            elif account_type == 'demat':
                self.db.cursor.execute("""
                    INSERT INTO DematAccount (
                        AccountNumber, DPID, TradingAccountLink, MaintenanceCharges
                    ) VALUES (%s, %s, %s, %s)
                """, (
                    account_number,
                    input("Enter DP ID: "),
                    input("Enter trading account link: "),
                    float(input("Enter maintenance charges: "))
                ))

            elif account_type == 'fixeddeposit':
                self.db.cursor.execute("""
                    INSERT INTO FixedDepositAccount (
                        AccountNumber, LockinPeriod, MaturityDate, PrematurePenalty
                    ) VALUES (%s, %s, %s, %s)
                """, (
                    account_number,
                    input("Enter lock-in period (YYYY-MM-DD): "),
                    input("Enter maturity date (YYYY-MM-DD): "),
                    float(input("Enter premature penalty: "))
                ))

            self.db.connection.commit()
            print(f"\nAccount created successfully! Account Number: {
                  account_number}")

        except Exception as e:
            self.db.connection.rollback()
            logging.error(f"Error creating account: {str(e)}")
            print(f"\nError: {str(e)}")

    def update_budget_limit(self):
        """Update budget limit for a user"""
        try:
            nationality = input("Enter user nationality: ").strip()
            national_id = input("Enter national ID: ").strip()
            category = input("Enter budget category: ").strip()
            new_limit = float(input("Enter new budget limit: ").strip())

            # Verify user and their income
            self.db.cursor.execute("""
                SELECT AnnualIncome FROM Person1 
                WHERE Nationality = %s AND NationalID = %s
            """, (nationality, national_id))
            user = self.db.cursor.fetchone()

            if not user:
                print("\nUser not found.")
                return

            # Check if new limit is reasonable compared to annual income
            if new_limit > user['AnnualIncome']:
                print("\nWarning: Budget limit exceeds annual income!")
                if input("Continue anyway? (y/n): ").lower() != 'y':
                    return

            self.db.cursor.execute("""
                UPDATE Budgets1 
                SET BudgetLimit = %s
                WHERE Category = %s 
                    AND UserNationality = %s 
                    AND UserNationalID = %s
            """, (new_limit, category, nationality, national_id))

            if self.db.cursor.rowcount > 0:
                self.db.connection.commit()
                print("\nBudget limit updated successfully!")
            else:
                print("\nNo matching budget found.")

        except Exception as e:
            self.db.connection.rollback()
            logging.error(f"Error updating budget: {str(e)}")
            print(f"\nError: {str(e)}")

    def remove_expired_goals(self):
        """Remove expired savings goals"""
        try:
            self.db.cursor.execute("START TRANSACTION")

            # Find expired goals
            self.db.cursor.execute("""
                SELECT sg1.GoalName, sg1.UserNationality, sg1.UserNationalID,
                       sg1.TargetAmount, sg1.CurrentSaving, sg2.DeadlineDate
                FROM SavingsGoals1 sg1
                JOIN SavingsGoals2 sg2 ON sg1.GoalName = sg2.GoalName
                    AND sg1.UserNationality = sg2.UserNationality
                    AND sg1.UserNationalID = sg2.UserNationalID
                WHERE sg2.DeadlineDate < CURDATE()
                    AND sg1.CurrentSaving < sg1.TargetAmount
            """)
            expired_goals = self.db.cursor.fetchall()

            if not expired_goals:
                print("\nNo expired goals found.")
                return

            print("\nExpired Goals to be Removed:")
            for goal in expired_goals:
                print(f"\nGoal: {goal['GoalName']}")
                print(f"User: {goal['UserNationality']
                               }-{goal['UserNationalID']}")
                print(f"Target: ${goal['TargetAmount']:,.2f}")
                print(f"Achieved: ${goal['CurrentSaving']:,.2f}")
                print(f"Deadline: {goal['DeadlineDate']}")

            if input("\nProceed with removal? (y/n): ").lower() == 'y':
                for goal in expired_goals:
                    # Remove from SavingsGoals2 first (due to foreign key)
                    self.db.cursor.execute("""
                        DELETE FROM SavingsGoals2
                        WHERE GoalName = %s 
                            AND UserNationality = %s 
                            AND UserNationalID = %s
                    """, (goal['GoalName'], goal['UserNationality'], goal['UserNationalID']))

                    # Then remove from SavingsGoals1
                    self.db.cursor.execute("""
                        DELETE FROM SavingsGoals1
                        WHERE GoalName = %s 
                            AND UserNationality = %s 
                            AND UserNationalID = %s
                    """, (goal['GoalName'], goal['UserNationality'], goal['UserNationalID']))

                self.db.connection.commit()
                print("\nExpired goals removed successfully!")
            else:
                self.db.connection.rollback()
                print("\nOperation cancelled.")

        except Exception as e:
            self.db.connection.rollback()
            logging.error(f"Error removing expired goals: {str(e)}")
            print(f"\nError: {str(e)}")

    def add_person(self):
        """Add a new person to the database"""
        try:
            print("\nAdd New Person")

            # Collect Person1 data
            person_data = {
                'nationality': input("Nationality: ").strip(),
                'national_id': input("National ID: ").strip(),
                'password': input("Password: ").strip(),
                'dob': input("Date of Birth (YYYY-MM-DD): ").strip(),
                'phone': input("Phone Number: ").strip(),
                'annual_income': float(input("Annual Income: ").strip()),
                'annual_expenditure': float(input("Annual Expenditure: ").strip())
            }

            # Optional custodian information
            if input("Does this person need a custodian? (y/n): ").lower() == 'y':
                person_data.update({
                    'custodian_nationality': input("Custodian Nationality: ").strip(),
                    'custodian_national_id': input("Custodian National ID: ").strip()
                })
            else:
                person_data['custodian_nationality'] = None
                person_data['custodian_national_id'] = None

            # Collect Person2 data
            person_data.update({
                'first_name': input("First Name: ").strip(),
                'middle_name': input("Middle Name (or press Enter to skip): ").strip() or None,
                'last_name': input("Last Name: ").strip()
            })

            # Collect Person3 data (email addresses)
            emails = []
            while True:
                email = input(
                    "Enter email address (or press Enter to finish): ").strip()
                if not email:
                    break
                emails.append(email)

            if not emails:
                emails.append(
                    input("At least one email address is required: ").strip())

            # Start transaction
            self.db.cursor.execute("START TRANSACTION")

            # Insert into Person1
            self.db.cursor.execute("""
                INSERT INTO Person1 (
                    Nationality, NationalID, Password, CustodianNationality,
                    CustodianNationalID, DateOfBirth, Phone, 
                    AnnualIncome, AnnualExpenditure
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                person_data['nationality'], person_data['national_id'],
                person_data['password'], person_data['custodian_nationality'],
                person_data['custodian_national_id'], person_data['dob'],
                person_data['phone'], person_data['annual_income'],
                person_data['annual_expenditure']
            ))

            # Insert into Person2
            self.db.cursor.execute("""
                INSERT INTO Person2 (
                    Nationality, NationalID, First, Middle, Last
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                person_data['nationality'], person_data['national_id'],
                person_data['first_name'], person_data['middle_name'],
                person_data['last_name']
            ))

            # Insert into Person3 (multiple email addresses)
            for email in emails:
                self.db.cursor.execute("""
                    INSERT INTO Person3 (
                        Email, Nationality, NationalID
                    ) VALUES (%s, %s, %s)
                """, (
                    email, person_data['nationality'], person_data['national_id']
                ))

            self.db.connection.commit()
            print("\nPerson added successfully!")
            logging.info(f"New person added: {
                person_data['nationality']}-{person_data['national_id']}")

        except Exception as e:
            self.db.connection.rollback()
            logging.error(f"Error adding person: {str(e)}")
            print(f"\nError: {str(e)}")

    def add_location(self):
        """Add a new location to the database"""
        try:
            print("\nAdd New Location")
            location_data = {
                'country': input("Country: ").strip(),
                'pincode': input("Pincode: ").strip(),
                'state': input("State: ").strip(),
                'city': input("City: ").strip()
            }

            self.db.cursor.execute("""
                INSERT INTO Locations (Country, Pincode, State, City)
                VALUES (%s, %s, %s, %s)
            """, (location_data['country'], location_data['pincode'],
                  location_data['state'], location_data['city']))

            self.db.connection.commit()
            print("\nLocation added successfully!")

        except Exception as e:
            self.db.connection.rollback()
            logging.error(f"Error adding location: {str(e)}")
            print(f"\nError: {str(e)}")

    def add_bank(self):
        """Add a new bank to the database"""
        try:
            print("\nAdd New Bank")
            bank_data = {
                'bank_name': input("Bank Name: ").strip(),
                'head_nationality': input("Global Head Nationality: ").strip(),
                'head_national_id': input("Global Head National ID: ").strip(),
                'country': input("Bank Country: ").strip(),
                'pincode': input("Bank Pincode: ").strip()
            }

            self.db.cursor.execute("START TRANSACTION")

            # Generate new bank ID
            self.db.cursor.execute(
                "SELECT MAX(BankID) as max_id FROM RegisteredBank1")
            result = self.db.cursor.fetchone()
            bank_id = (result['max_id'] or 0) + 1

            # Insert into RegisteredBank1
            self.db.cursor.execute("""
                INSERT INTO RegisteredBank1 (BankID, BankName, GlobalHeadNationality, GlobalHeadNationalID)
                VALUES (%s, %s, %s, %s)
            """, (bank_id, bank_data['bank_name'],
                  bank_data['head_nationality'], bank_data['head_national_id']))

            # Insert into RegisteredBank2
            self.db.cursor.execute("""
                INSERT INTO RegisteredBank2 (BankID, Country, Pincode)
                VALUES (%s, %s, %s)
            """, (bank_id, bank_data['country'], bank_data['pincode']))

            self.db.connection.commit()
            print(f"\nBank added successfully! Bank ID: {bank_id}")

        except Exception as e:
            self.db.connection.rollback()
            logging.error(f"Error adding bank: {str(e)}")
            print(f"\nError: {str(e)}")

    def add_branch(self):
        """Add a new bank branch"""
        try:
            print("\nAdd New Bank Branch")
            branch_data = {
                'bank_id': int(input("Bank ID: ").strip()),
                'manager_nationality': input("Branch Manager Nationality: ").strip(),
                'manager_national_id': input("Branch Manager National ID: ").strip(),
                'country': input("Branch Country: ").strip(),
                'pincode': input("Branch Pincode: ").strip()
            }

            self.db.cursor.execute("START TRANSACTION")

            # Generate new branch code
            self.db.cursor.execute("""
                SELECT MAX(BranchCode) as max_code 
                FROM BankBranch1 
                WHERE BankID = %s
            """, (branch_data['bank_id'],))
            result = self.db.cursor.fetchone()
            branch_code = (result['max_code'] or 0) + 1

            # Insert into BankBranch1
            self.db.cursor.execute("""
                INSERT INTO BankBranch1 (BranchCode, BankID, BranchManagerNationality, BranchManagerNationalID)
                VALUES (%s, %s, %s, %s)
            """, (branch_code, branch_data['bank_id'],
                  branch_data['manager_nationality'], branch_data['manager_national_id']))

            # Insert into BankBranch2
            self.db.cursor.execute("""
                INSERT INTO BankBranch2 (BranchCode, BankID, Country, Pincode)
                VALUES (%s, %s, %s, %s)
            """, (branch_code, branch_data['bank_id'],
                  branch_data['country'], branch_data['pincode']))

            self.db.connection.commit()
            print(f"\nBranch added successfully! Branch Code: {branch_code}")

        except Exception as e:
            self.db.connection.rollback()
            logging.error(f"Error adding branch: {str(e)}")
            print(f"\nError: {str(e)}")

    def add_budget(self):
        """Add a new budget for a user"""
        try:
            print("\nAdd New Budget")
            budget_data = {
                'category': input("Budget Category: ").strip(),
                'user_nationality': input("User Nationality: ").strip(),
                'user_national_id': input("User National ID: ").strip(),
                'budget_limit': float(input("Budget Limit: ").strip()),
                'duration_date': input("Duration Date (YYYY-MM-DD): ").strip(),
                'duration_time': input("Duration Time (HH:MM:SS): ").strip()
            }

            self.db.cursor.execute("START TRANSACTION")

            # Insert into Budgets1
            self.db.cursor.execute("""
                INSERT INTO Budgets1 (Category, UserNationality, UserNationalID, BudgetLimit, CurrentExpend)
                VALUES (%s, %s, %s, %s, 0)
            """, (budget_data['category'], budget_data['user_nationality'],
                  budget_data['user_national_id'], budget_data['budget_limit']))

            # Insert into Budgets2
            self.db.cursor.execute("""
                INSERT INTO Budgets2 (Category, UserNationality, UserNationalID, DurationDate, DurationTime)
                VALUES (%s, %s, %s, %s, %s)
            """, (budget_data['category'], budget_data['user_nationality'],
                  budget_data['user_national_id'], budget_data['duration_date'],
                  budget_data['duration_time']))

            self.db.connection.commit()
            print("\nBudget added successfully!")

        except Exception as e:
            self.db.connection.rollback()
            logging.error(f"Error adding budget: {str(e)}")
            print(f"\nError: {str(e)}")

    def add_savings_goal(self):
        """Add a new savings goal for a user"""
        try:
            print("\nAdd New Savings Goal")
            goal_data = {
                'goal_name': input("Goal Name: ").strip(),
                'user_nationality': input("User Nationality: ").strip(),
                'user_national_id': input("User National ID: ").strip(),
                'target_amount': float(input("Target Amount: ").strip()),
                'deadline_date': input("Deadline Date (YYYY-MM-DD): ").strip(),
                'deadline_time': input("Deadline Time (HH:MM:SS): ").strip()
            }

            self.db.cursor.execute("START TRANSACTION")

            # Insert into SavingsGoals1
            self.db.cursor.execute("""
                INSERT INTO SavingsGoals1 (GoalName, UserNationality, UserNationalID, TargetAmount, CurrentSaving)
                VALUES (%s, %s, %s, %s, 0)
            """, (goal_data['goal_name'], goal_data['user_nationality'],
                  goal_data['user_national_id'], goal_data['target_amount']))

            # Insert into SavingsGoals2
            self.db.cursor.execute("""
                INSERT INTO SavingsGoals2 (GoalName, UserNationality, UserNationalID, DeadlineDate, DeadlineTime)
                VALUES (%s, %s, %s, %s, %s)
            """, (goal_data['goal_name'], goal_data['user_nationality'],
                  goal_data['user_national_id'], goal_data['deadline_date'],
                  goal_data['deadline_time']))

            self.db.connection.commit()
            print("\nSavings goal added successfully!")

        except Exception as e:
            self.db.connection.rollback()
            logging.error(f"Error adding savings goal: {str(e)}")
            print(f"\nError: {str(e)}")


def main():
    banking_system = BankingSystem()

    # ASCII Art Banner
    banner = """

░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓███████▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░
░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░   ░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░░▒▓██████▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░


"""

    while True:
        try:
            sp.call('clear' if os.name == 'posix' else 'cls', shell=True)
            print(banner)

            username = input("Database Username: ").strip()
            password = getpass("Database Password: ")

            if banking_system.db.connect(username, password):
                print("\nConnected to the database successfully!")

                while True:
                    try:
                        banking_system.check_session_timeout()

                        print("\n=== Main Menu ===")

                        print("\nData Entry Operations:")
                        print("1.  Add New Location")
                        print("2.  Add New Bank")
                        print("3.  Add New Branch")
                        print("4.  Add New Person")
                        print("5.  Add New Bank Account")
                        print("6.  Add New Budget")
                        print("7.  Add New Savings Goal")

                        print("\nRetrieval Operations:")
                        print("8.  View User Transactions")
                        print("9.  View Branch Accounts")
                        print("10. View High Income Users")
                        print("11. View Bank Branch Statistics")
                        print("12. Calculate User Transaction Total")
                        print("13. Find Maximum Account Balance")
                        print("14. View Country Expenditure Statistics")
                        print("15. Search Users by Name")
                        print("16. Search Banks/Branches")

                        print("\nAnalysis Operations:")
                        print("17. Analyze Expenditure Patterns")
                        print("18. Analyze Transaction Patterns")

                        print("\nModification Operations:")
                        print("19. Update Budget Limit")
                        print("20. Remove Expired Goals")

                        print("\n21. Logout")

                        choice = input("\nEnter your choice (1-21): ").strip()

                        if choice == '21':
                            banking_system.db.disconnect()
                            print("\nLogged out successfully!")
                            break

                        # Map choices to functions
                        operations = {
                            '1': banking_system.add_location,
                            '2': banking_system.add_bank,
                            '3': banking_system.add_branch,
                            '4': banking_system.add_person,
                            '5': banking_system.add_bank_account,
                            '6': banking_system.add_budget,
                            '7': banking_system.add_savings_goal,
                            '8': banking_system.view_user_transactions,
                            '9': banking_system.view_branch_accounts,
                            '10': banking_system.view_high_income_users,
                            '11': banking_system.view_bank_branch_count,
                            '12': banking_system.calculate_user_transactions,
                            '13': banking_system.find_max_balance,
                            '14': banking_system.get_country_expenditure,
                            '15': banking_system.search_users,
                            '16': banking_system.search_banks,
                            '17': banking_system.analyze_expenditure_patterns,
                            '18': banking_system.analyze_transaction_patterns,
                            '19': banking_system.update_budget_limit,
                            '20': banking_system.remove_expired_goals
                        }

                        if choice in operations:
                            print("\n" + "="*50)
                            operations[choice]()
                            print("\n" + "="*50)
                            input("\nPress Enter to continue...")
                        else:
                            print("\nInvalid choice. Please try again.")

                    except SecurityException as se:
                        print(f"\nSecurity Error: {str(se)}")
                        break
                    except Exception as e:
                        logging.error(f"Operation error: {str(e)}")
                        print(f"\nError: {str(e)}")
                        input("\nPress Enter to continue...")

            else:
                print("\nFailed to connect to database. Please check your credentials.")

        except Exception as e:
            logging.error(f"System error: {str(e)}")
            print(f"\nSystem Error: {str(e)}")

        if input("\nDo you want to try again? (y/n): ").lower() != 'y':
            break

    print("\nThank you for using the Advanced Banking System! Goodbye! 👋")


if __name__ == "__main__":
    main()
