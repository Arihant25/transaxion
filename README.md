# Transaxion

## Database Management System Project

### Overview

This is a comprehensive banking system that manages customer accounts, transactions, budgets, and savings goals. The system provides a user-friendly CLI interface to interact with the banking database.

### Features

#### Data Entry Operations

1. **Add New Location** (Command 1)

   - Adds new locations to the system
   - Required fields: Country, Pincode, State, City

2. **Add New Bank** (Command 2)

   - Registers new banks in the system
   - Captures bank details and global head information
   - Required fields: Bank Name, Global Head details, Location information

3. **Add New Branch** (Command 3)

   - Creates new bank branches
   - Links branches to existing banks
   - Required fields: Bank ID, Branch Manager details, Location information

4. **Add New Person** (Command 4)

   - Registers new customers in the system
   - Handles personal details, contact information, and financial data
   - Optional custodian assignment for minors
   - Required fields: Personal details, Income information, Contact details

5. **Add New Bank Account** (Command 5)

   - Creates different types of bank accounts:
     - Current Account
     - Savings Account
     - Salary Account
     - Demat Account
     - Fixed Deposit Account
   - Required fields: Account type specific details, Initial balance

6. **Add New Budget** (Command 6)

   - Creates budget plans for users
   - Required fields: Category, Limit, Duration

7. **Add New Savings Goal** (Command 7)
   - Sets up savings targets for users
   - Required fields: Goal details, Target amount, Deadline

#### Retrieval Operations

8. **View User Transactions** (Command 8)

   - Displays all transactions for a specific user
   - Shows transaction history with dates and amounts

9. **View Branch Accounts** (Command 9)

   - Lists all accounts in a specific branch
   - Shows account holders and balances

10. **View High Income Users** (Command 10)

    - Lists users above specified income threshold
    - Shows detailed user information

11. **View Bank Branch Statistics** (Command 11)

    - Displays branch count for each bank
    - Shows distribution of branches

12. **Calculate User Transaction Total** (Command 12)

    - Calculates total transaction amount for a user
    - Filters by date range

13. **Find Maximum Account Balance** (Command 13)

    - Identifies account with highest balance
    - Shows account holder details

14. **View Country Expenditure Statistics** (Command 14)

    - Shows average expenditure by country
    - Includes user count per country

15. **Search Users by Name** (Command 15)

    - Searches users using name patterns
    - Supports partial name matching

16. **Search Banks/Branches** (Command 16)
    - Searches banks by name or branch location
    - Shows detailed bank information

#### Analysis Operations

17. **Analyze Expenditure Patterns** (Command 17)

    - Analyzes user spending patterns
    - Groups by country or city
    - Shows percentage of income spent

18. **Analyze Transaction Patterns** (Command 18)
    - Studies transaction frequencies and amounts
    - Identifies high-volume users

#### Modification Operations

19. **Update Budget Limit** (Command 19)

    - Modifies existing budget limits
    - Validates against user income

20. **Remove Expired Goals** (Command 20)

    - Cleans up unmet savings goals
    - Maintains data integrity

#### Transaction Operations

21. **Make Transaction** (Command 21)
    - Performs a transaction between two accounts
    - Updates account balances
    - Logs transaction details

### Video Demonstration

The video demonstration shows all major functionalities of the system in the following order:

#### Data Entry Operations

1. Adding a New Location (Command 1)

   - Demonstrating location addition
   - Verifying in Locations table

2. Adding a New Bank (Command 2)

   - Creating a new bank entry
   - Verifying in RegisteredBank1 and RegisteredBank2 tables

3. Adding a New Branch (Command 3)

   - Creating a branch for existing bank
   - Verifying in BankBranch1 and BankBranch2 tables

4. Adding a New Person (Command 4)

   - Creating customer profile with all details
   - Verifying in Person1, Person2, and Person3 tables

5. Creating Different Bank Accounts (Command 5)

   - Demonstrating creation of:
     - Current Account
     - Savings Account
     - Salary Account
   - Verifying in respective account tables

6. Setting Up a Budget (Command 6)

   - Creating budget categories
   - Verifying in Budgets1 and Budgets2 tables

7. Creating Savings Goals (Command 7)
   - Setting up savings targets
   - Verifying in SavingsGoals1 and SavingsGoals2 tables

#### Retrieval Operations

8. Viewing User Transactions (Command 8)

   - Displaying transaction history
   - Showing different transaction types

9. Viewing Branch Accounts (Command 9)

   - Listing all accounts in a branch
   - Showing account details and balances

10. Viewing High Income Users (Command 10)

    - Demonstrating income-based filtering
    - Showing detailed user information

11. Viewing Bank Branch Statistics (Command 11)

    - Displaying branch distribution
    - Showing bank-wise statistics

12. Calculating Transaction Totals (Command 12)

    - Demonstrating period-wise calculations
    - Showing transaction summaries

13. Finding Maximum Balance (Command 13)

    - Identifying highest balance account
    - Showing account holder details

14. Viewing Country Statistics (Command 14)

    - Showing country-wise expenditure
    - Demonstrating statistical analysis

15. Searching Users (Command 15)

    - Demonstrating name-based search
    - Showing partial match results

16. Searching Banks/Branches (Command 16)
    - Location-based search
    - Name-based search

#### Analysis Operations

17. Expenditure Pattern Analysis (Command 17)

    - Showing spending patterns
    - Demonstrating geographical analysis

18. Transaction Pattern Analysis (Command 18)
    - Frequency analysis
    - Amount-based patterns

#### Modification Operations

19. Budget Limit Updates (Command 19)

    - Modifying existing budgets
    - Showing validation checks

20. Expired Goals Management (Command 20)
    - Cleaning up expired goals
    - Demonstrating data integrity

#### Transaction Operations

21. Making Transactions (Command 21)
    - Performing account transactions
    - Showing real-time updates

Each operation is demonstrated with:

1. Command execution in the CLI interface
2. Database verification using SQL Workbench
3. Display of before and after states
4. Error handling demonstration for one case, all other cases are handled similarly

The video maintains a clear flow, showing:

- Input validation
- Success messages
- Error handling
- Database consistency
- Real-time updates

Note: The demonstration uses pre-populated data to show realistic scenarios and interactions between different components of the system.

### Technical Requirements

- Python 3.7+
- MySQL Server
- Required Python packages:
  - pymysql
  - logging
  - getpass

### Setup Instructions

1. Create the database using the provided SQL scripts
2. Configure database connection parameters
3. Install required Python packages
4. Run the main.py script

### Security Features

- Session timeout management
- Password protection
- Transaction verification
- Data validation
- Error logging

### Error Handling

The system includes comprehensive error handling for:

- Database connection issues
- Invalid input data
- Constraint violations
- Transaction failures
- Security breaches

### Logging

All operations are logged in 'banking_system.log' with timestamps and error details.
