# Advanced Data Management Mid-Year Project

## 📌 Project Overview
This project is part of the **Advanced Data Management** course, focusing on **database design, data processing, and analytical queries**.  
It utilizes **PostgreSQL** for database storage and **Python** for data processing and analysis.

---

## 📂 Project Structure and Python Files

### **1️⃣ `Project_part3_updated_create_dim_tables.py`**
📌 **Objective:**  
This script **creates the dimension tables** in PostgreSQL, which store descriptive information such as customers, movies, and transactions.

🔹 **What It Does:**  
- Defines tables like `DimCustomer`, `DimMovie`, `DimCinema`, and `DimTransactionDate`.
- Establishes **foreign key relationships** for database integrity.
- **Drops existing tables** (if applicable) before creation to avoid conflicts.

---

### **2️⃣ `Project_part3_updated_create_fact_tables.py`**
📌 **Objective:**  
This script **creates the `FactSales` table**, which stores transactional data.

🔹 **What It Does:**  
- Defines the `FactSales` table with attributes like **tickets sold, total sales, transaction timestamps, and customer demographics**.
- Enforces **foreign key constraints** to link dimension tables.
- **Prepares the database schema** for inserting transactional records.

---

### **3️⃣ `Project_part3_updated_load_db.py`**
📌 **Objective:**  
Loads **synthetic data** into the database for testing and analysis.

🔹 **What It Does:**  
- **Populates** dimension tables (`DimCustomer`, `DimMovie`, `DimCinema`, etc.).
- Loads **realistic synthetic data** into `FactSales` with **randomized but meaningful attributes**.
- Ensures **data consistency** across tables in PostgreSQL.

---

### **4️⃣ `part2_query_analysis.py`**
📌 **Objective:**  
Executes SQL queries for **Part 2**, analyzing sales data and trends.

🔹 **What It Does:**  
- Uses SQL queries to **retrieve insights** from `FactSales`.
- Computes **aggregations, groupings, and pivot tables** for total sales based on **gender, movie genre, promotions, and showtimes**.
- Uses **Python (`pandas`)** for **data formatting and visualization**.

🔍 **Key Queries Answered:**  
✅ **Sales by Gender and Age Groups (2015-2018)**  
✅ **Total sales grouped by Movie Genre & Weekdays**  
✅ **Tickets sold based on Morning, Afternoon, Night showtimes**  
✅ **Sales by Directors & States**  

---

### **5️⃣ `part3_query_analysis.py`**
📌 **Objective:**  
Executes SQL queries for **Part 3**, focusing on **ranking and moving averages**.

🔹 **What It Does:**  
- Retrieves **top-ranked** results for **cinemas, directors, and browsers used for online sales**.
- Computes **8-week and 4-week moving averages** for total sales trends.
- Uses **Python (`pandas`, `matplotlib`)** for additional sorting, ranking, and plotting.

🔍 **Key Queries Answered:**  
✅ **Ranking of Cinemas** in each city based on total sales (2018).  
✅ **Top 10 movies** for male and female customers (2018).  
✅ **8-week and 4-week Moving Averages** for total sales trends.  

---

## 📧 Contact
For any questions, feel free to reach out!  

🚀 **This README provides an in-depth explanation of each Python file's objective and functionalities, making it easier for instructors and contributors to navigate the project.** 🚀  
