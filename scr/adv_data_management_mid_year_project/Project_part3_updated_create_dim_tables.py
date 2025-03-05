import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

# Define dataset sizes
NUM_CUSTOMERS = 5000
NUM_MOVIES = 500
NUM_PROMOTIONS = 10
NUM_CINEMAS = 50
NUM_TRANSACTION_TYPES = 5  # 4 online + 1 offline
NUM_YEARS = list(range(2014, 2025))  # 2014-2024
NUM_HOURS = [9, 12, 15, 18, 21]  # Typical movie showtimes

# Predefined Data
STATES_CITIES = {
    "California": ["Los Angeles", "San Francisco", "San Diego"],
    "Texas": ["Houston", "Dallas", "Austin"],
    "New York": ["New York City", "Buffalo", "Rochester"],
    "Florida": ["Miami", "Orlando", "Tampa"],
    "Illinois": ["Chicago", "Springfield", "Naperville"]
}

GENRES = ["Action", "Drama", "Comedy", "Horror", "Sci-Fi", "Documentary"]
BROWSERS = ["Chrome", "Firefox", "Edge", "Safari"]

# Generate DimCustomer
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    gender = random.choice(["Male", "Female"])
    dob = fake.date_of_birth(minimum_age=6, maximum_age=80)  # Ensure valid ages
    customers.append([i, fake.name(), gender, dob])

df_customers = pd.DataFrame(customers, columns=["CustomerID", "CustomerName", "Gender", "DateOfBirth"])
df_customers.to_csv("DimCustomer.csv", index=False)

# Generate DimMovie
movies = []
for i in range(1, NUM_MOVIES + 1):
    director = fake.name()
    if i % 25 == 0:
        director = "Mohamed Khan"  # Ensuring some movies have Mohamed Khan

    actors = list(set([fake.name() for _ in range(random.randint(1, 5))]))  # Ensure unique cast members
    if i % 30 == 0:
        actors[random.randint(0, len(actors) - 1)] = "Omar Sharif"  # Ensuring Omar Sharif is a star in some movies

    movies.append([
        i, fake.sentence(nb_words=3), random.choice(GENRES), director,
        actors[0] if len(actors) > 0 else None,
        actors[1] if len(actors) > 1 else None,
        actors[2] if len(actors) > 2 else None,
        actors[3] if len(actors) > 3 else None,
        actors[4] if len(actors) > 4 else None,
        random.randint(1900, 2024)
    ])

df_movies = pd.DataFrame(movies, columns=["MovieID", "Title", "Genre", "Director", "Star1", "Star2", "Star3", "Star4", "Star5", "ReleaseYear"])
df_movies.to_csv("DimMovie.csv", index=False)

# Generate DimPromotion
promotions = [[i, fake.word(), round(random.uniform(0, 50), 2)] for i in range(1, NUM_PROMOTIONS + 1)]
df_promotions = pd.DataFrame(promotions, columns=["PromotionID", "PromotionType", "DiscountAmount"])
df_promotions.to_csv("DimPromotion.csv", index=False)

# Generate DimDate and DimTransactionDate
date_data = []
transaction_date_data = []
for year in NUM_YEARS:
    for month in range(1, 13):
        for day in range(1, 29):  # Keeping it simple (ignoring 30th & 31st)
            weekday_weekend = "Weekend" if fake.date_object().weekday() >= 5 else "Weekday"
            is_holiday = random.choice([True, False])
            date_data.append([f"{year:04d}{month:02d}{day:02d}", f"{year}-{month:02d}-{day:02d}", year, month, day, weekday_weekend, is_holiday])
            transaction_date_data.append([f"{year:04d}{month:02d}{day:02d}", f"{year}-{month:02d}-{day:02d}", year, month, day, weekday_weekend, is_holiday])

df_date = pd.DataFrame(date_data, columns=["DateID", "Date", "Year", "Month", "Day", "WeekdayWeekend", "HolidayIndicator"])
df_date.to_csv("DimDate.csv", index=False)

df_transaction_date = pd.DataFrame(transaction_date_data, columns=["TransactionDateID", "TransactionDate", "Year", "Month", "Day", "WeekdayWeekend", "HolidayIndicator"])
df_transaction_date.to_csv("DimTransactionDate.csv", index=False)

# Generate DimTime
time_data = []
for i, hour in enumerate(NUM_HOURS, start=1):
    time_of_day = "Morning" if hour < 12 else "Afternoon" if hour < 18 else "Night"
    time_data.append([i, hour, 0, time_of_day])

df_time = pd.DataFrame(time_data, columns=["TimeID", "Hour", "Minute", "TimeOfDay"])
df_time.to_csv("DimTime.csv", index=False)

# Generate DimTransactionType
transaction_types = [[1, "Online", "Chrome"], [2, "Online", "Firefox"], [3, "Online", "Edge"], [4, "Online", "Safari"], [5, "Offline", None]]
df_transaction_type = pd.DataFrame(transaction_types, columns=["TransactionTypeID", "TransactionMode", "BrowserUsed"])
df_transaction_type.to_csv("DimTransactionType.csv", index=False)

# Generate DimCinema
cinema_data = []
cinema_id = 1  # Start Cinema ID counter

for state, cities in STATES_CITIES.items():
    for city in cities:
        num_cinemas = random.randint(2, 4)  # Each city has 2-4 cinemas
        for _ in range(num_cinemas):
            cinema_name = fake.company()
            num_halls = random.randint(2, 8)  # Each cinema has 2-8 halls

            for hall_num in range(1, num_halls + 1):  # Assign halls to the same cinema
                hall_name = f"{cinema_name} - Hall {hall_num}"
                hall_capacity = random.randint(50, 500)
                hall_size = "Small" if hall_capacity <= 200 else "Mid-size" if hall_capacity <= 400 else "Large"

                cinema_data.append([cinema_id, cinema_name, hall_name, hall_capacity, hall_size, state, city])

            cinema_id += 1  # Increment cinema ID only after all halls are assigned

# Convert to DataFrame
df_cinema = pd.DataFrame(cinema_data,
                         columns=["CinemaID", "CinemaName", "HallName", "HallCapacity", "HallSize", "State", "City"])

# Save to CSV
df_cinema.to_csv("DimCinema.csv", index=False)

print("✅ Updated Dimension tables data generated and saved as CSV files!")
