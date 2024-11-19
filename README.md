# Transaxion

**Course Project for Data and Applications 2024**  
*International Institute of Information Technology, Hyderabad (IIIT-H)*  

---

## 📖 Overview

**Transaxion** is a database-backed application designed to manage transactional operations in a financial ecosystem. It leverages a relational database to store, retrieve, and manipulate structured data efficiently. The project implements real-world banking scenarios, showcasing various querying and update functionalities using Python and MySQL.

---

## 🎯 Objectives

1. **Database Design**: Develop a relational schema for a financial system with entities like `Person`, `BankAccount`, `Transactions`, etc.  
2. **Data Management**: Perform CRUD operations using `pymysql` to interact with the MySQL database.  
3. **Functional Queries**: Implement at least 5 data retrieval queries.  
4. **Updates**: Perform at least 3 updates to simulate real-world modifications in the database.  
5. **Error Handling**: Ensure domain constraints and referential integrity are maintained during user input and database updates.

---

## 🛠️ Features

- **View All Persons**: Retrieve all records from the `Person` table.  
- **Add a New Person**: Insert a new record into the `Person` table with data validation.  
- **View Bank Accounts**: Display details of all bank accounts.  
- **Update Bank Balance**: Modify the balance for a given account.  
- **Delete a Person**: Remove a person and their associated records from the database.

---

## 🚀 Getting Started

### Prerequisites

1. **Python**: Ensure Python 3.x is installed.
2. **MySQL Server**: Install MySQL and create a database named `BANK_SYSTEM` by running `creator.sql`.
3. **Python Modules**: Install required dependency:
   ```bash
   pip install pymysql
   ```

### Running the Application

1. Start the application:
   ```bash
   python main.py
   ```
2. Enter your MySQL username and password to connect.  

---

## 📄 License

This project is licensed under the MIT License.