import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL Connection Config
DB_NAME = "postgres"
DB_USER = "khha88838"
DB_PASSWORD = "55652323"
DB_HOST = "localhost"
DB_PORT = "5432"


# Establish Database Connection using SQLAlchemy
def get_db_connection():
    db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(db_url)
    return engine


# Define SQL Queries for Part 2
queries = {
    "sales_by_year_gender": """
        SELECT f.TransactionYear, f.Gender, SUM(f.TotalSalesAmount) AS TotalSales
        FROM FactSales f
        GROUP BY f.TransactionYear, f.Gender
        ORDER BY f.TransactionYear, f.Gender;
    """,

    "sales_by_month_online_offline": """
        SELECT f.TransactionYear, f.TransactionMonth, t.TransactionMode, SUM(f.TotalSalesAmount) AS TotalSales
        FROM FactSales f
        JOIN DimTransactionType t ON f.TransactionTypeID = t.TransactionTypeID
        GROUP BY ROLLUP (f.TransactionYear, f.TransactionMonth), t.TransactionMode
        ORDER BY f.TransactionYear, f.TransactionMonth, t.TransactionMode;
    """,

    "sales_by_genre_weekend": """
        SELECT m.Genre, d.WeekdayWeekend, SUM(f.TotalSalesAmount) AS TotalSales
        FROM FactSales f
        JOIN DimMovie m ON f.MovieID = m.MovieID
        JOIN DimDate d ON f.DateID = d.DateID
        GROUP BY m.Genre, d.WeekdayWeekend
        ORDER BY m.Genre, d.WeekdayWeekend;
    """,

    "sales_by_gender_promotion": """
        SELECT f.Gender, p.PromotionType, SUM(f.TotalSalesAmount) AS TotalSales
        FROM FactSales f
        LEFT JOIN DimPromotion p ON f.PromotionID = p.PromotionID
        WHERE f.TransactionYear = 2018
        GROUP BY f.Gender, p.PromotionType
        ORDER BY f.Gender, p.PromotionType;
    """,

    "sales_by_gender_tickets": """
        SELECT f.Gender, f.TicketsSold, SUM(f.TotalSalesAmount) AS TotalSales
        FROM FactSales f
        WHERE f.TransactionYear = 2018
        GROUP BY f.Gender, f.TicketsSold
        ORDER BY f.Gender, f.TicketsSold;
    """,

    "tickets_sold_gender_showtime": """
        SELECT f.Gender, t.TimeOfDay, SUM(f.TicketsSold) AS TotalTickets
        FROM FactSales f
        JOIN DimTime t ON f.TimeID = t.TimeID
        WHERE f.TransactionYear = 2018
        GROUP BY f.Gender, t.TimeOfDay
        ORDER BY f.Gender, t.TimeOfDay;
    """,

    "sales_mohamed_khan_by_year_state": """
        SELECT f.TransactionYear, c.State, SUM(f.TotalSalesAmount) AS TotalSales
        FROM FactSales f
        JOIN DimMovie m ON f.MovieID = m.MovieID
        JOIN DimCinema c ON f.CinemaID = c.CinemaID
        WHERE f.TransactionYear BETWEEN 2015 AND 2018 AND m.Director = 'Mohamed Khan'
        GROUP BY f.TransactionYear, c.State
        ORDER BY f.TransactionYear, c.State;
    """,

    "sales_omar_sharif_by_genre_gender": """
        SELECT m.Genre, f.Gender, SUM(f.TotalSalesAmount) AS TotalSales
        FROM FactSales f
        JOIN DimMovie m ON f.MovieID = m.MovieID
        WHERE m.Star1 = 'Omar Sharif' OR m.Star2 = 'Omar Sharif' OR m.Star3 = 'Omar Sharif' 
           OR m.Star4 = 'Omar Sharif' OR m.Star5 = 'Omar Sharif'
        GROUP BY m.Genre, f.Gender
        ORDER BY m.Genre, f.Gender;
    """,

    "sales_offline_2018_by_state_hallsize": """
        SELECT c.State, c.HallSize, SUM(f.TotalSalesAmount) AS TotalSales
        FROM FactSales f
        JOIN DimCinema c ON f.CinemaID = c.CinemaID
        JOIN DimTransactionType t ON f.TransactionTypeID = t.TransactionTypeID
        WHERE f.TransactionYear = 2018 AND t.TransactionMode = 'Offline'
        GROUP BY c.State, c.HallSize
        ORDER BY c.State, c.HallSize;
    """,

    "sales_by_gender_agegroup": """
        SELECT 
            f.Gender, 
            f.Age, 
            f.AgeGroup, 
            SUM(f.TotalSalesAmount) AS TotalSales
        FROM FactSales f
        WHERE f.TransactionYear BETWEEN 2015 AND 2018
        GROUP BY f.Gender, ROLLUP (f.AgeGroup, f.Age)
        ORDER BY f.Gender NULLS LAST, f.AgeGroup NULLS LAST, f.Age NULLS LAST;
    """
}


# Function to Fetch and Display Results
def fetch_and_display_results():
    engine = get_db_connection()

    for query_name, sql in queries.items():
        df = pd.read_sql(sql, engine)
        print(f"\n🔹 {query_name.replace('_', ' ').title()} Results:")
        print(df.head(10))  # Show first 10 rows

    engine.dispose()  # Close connection


# Run the Queries
if __name__ == "__main__":
    fetch_and_display_results()
