import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()

# Load dimension tables (use only necessary columns)
df_customers = pd.read_csv("DimCustomer.csv", usecols=["CustomerID", "Gender", "DateOfBirth"])
df_movies = pd.read_csv("DimMovie.csv", usecols=["MovieID", "ReleaseYear"])
df_cinemas = pd.read_csv("DimCinema.csv", usecols=["CinemaID"])
df_dates = pd.read_csv("DimDate.csv", usecols=["DateID", "Year"])
df_transaction_dates = pd.read_csv("DimTransactionDate.csv", usecols=["TransactionDateID", "Year", "Month"])
df_times = pd.read_csv("DimTime.csv", usecols=["TimeID"])
df_promotions = pd.read_csv("DimPromotion.csv", usecols=["PromotionID"])
df_transaction_types = pd.read_csv("DimTransactionType.csv", usecols=["TransactionTypeID"])

# Configuration
NUM_TRANSACTIONS = 1_000_000  # 1 million transactions
AGE_GROUPS = [(6, 11, "6-11"), (12, 17, "12-17"), (18, 40, "18-40"), (41, 100, "40+")]
TICKET_PRICES = np.array([5, 10, 15, 20])  # Ticket price options
TICKET_COUNTS = np.array([1, 2, 3, 4, 5, 6])  # Ticket count options

# Convert to NumPy arrays for fast access
customer_array = df_customers.to_records(index=False)
movie_array = df_movies.to_records(index=False)
cinema_array = df_cinemas.to_records(index=False)
date_array = df_dates.to_records(index=False)
transaction_date_array = df_transaction_dates.to_records(index=False)
time_array = df_times.to_records(index=False)
promotion_array = df_promotions.to_records(index=False)
transaction_type_array = df_transaction_types.to_records(index=False)

# Preallocate list for fast appends
fact_sales = []

# Generate transactions in bulk
for _ in range(NUM_TRANSACTIONS):
    valid_transaction = False

    while not valid_transaction:  # Keep trying until we get a valid transaction
        customer = random.choice(customer_array)
        movie = random.choice(movie_array)
        cinema = random.choice(cinema_array)
        transaction_date = random.choice(transaction_date_array)
        date = random.choice(date_array)  # Movie show date
        time_slot = random.choice(time_array)
        transaction_type = random.choice(transaction_type_array)
        promotion = random.choice(promotion_array) if random.random() > 0.7 else None  # 30% have promotions

        # Compute Age
        transaction_year = transaction_date.Year
        birth_year = int(str(customer.DateOfBirth)[:4])  # Extract year from date
        age = transaction_year - birth_year

        # Validate conditions
        if age >= 6 and transaction_year >= movie.ReleaseYear:
            valid_transaction = True  # Accept transaction

    # Assign Age Group
    age_group = next(group for min_age, max_age, group in AGE_GROUPS if min_age <= age <= max_age)

    # Assign Tickets Sold and Calculate Total Sales
    tickets_sold = np.random.choice(TICKET_COUNTS)
    total_sales = np.random.choice(TICKET_PRICES) * tickets_sold

    # Append Valid Transaction
    fact_sales.append([
        _,  # TransactionID (auto-increment)
        transaction_date.TransactionDateID,
        transaction_type.TransactionTypeID,
        customer.CustomerID,
        movie.MovieID,
        date.DateID,
        time_slot.TimeID,
        promotion.PromotionID if promotion is not None else None,
        cinema.CinemaID,
        tickets_sold,
        total_sales,
        customer.Gender,
        age,
        age_group,
        transaction_year,
        transaction_date.Month
    ])

# Convert to DataFrame
df_fact_sales = pd.DataFrame(fact_sales, columns=[
    "TransactionID", "TransactionDateID", "TransactionTypeID", "CustomerID", "MovieID",
    "DateID", "TimeID", "PromotionID", "CinemaID", "TicketsSold", "TotalSalesAmount",
    "Gender", "Age", "AgeGroup", "TransactionYear", "TransactionMonth"
])

# Save to CSV
df_fact_sales.to_csv("FactSales.csv", index=False)

print("✅ FactSales table generated successfully with 1,000,000 transactions (Optimized)!")
