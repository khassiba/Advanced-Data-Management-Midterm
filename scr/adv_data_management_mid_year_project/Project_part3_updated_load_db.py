import psycopg2
import pandas as pd
import numpy as np

# PostgreSQL Connection Config
DB_NAME = "postgres"
DB_USER = "khha88838"
DB_PASSWORD = "55652323"
DB_HOST = "localhost"  # Use the service/container name if running in Docker
DB_PORT = "5432"

# Flag to reset DB (delete existing tables)
RESET_DB = True  # Change to False to keep existing tables

# Establish Connection
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True  # Commit automatically
    cursor = conn.cursor()
    print("✅ Connected to PostgreSQL successfully!")
except Exception as e:
    print(f"❌ Connection error: {e}")
    exit()

# Function to Drop Tables if RESET_DB is enabled
def drop_tables():
    if RESET_DB:
        print("⚠️ Dropping all tables (Reset mode enabled)...")
        cursor.execute("""
            DROP TABLE IF EXISTS FactSales CASCADE;
            DROP TABLE IF EXISTS DimCustomer CASCADE;
            DROP TABLE IF EXISTS DimMovie CASCADE;
            DROP TABLE IF EXISTS DimPromotion CASCADE;
            DROP TABLE IF EXISTS DimDate CASCADE;
            DROP TABLE IF EXISTS DimTransactionDate CASCADE;
            DROP TABLE IF EXISTS DimTime CASCADE;
            DROP TABLE IF EXISTS DimTransactionType CASCADE;
            DROP TABLE IF EXISTS DimCinema CASCADE;
        """)
        print("✅ All tables dropped successfully!")

# Function to Create Tables (If Not Exists)
def create_tables():
    table_creation_queries = [
        """
        CREATE TABLE IF NOT EXISTS DimCustomer (
            CustomerID INT PRIMARY KEY,
            CustomerName VARCHAR(100),
            Gender VARCHAR(10) CHECK (Gender IN ('Male', 'Female')),
            DateOfBirth DATE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS DimMovie (
            MovieID INT PRIMARY KEY,
            Title VARCHAR(255),
            Genre VARCHAR(50),
            Director VARCHAR(100),
            Star1 VARCHAR(100),
            Star2 VARCHAR(100),
            Star3 VARCHAR(100),
            Star4 VARCHAR(100),
            Star5 VARCHAR(100),
            ReleaseYear INT CHECK (ReleaseYear BETWEEN 1900 AND 2024)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS DimPromotion (
            PromotionID INT PRIMARY KEY,
            PromotionType VARCHAR(50),
            DiscountAmount DECIMAL(5,2) CHECK (DiscountAmount >= 0)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS DimDate (
            DateID INT PRIMARY KEY,
            Date DATE,
            Year INT CHECK (Year BETWEEN 2014 AND 2024),
            Month INT CHECK (Month BETWEEN 1 AND 12),
            Day INT CHECK (Day BETWEEN 1 AND 31),
            WeekdayWeekend VARCHAR(10) CHECK (WeekdayWeekend IN ('Weekday', 'Weekend')),
            HolidayIndicator BOOLEAN
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS DimTransactionDate (
            TransactionDateID INT PRIMARY KEY,
            TransactionDate DATE,
            Year INT CHECK (Year BETWEEN 2014 AND 2024),
            Month INT CHECK (Month BETWEEN 1 AND 12),
            Day INT CHECK (Day BETWEEN 1 AND 31),
            WeekdayWeekend VARCHAR(10) CHECK (WeekdayWeekend IN ('Weekday', 'Weekend')),
            HolidayIndicator BOOLEAN
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS DimTime (
            TimeID INT PRIMARY KEY,
            Hour INT CHECK (Hour BETWEEN 0 AND 23),
            Minute INT CHECK (Minute BETWEEN 0 AND 59),
            TimeOfDay VARCHAR(10) CHECK (TimeOfDay IN ('Morning', 'Afternoon', 'Night'))
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS DimTransactionType (
            TransactionTypeID INT PRIMARY KEY,
            TransactionMode VARCHAR(10) CHECK (TransactionMode IN ('Online', 'Offline')),
            BrowserUsed VARCHAR(50) -- NULL for Offline transactions
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS DimCinema (
            CinemaID INT PRIMARY KEY,
            CinemaName VARCHAR(100),
            HallName VARCHAR(50),
            HallCapacity INT CHECK (HallCapacity BETWEEN 50 AND 500),
            HallSize VARCHAR(10) CHECK (HallSize IN ('Small', 'Mid-size', 'Large')),
            State VARCHAR(50),
            City VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS FactSales (
            TransactionID BIGINT PRIMARY KEY,
            TransactionDateID BIGINT,
            TransactionTypeID BIGINT,
            CustomerID BIGINT,
            MovieID BIGINT,
            DateID BIGINT,
            TimeID BIGINT,
            PromotionID BIGINT,
            CinemaID BIGINT,
            TicketsSold BIGINT CHECK (TicketsSold >= 1),
            TotalSalesAmount DECIMAL(10,2) CHECK (TotalSalesAmount >= 0),
            Gender VARCHAR(10) CHECK (Gender IN ('Male', 'Female')),
            Age BIGINT CHECK (Age >= 6),
            AgeGroup VARCHAR(10) CHECK (AgeGroup IN ('6-11', '12-17', '18-40', '40+')),
            TransactionYear BIGINT CHECK (TransactionYear BETWEEN 2014 AND 2024),
            TransactionMonth BIGINT CHECK (TransactionMonth BETWEEN 1 AND 12),
            FOREIGN KEY (CustomerID) REFERENCES DimCustomer(CustomerID),
            FOREIGN KEY (MovieID) REFERENCES DimMovie(MovieID),
            FOREIGN KEY (DateID) REFERENCES DimDate(DateID),
            FOREIGN KEY (TransactionDateID) REFERENCES DimTransactionDate(TransactionDateID),
            FOREIGN KEY (TimeID) REFERENCES DimTime(TimeID),
            FOREIGN KEY (PromotionID) REFERENCES DimPromotion(PromotionID),
            FOREIGN KEY (TransactionTypeID) REFERENCES DimTransactionType(TransactionTypeID),
            FOREIGN KEY (CinemaID) REFERENCES DimCinema(CinemaID)
        );
        """
    ]

    for query in table_creation_queries:
        cursor.execute(query)
    print("✅ Tables created successfully!")

# Function to Load CSV Data into PostgreSQL Using executemany()
def load_csv_to_db(table_name, csv_file):
    df = pd.read_csv(csv_file)

    # Convert NaN values to None for SQL compatibility
    df = df.where(pd.notnull(df), None)

    # Prepare INSERT query
    columns = ", ".join(df.columns)
    placeholders = ", ".join(["%s"] * len(df.columns))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"

    # Convert DataFrame to List of Tuples
    data = df.values.tolist()

    # Bulk Insert using executemany()
    try:
        cursor.executemany(insert_query, data)
        print(f"✅ Data inserted into {table_name} successfully!")
    except Exception as e:
        print(f"❌ Error inserting data into {table_name}: {e}")

# Drop tables if RESET_DB is enabled
drop_tables()

# Run table creation
create_tables()

# Load Data into PostgreSQL
load_csv_to_db("DimCustomer", "DimCustomer.csv")
load_csv_to_db("DimMovie", "DimMovie.csv")
load_csv_to_db("DimPromotion", "DimPromotion.csv")
load_csv_to_db("DimDate", "DimDate.csv")
load_csv_to_db("DimTransactionDate", "DimTransactionDate.csv")
load_csv_to_db("DimTime", "DimTime.csv")
load_csv_to_db("DimTransactionType", "DimTransactionType.csv")
load_csv_to_db("DimCinema", "DimCinema.csv")
load_csv_to_db("FactSales", "FactSales.csv")  # Now uses executemany()

# Close Connection
cursor.close()
conn.close()
print("✅ PostgreSQL Connection Closed!")
