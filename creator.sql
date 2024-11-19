CREATE DATABASE BankingSystem;
USE BankingSystem;

-- Person table
CREATE TABLE Person (
    Nationality VARCHAR(100),
    NationalID VARCHAR(100),
    Password VARCHAR(100),
    FirstName VARCHAR(100),
    MiddleName VARCHAR(100),
    LastName VARCHAR(100),
    DateOfBirth DATE,
    Phone VARCHAR(20) UNIQUE,
    Email VARCHAR(100),
    PRIMARY KEY (Nationality, NationalID)
);

-- Registered Bank table
CREATE TABLE RegisteredBank (
    BankID INT PRIMARY KEY,
    BankName VARCHAR(100),
    City VARCHAR(100),
    State VARCHAR(100),
    Pincode VARCHAR(20),
    Country VARCHAR(100),
    GlobalHead_Nationality VARCHAR(100),
    GlobalHead_NationalID VARCHAR(100),
    FOREIGN KEY (GlobalHead_Nationality, GlobalHead_NationalID) 
        REFERENCES Person(Nationality, NationalID)
);

-- Bank Branch table (Weak Entity)
CREATE TABLE BankBranch (
    BranchCode INT,
    BankID INT,
    City VARCHAR(100),
    State VARCHAR(100),
    Pincode VARCHAR(20),
    Country VARCHAR(100),
    BranchManager_Nationality VARCHAR(100),
    BranchManager_NationalID VARCHAR(100),
    PRIMARY KEY (BranchCode, BankID),
    FOREIGN KEY (BankID) REFERENCES RegisteredBank(BankID),
    FOREIGN KEY (BranchManager_Nationality, BranchManager_NationalID) 
        REFERENCES Person(Nationality, NationalID)
);

-- Bank Account table
CREATE TABLE BankAccount (
    AccountNumber INT PRIMARY KEY,
    User_Nationality VARCHAR(100),
    User_NationalID VARCHAR(100),
    BranchCode INT,
    BankID INT,
    Balance DECIMAL(15, 2),
    CreationDate DATE,
    Nominee_Nationality VARCHAR(100),
    Nominee_NationalID VARCHAR(100),
    FOREIGN KEY (User_Nationality, User_NationalID) 
        REFERENCES Person(Nationality, NationalID),
    FOREIGN KEY (BranchCode, BankID) 
        REFERENCES BankBranch(BranchCode, BankID),
    FOREIGN KEY (Nominee_Nationality, Nominee_NationalID) 
        REFERENCES Person(Nationality, NationalID)
);

-- Current Account (Subclass of BankAccount)
CREATE TABLE CurrentAccount (
    AccountNumber INT PRIMARY KEY,
    MinBalance DECIMAL(15, 2),
    MonthlyTransactionLimit INT,
    FOREIGN KEY (AccountNumber) REFERENCES BankAccount(AccountNumber)
);

-- Saving Account (Subclass of BankAccount)
CREATE TABLE SavingAccount (
    AccountNumber INT PRIMARY KEY,
    MinBalance DECIMAL(15, 2),
    InterestRate DECIMAL(5, 2),
    MonthlyWithdrawalLimit INT,
    FOREIGN KEY (AccountNumber) REFERENCES BankAccount(AccountNumber)
);

-- Salary Account (Subclass of BankAccount)
CREATE TABLE SalaryAccount (
    AccountNumber INT PRIMARY KEY,
    OrganisationID VARCHAR(100),
    EmployeeID VARCHAR(100),
    FOREIGN KEY (AccountNumber) REFERENCES BankAccount(AccountNumber)
);

-- Demat Account (Subclass of BankAccount)
CREATE TABLE DematAccount (
    AccountNumber INT PRIMARY KEY,
    DPID VARCHAR(100),
    TradingAccountLink VARCHAR(100),
    MaintenanceCharges DECIMAL(15, 2),
    FOREIGN KEY (AccountNumber) REFERENCES BankAccount(AccountNumber)
);

-- Fixed Deposit Account (Subclass of BankAccount)
CREATE TABLE FixedDepositAccount (
    AccountNumber INT PRIMARY KEY,
    LockinPeriod DATE,
    MaturityDate DATE,
    PrematurePenalty DECIMAL(15, 2),
    FOREIGN KEY (AccountNumber) REFERENCES BankAccount(AccountNumber)
);

-- Transaction table (Weak Entity)
CREATE TABLE Transaction (
    TransactionID INT,
    SenderAccNum INT,
    ReceiverAccNum INT,
    Amount DECIMAL(15, 2),
    TransactionDate DATE,
    TransactionTime TIME,
    PRIMARY KEY (TransactionID, SenderAccNum),
    FOREIGN KEY (SenderAccNum) REFERENCES BankAccount(AccountNumber),
    FOREIGN KEY (ReceiverAccNum) REFERENCES BankAccount(AccountNumber)
);

-- Budgets table (Weak Entity)
CREATE TABLE Budgets (
    Category VARCHAR(100),
    User_Nationality VARCHAR(100),
    User_NationalID VARCHAR(100),
    BudgetLimit DECIMAL(15, 2),
    CurrentExpend DECIMAL(15, 2),
    DurationDate DATE,
    DurationTime TIME,
    PRIMARY KEY (Category, User_Nationality, User_NationalID),
    FOREIGN KEY (User_Nationality, User_NationalID) 
        REFERENCES Person(Nationality, NationalID)
);

-- Savings Goals table (Weak Entity)
CREATE TABLE SavingsGoals (
    GoalName VARCHAR(100),
    User_Nationality VARCHAR(100),
    User_NationalID VARCHAR(100),
    TargetAmount DECIMAL(15, 2),
    CurrentSaving DECIMAL(15, 2),
    DeadlineDate DATE,
    DeadlineTime TIME,
    PRIMARY KEY (GoalName, User_Nationality, User_NationalID),
    FOREIGN KEY (User_Nationality, User_NationalID) 
        REFERENCES Person(Nationality, NationalID)
);
