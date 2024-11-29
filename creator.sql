CREATE DATABASE IF NOT EXISTS BankingSystem;
USE BankingSystem;

-- Person1 table
 CREATE TABLE IF NOT EXISTS Person1 (
    Nationality VARCHAR(69),
    NationalID VARCHAR(69),
    Password VARCHAR(69) NOT NULL,
    CustodianNationality VARCHAR(69),
    CustodianNationalID VARCHAR(69),
    DateOfBirth DATE,
    Phone VARCHAR(69),
    AnnualIncome DECIMAL(15, 2),
    AnnualExpenditure DECIMAL(15, 2),
    -- GoalsCount INT Derived Attribute,
    PRIMARY KEY (Nationality, NationalID),
    FOREIGN KEY (CustodianNationality, CustodianNationalID) 
        REFERENCES Person1(Nationality, NationalID)
);

-- Person2 table
CREATE TABLE IF NOT EXISTS Person2 (
    Nationality VARCHAR(69),
    NationalID VARCHAR(69),
    First VARCHAR(69),
    Middle VARCHAR(69),
    Last VARCHAR(69),
    PRIMARY KEY (Nationality, NationalID),
    FOREIGN KEY (Nationality, NationalID) 
        REFERENCES Person1(Nationality, NationalID)
);

-- Person3 table
CREATE TABLE IF NOT EXISTS Person3 (
    Email VARCHAR(69),
    Nationality VARCHAR(69),
    NationalID VARCHAR(69),
    PRIMARY KEY (Email, Nationality, NationalID),
    FOREIGN KEY (Nationality, NationalID) 
        REFERENCES Person1(Nationality, NationalID)
);

-- Locations table
CREATE TABLE IF NOT EXISTS Locations (
    Country VARCHAR(69),
    Pincode VARCHAR(69),
    State VARCHAR(69),
    City VARCHAR(69),
    PRIMARY KEY (Country, Pincode)
);

-- Registered Bank1 table
CREATE TABLE IF NOT EXISTS RegisteredBank1 (
    BankID INT PRIMARY KEY,
    BankName VARCHAR(69) NOT NULL,
    GlobalHeadNationality VARCHAR(69) NOT NULL,
    GlobalHeadNationalID VARCHAR(69) NOT NULL,
    FOREIGN KEY (GlobalHeadNationality, GlobalHeadNationalID) 
        REFERENCES Person1(Nationality, NationalID)
);

-- Registered Bank2 table
CREATE TABLE IF NOT EXISTS RegisteredBank2 (
    BankID INT PRIMARY KEY,
    Pincode VARCHAR(69),
    Country VARCHAR(69) NOT NULL,
    FOREIGN KEY (BankID) REFERENCES RegisteredBank1(BankID),
    FOREIGN KEY (Country, Pincode) 
        REFERENCES Locations(Country, Pincode)
);

-- Bank Branch1 table
CREATE TABLE IF NOT EXISTS BankBranch1 (
    BranchCode INT,
    BankID INT,
    BranchManagerNationality VARCHAR(69) NOT NULL,
    BranchManagerNationalID VARCHAR(69) NOT NULL,
    PRIMARY KEY (BranchCode, BankID),
    FOREIGN KEY (BankID) REFERENCES RegisteredBank1(BankID),
    FOREIGN KEY (BranchManagerNationality, BranchManagerNationalID) 
        REFERENCES Person1(Nationality, NationalID)
);

-- Bank Branch2 table
CREATE TABLE IF NOT EXISTS BankBranch2 (
    BranchCode INT,
    BankID INT,
    Pincode VARCHAR(69),
    Country VARCHAR(69) NOT NULL,
    FOREIGN KEY (BranchCode, BankID) 
        REFERENCES BankBranch1(BranchCode, BankID),
    FOREIGN KEY (Country, Pincode) 
        REFERENCES Locations(Country, Pincode)
);

-- Bank Account table
CREATE TABLE IF NOT EXISTS BankAccount (
    AccountNumber INT PRIMARY KEY,
    UserNationalID VARCHAR(69) NOT NULL,
    UserNationality VARCHAR(69) NOT NULL,
    NomineeNationalID VARCHAR(69),
    NomineeNationality VARCHAR(69),
    BranchCode INT,
    BankID INT,
    Balance DECIMAL(15, 2),
    CreationDate DATE,
    FOREIGN KEY (UserNationality, UserNationalID) 
        REFERENCES Person1(Nationality, NationalID),
    FOREIGN KEY (BranchCode, BankID) 
        REFERENCES BankBranch1(BranchCode, BankID),
    FOREIGN KEY (NomineeNationality, NomineeNationalID) 
        REFERENCES Person1(Nationality, NationalID)
);

-- Current Account (Subclass of BankAccount)
CREATE TABLE IF NOT EXISTS  CurrentAccount (
    AccountNumber INT PRIMARY KEY,
    MinBalance DECIMAL(15, 2),
    MonthlyTransactionLimit INT,
    FOREIGN KEY (AccountNumber) REFERENCES BankAccount(AccountNumber)
);

-- Saving Account (Subclass of BankAccount)
CREATE TABLE IF NOT EXISTS SavingAccount (
    AccountNumber INT PRIMARY KEY,
    MinBalance DECIMAL(15, 2),
    InterestRate DECIMAL(5, 2),
    MonthlyWithdrawalLimit INT,
    FOREIGN KEY (AccountNumber) REFERENCES BankAccount(AccountNumber)
);

-- Salary Account (Subclass of BankAccount)
CREATE TABLE IF NOT EXISTS SalaryAccount (
    AccountNumber INT PRIMARY KEY,
    OrganisationID VARCHAR(69),
    EmployeeID VARCHAR(69),
    FOREIGN KEY (AccountNumber) REFERENCES BankAccount(AccountNumber)
);

-- Demat Account (Subclass of BankAccount)
CREATE TABLE IF NOT EXISTS DematAccount (
    AccountNumber INT PRIMARY KEY,
    DPID VARCHAR(69),
    TradingAccountLink VARCHAR(69),
    MaintenanceCharges DECIMAL(15, 2),
    FOREIGN KEY (AccountNumber) REFERENCES BankAccount(AccountNumber)
);

-- Fixed Deposit Account (Subclass of BankAccount)
CREATE TABLE IF NOT EXISTS FixedDepositAccount (
    AccountNumber INT PRIMARY KEY,
    LockinPeriod DATE,
    MaturityDate DATE,
    PrematurePenalty DECIMAL(15, 2),
    FOREIGN KEY (AccountNumber) REFERENCES BankAccount(AccountNumber)
);

-- Transaction1 table
CREATE TABLE IF NOT EXISTS Transaction1 (
    TransactionID INT UNIQUE,
    SenderAccNum INT,
    ReceiverAccNum INT,
    PRIMARY KEY (TransactionID, SenderAccNum, ReceiverAccNum),
    FOREIGN KEY (SenderAccNum) REFERENCES BankAccount(AccountNumber),
    FOREIGN KEY (ReceiverAccNum) REFERENCES BankAccount(AccountNumber)
);

-- Transaction2 table
CREATE TABLE IF NOT EXISTS Transaction2 (
    TransactionID INT,
    TransactionDate DATE NOT NULL,
    TransactionTime TIME NOT NULL,
    Amount DECIMAL(15, 2) NOT NULL,
    PRIMARY KEY (TransactionID),
    FOREIGN KEY (TransactionID) REFERENCES Transaction1(TransactionID)
);

-- Budgets1 table
CREATE TABLE IF NOT EXISTS Budgets1 (
    Category VARCHAR(69),
    UserNationality VARCHAR(69),
    UserNationalID VARCHAR(69),
    BudgetLimit DECIMAL(15, 2) NOT NULL,
    CurrentExpend DECIMAL(15, 2) NOT NULL,
    PRIMARY KEY (Category, UserNationality, UserNationalID),
    FOREIGN KEY (UserNationality, UserNationalID) 
        REFERENCES Person1(Nationality, NationalID)
);

-- Budgets2 table
CREATE TABLE IF NOT EXISTS Budgets2 (
    Category VARCHAR(69),
    UserNationality VARCHAR(69),
    UserNationalID VARCHAR(69),
    DurationDate DATE NOT NULL,
    DurationTime TIME NOT NULL,
    PRIMARY KEY (Category, UserNationality, UserNationalID),
    FOREIGN KEY (Category, UserNationality, UserNationalID) 
        REFERENCES Budgets1(Category, UserNationality, UserNationalID)
);

-- Savings Goals1 table
CREATE TABLE IF NOT EXISTS SavingsGoals1 (
    GoalName VARCHAR(69),
    UserNationality VARCHAR(69),
    UserNationalID VARCHAR(69),
    TargetAmount DECIMAL(15, 2) NOT NULL,
    CurrentSaving DECIMAL(15, 2) NOT NULL,
    PRIMARY KEY (GoalName, UserNationality, UserNationalID),
    FOREIGN KEY (UserNationality, UserNationalID) 
        REFERENCES Person1(Nationality, NationalID)
);

-- Savings Goals2 table
CREATE TABLE IF NOT EXISTS SavingsGoals2 (
    GoalName VARCHAR(69),
    UserNationality VARCHAR(69),
    UserNationalID VARCHAR(69),
    DeadlineDate DATE NOT NULL,
    DeadlineTime TIME NOT NULL,
    PRIMARY KEY (GoalName, UserNationality, UserNationalID),
    FOREIGN KEY (GoalName, UserNationality, UserNationalID) 
        REFERENCES SavingsGoals1(GoalName, UserNationality, UserNationalID)
);
