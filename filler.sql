-- First, insert Locations data
INSERT INTO Locations VALUES
('India', '110001', 'Delhi', 'New Delhi'),
('India', '400001', 'Maharashtra', 'Mumbai'),
('India', '700001', 'West Bengal', 'Kolkata'),
('India', '600001', 'Tamil Nadu', 'Chennai'),
('India', '500001', 'Telangana', 'Hyderabad'),
('USA', '10001', 'New York', 'New York City'),
('UK', 'SW1A 1AA', 'England', 'London'),
('Japan', '100-0001', 'Tokyo', 'Chiyoda'),
('Singapore', '018989', 'Central Region', 'Singapore'),
('UAE', '00000', 'Dubai', 'Dubai');

-- Insert Person1 data (First without custodians)
INSERT INTO Person1 (Nationality, NationalID, Password, DateOfBirth, Phone, AnnualIncome, AnnualExpenditure) VALUES
('India', 'AADHAAR001', 'pass123', '1980-05-15', '+91-9876543210', 1500000.00, 1000000.00),
('India', 'AADHAAR002', 'pass124', '1975-06-20', '+91-9876543211', 2500000.00, 1800000.00),
('India', 'AADHAAR003', 'pass125', '1990-07-25', '+91-9876543212', 800000.00, 600000.00),
('India', 'AADHAAR004', 'pass126', '1985-08-30', '+91-9876543213', 3500000.00, 2500000.00),
('India', 'AADHAAR005', 'pass127', '1995-09-05', '+91-9876543214', 1200000.00, 900000.00),
('USA', 'SSN001', 'pass128', '1982-10-10', '+1-234-567-8901', 75000.00, 50000.00),
('UK', 'NIN001', 'pass129', '1978-11-15', '+44-7911-123456', 65000.00, 45000.00),
('Japan', 'MyNumber001', 'pass130', '1988-12-20', '+81-80-1234-5678', 8000000.00, 6000000.00),
('Singapore', 'NRIC001', 'pass131', '1992-01-25', '+65-8123-4567', 120000.00, 90000.00),
('UAE', 'EID001', 'pass132', '1986-02-28', '+971-50-123-4567', 200000.00, 150000.00);

-- Update Person1 with custodians
UPDATE Person1 SET 
CustodianNationality = 'India', CustodianNationalID = 'AADHAAR001'
WHERE NationalID = 'AADHAAR003';

-- Insert Person2 data
INSERT INTO Person2 VALUES
('India', 'AADHAAR001', 'Rajesh', 'Kumar', 'Sharma'),
('India', 'AADHAAR002', 'Priya', NULL, 'Patel'),
('India', 'AADHAAR003', 'Amit', 'Singh', 'Verma'),
('India', 'AADHAAR004', 'Sunita', NULL, 'Gupta'),
('India', 'AADHAAR005', 'Rahul', 'Kumar', 'Malhotra'),
('USA', 'SSN001', 'John', 'Robert', 'Smith'),
('UK', 'NIN001', 'James', NULL, 'Wilson'),
('Japan', 'MyNumber001', 'Takeshi', NULL, 'Yamamoto'),
('Singapore', 'NRIC001', 'Lee', 'Wei', 'Chen'),
('UAE', 'EID001', 'Mohammed', 'Abdul', 'Rahman');

-- Insert Person3 data
INSERT INTO Person3 VALUES
('rajesh.sharma@email.com', 'India', 'AADHAAR001'),
('priya.patel@email.com', 'India', 'AADHAAR002'),
('amit.verma@email.com', 'India', 'AADHAAR003'),
('sunita.gupta@email.com', 'India', 'AADHAAR004'),
('rahul.malhotra@email.com', 'India', 'AADHAAR005'),
('john.smith@email.com', 'USA', 'SSN001'),
('james.wilson@email.com', 'UK', 'NIN001'),
('takeshi.yamamoto@email.com', 'Japan', 'MyNumber001'),
('lee.chen@email.com', 'Singapore', 'NRIC001'),
('mohammed.rahman@email.com', 'UAE', 'EID001');

-- Insert RegisteredBank1 data
INSERT INTO RegisteredBank1 VALUES
(1, 'State Bank of India', 'India', 'AADHAAR001'),
(2, 'HDFC Bank', 'India', 'AADHAAR002'),
(3, 'ICICI Bank', 'India', 'AADHAAR003'),
(4, 'Axis Bank', 'India', 'AADHAAR004'),
(5, 'Punjab National Bank', 'India', 'AADHAAR005'),
(6, 'JP Morgan Chase', 'USA', 'SSN001'),
(7, 'Barclays', 'UK', 'NIN001'),
(8, 'Mitsubishi UFJ', 'Japan', 'MyNumber001'),
(9, 'DBS Bank', 'Singapore', 'NRIC001'),
(10, 'Emirates NBD', 'UAE', 'EID001');

-- Insert RegisteredBank2 data
INSERT INTO RegisteredBank2 VALUES
(1, '110001', 'India'),
(2, '400001', 'India'),
(3, '400001', 'India'),
(4, '500001', 'India'),
(5, '110001', 'India'),
(6, '10001', 'USA'),
(7, 'SW1A 1AA', 'UK'),
(8, '100-0001', 'Japan'),
(9, '018989', 'Singapore'),
(10, '00000', 'UAE');

-- Insert BankBranch1 data
INSERT INTO BankBranch1 VALUES
(101, 1, 'India', 'AADHAAR001'),
(102, 2, 'India', 'AADHAAR002'),
(103, 3, 'India', 'AADHAAR003'),
(104, 4, 'India', 'AADHAAR004'),
(105, 5, 'India', 'AADHAAR005'),
(106, 6, 'USA', 'SSN001'),
(107, 7, 'UK', 'NIN001'),
(108, 8, 'Japan', 'MyNumber001'),
(109, 9, 'Singapore', 'NRIC001'),
(110, 10, 'UAE', 'EID001');

-- Insert BankBranch2 data
INSERT INTO BankBranch2 VALUES
(101, 1, '110001', 'India'),
(102, 2, '400001', 'India'),
(103, 3, '400001', 'India'),
(104, 4, '500001', 'India'),
(105, 5, '110001', 'India'),
(106, 6, '10001', 'USA'),
(107, 7, 'SW1A 1AA', 'UK'),
(108, 8, '100-0001', 'Japan'),
(109, 9, '018989', 'Singapore'),
(110, 10, '00000', 'UAE');

-- Insert BankAccount data
INSERT INTO BankAccount VALUES
(1001, 'AADHAAR001', 'India', 'AADHAAR002', 'India', 101, 1, 100000.00, '2020-01-01'),
(1002, 'AADHAAR002', 'India', 'AADHAAR003', 'India', 102, 2, 200000.00, '2020-02-01'),
(1003, 'AADHAAR003', 'India', 'AADHAAR004', 'India', 103, 3, 150000.00, '2020-03-01'),
(1004, 'AADHAAR004', 'India', 'AADHAAR005', 'India', 104, 4, 300000.00, '2020-04-01'),
(1005, 'AADHAAR005', 'India', 'AADHAAR001', 'India', 105, 5, 250000.00, '2020-05-01'),
(1006, 'SSN001', 'USA', NULL, NULL, 106, 6, 50000.00, '2020-06-01'),
(1007, 'NIN001', 'UK', NULL, NULL, 107, 7, 45000.00, '2020-07-01'),
(1008, 'MyNumber001', 'Japan', NULL, NULL, 108, 8, 800000.00, '2020-08-01'),
(1009, 'NRIC001', 'Singapore', NULL, NULL, 109, 9, 120000.00, '2020-09-01'),
(1010, 'EID001', 'UAE', NULL, NULL, 110, 10, 200000.00, '2020-10-01');

-- Insert different types of accounts
-- Current Accounts
INSERT INTO CurrentAccount VALUES
(1001, 10000.00, 100),
(1006, 5000.00, 50);

-- Saving Accounts
INSERT INTO SavingAccount VALUES
(1002, 5000.00, 4.50, 20),
(1007, 3000.00, 3.75, 15);

-- Salary Accounts
INSERT INTO SalaryAccount VALUES
(1003, 'ORG001', 'EMP001'),
(1008, 'ORG002', 'EMP002');

-- Demat Accounts
INSERT INTO DematAccount VALUES
(1004, 'DP001', 'TRADE001', 500.00),
(1009, 'DP002', 'TRADE002', 400.00);

-- Fixed Deposit Accounts
INSERT INTO FixedDepositAccount VALUES
(1005, '2023-12-31', '2024-12-31', 500.00),
(1010, '2023-12-31', '2024-12-31', 400.00);

-- Insert Transaction1 data
INSERT INTO Transaction1 VALUES
(1, 1001, 1002),
(2, 1002, 1003),
(3, 1003, 1004),
(4, 1004, 1005),
(5, 1005, 1001),
(6, 1006, 1007),
(7, 1007, 1008),
(8, 1008, 1009),
(9, 1009, 1010),
(10, 1010, 1006);

-- Insert Transaction2 data
INSERT INTO Transaction2 VALUES
(1, '2023-01-01', '10:00:00', 1000.00),
(2, '2023-01-02', '11:00:00', 2000.00),
(3, '2023-01-03', '12:00:00', 3000.00),
(4, '2023-01-04', '13:00:00', 4000.00),
(5, '2023-01-05', '14:00:00', 5000.00),
(6, '2023-01-06', '15:00:00', 6000.00),
(7, '2023-01-07', '16:00:00', 7000.00),
(8, '2023-01-08', '17:00:00', 8000.00),
(9, '2023-01-09', '18:00:00', 9000.00),
(10, '2023-01-10', '19:00:00', 10000.00);

-- Insert Budgets1 data
INSERT INTO Budgets1 VALUES
('Groceries', 'India', 'AADHAAR001', 10000.00, 8000.00),
('Entertainment', 'India', 'AADHAAR002', 5000.00, 4000.00),
('Transport', 'India', 'AADHAAR003', 3000.00, 2500.00),
('Shopping', 'India', 'AADHAAR004', 15000.00, 12000.00),
('Utilities', 'India', 'AADHAAR005', 7000.00, 6000.00),
('Food', 'USA', 'SSN001', 1000.00, 800.00),
('Travel', 'UK', 'NIN001', 2000.00, 1500.00),
('Healthcare', 'Japan', 'MyNumber001', 50000.00, 40000.00),
('Education', 'Singapore', 'NRIC001', 3000.00, 2500.00),
('Housing', 'UAE', 'EID001', 5000.00, 4000.00);

-- Insert Budgets2 data
INSERT INTO Budgets2 VALUES
('Groceries', 'India', 'AADHAAR001', '2023-12-31', '23:59:59'),
('Entertainment', 'India', 'AADHAAR002', '2023-12-31', '23:59:59'),
('Transport', 'India', 'AADHAAR003', '2023-12-31', '23:59:59'),
('Shopping', 'India', 'AADHAAR004', '2023-12-31', '23:59:59'),
('Utilities', 'India', 'AADHAAR005', '2023-12-31', '23:59:59'),
('Food', 'USA', 'SSN001', '2023-12-31', '23:59:59'),
('Travel', 'UK', 'NIN001', '2023-12-31', '23:59:59'),
('Healthcare', 'Japan', 'MyNumber001', '2023-12-31', '23:59:59'),
('Education', 'Singapore', 'NRIC001', '2023-12-31', '23:59:59'),
('Housing', 'UAE', 'EID001', '2023-12-31', '23:59:59');

-- Insert SavingsGoals1 data
INSERT INTO SavingsGoals1 VALUES
('House', 'India', 'AADHAAR001', 5000000.00, 2000000.00),
('Car', 'India', 'AADHAAR002', 1000000.00, 500000.00),
('Education', 'India', 'AADHAAR003', 2000000.00, 1000000.00),
('Wedding', 'India', 'AADHAAR004', 3000000.00, 1500000.00),
('Retirement', 'India', 'AADHAAR005', 10000000.00, 4000000.00),
('Vacation', 'USA', 'SSN001', 10000.00, 5000.00),
('Business', 'UK', 'NIN001', 50000.00, 20000.00),
('Property', 'Japan', 'MyNumber001', 20000000.00, 10000000.00),
('Investment', 'Singapore', 'NRIC001', 100000.00, 50000.00),
('Emergency', 'UAE', 'EID001', 200000.00, 100000.00);

-- Insert SavingsGoals2 data
INSERT INTO SavingsGoals2 VALUES
('House', 'India', 'AADHAAR001', '2025-12-31', '23:59:59'),
('Car', 'India', 'AADHAAR002', '2024-12-31', '23:59:59'),
('Education', 'India', 'AADHAAR003', '2026-12-31', '23:59:59'),
('Wedding', 'India', 'AADHAAR004', '2025-06-30', '23:59:59'),
('Retirement', 'India', 'AADHAAR005', '2040-12-31', '23:59:59'),
('Vacation', 'USA', 'SSN001', '2024-06-30', '23:59:59'),
('Business', 'UK', 'NIN001', '2025-12-31', '23:59:59'),
('Property', 'Japan', 'MyNumber001', '2026-12-31', '23:59:59'),
('Investment', 'Singapore', 'NRIC001', '2024-12-31', '23:59:59'),
('Emergency', 'UAE', 'EID001', '2024-06-30', '23:59:59');
