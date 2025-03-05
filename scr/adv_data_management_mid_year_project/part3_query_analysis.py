
from sqlalchemy import create_engine
import pandas as pd
from matplotlib import pyplot as plt


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
    return engine  # Return engine instead of psycopg2 connection

queries = {
    "cinema_sales": """
        SELECT c.City, c.CinemaName, SUM(f.TotalSalesAmount) AS TotalSales
        FROM FactSales f
        JOIN DimCinema c ON f.CinemaID = c.CinemaID
        WHERE f.TransactionYear = 2018
        GROUP BY c.City, c.CinemaName;
    """,
    "director_movie_sales": """
        SELECT m.Director, m.Title AS MovieTitle, SUM(f.TotalSalesAmount) AS TotalSales
        FROM FactSales f
        JOIN DimMovie m ON f.MovieID = m.MovieID
        WHERE f.Age < 40
        GROUP BY m.Director, m.Title;
    """,
    "browser_ranking": """
        SELECT c.City, t.BrowserUsed, COUNT(*) AS TransactionCount
        FROM FactSales f
        JOIN DimTransactionType t ON f.TransactionTypeID = t.TransactionTypeID
        JOIN DimCinema c ON f.CinemaID = c.CinemaID
        WHERE t.TransactionMode = 'Online'
        GROUP BY c.City, t.BrowserUsed;
    """,
    "top_movies_2018": """
        SELECT f.Gender, m.Title AS MovieTitle, SUM(f.TicketsSold) AS TicketsSold
        FROM FactSales f
        JOIN DimMovie m ON f.MovieID = m.MovieID
        WHERE f.TransactionYear = 2018
        GROUP BY f.Gender, m.Title;
    """,
    "cinema_ticket_sales": """
        SELECT c.City, c.CinemaName, SUM(f.TicketsSold) AS TotalTickets
        FROM FactSales f
        JOIN DimCinema c ON f.CinemaID = c.CinemaID
        WHERE f.TransactionYear BETWEEN 2014 AND 2018
        GROUP BY c.City, c.CinemaName;
    """,
    "weekly_sales_2018": """
        SELECT EXTRACT(WEEK FROM d.TransactionDate) AS WeekNumber, SUM(f.TotalSalesAmount) AS TotalSales
        FROM FactSales f
        JOIN DimTransactionDate d ON f.TransactionDateID = d.TransactionDateID
        WHERE d.Year = 2018
        GROUP BY WeekNumber;
    """,
    "weekly_sales_2010_2018": """
        SELECT c.City, EXTRACT(WEEK FROM d.TransactionDate) AS WeekNumber, SUM(f.TotalSalesAmount) AS TotalSales
        FROM FactSales f
        JOIN DimTransactionDate d ON f.TransactionDateID = d.TransactionDateID
        JOIN DimCinema c ON f.CinemaID = c.CinemaID
        WHERE d.Year BETWEEN 2010 AND 2018
        GROUP BY c.City, WeekNumber;
    """
}


def fetch_and_process_data():
    """Fetches data from PostgreSQL and computes rankings & moving averages in Python."""
    engine = get_db_connection()

    # Query: Cinema Sales Ranking
    df_cinema_sales = pd.read_sql(queries["cinema_sales"], engine)
    df_cinema_sales.columns = df_cinema_sales.columns.str.lower()  # Convert to lowercase
    if 'city' in df_cinema_sales.columns:
        df_cinema_sales["rank"] = df_cinema_sales.groupby("city")["totalsales"].rank(ascending=False, method="dense")

    # Query: Director Movie Sales Ranking
    # ****

    #
    df_director_sales = pd.read_sql(queries["director_movie_sales"], engine)
    df_director_sales.columns = df_director_sales.columns.str.lower()
    if 'director' in df_director_sales.columns:
        # Apply ranking
        df_director_sales["rank"] = df_director_sales.groupby("director")["totalsales"].rank(ascending=False,method="dense")
        # Sort by director (A-Z) and rank (highest rank first)
        df_director_sales = df_director_sales.sort_values(by=["director", "rank"], ascending=[True, False])

    # Query: Browser Ranking for Online Transactions
    df_browser_ranking = pd.read_sql(queries["browser_ranking"], engine)
    df_browser_ranking.columns = df_browser_ranking.columns.str.lower()
    if 'city' in df_browser_ranking.columns:
        # Apply ranking
        df_browser_ranking["rank"] = df_browser_ranking.groupby("city")["transactioncount"].rank(ascending=False,method="dense")
        # Sort by city (A-Z) and rank (highest rank first)
        df_browser_ranking = df_browser_ranking.sort_values(by=["city", "rank"], ascending=[True, False])

    # Query: Top 10 Movies in 2018 by Gender
    df_movies = pd.read_sql(queries["top_movies_2018"], engine)
    df_movies.columns = df_movies.columns.str.lower()

    df_top_movies = (df_movies.groupby("gender").
                     apply(lambda x: x.nlargest(10, "ticketssold")).
                     reset_index(drop=True))


    # Query: Cinema Ticket Sales Ranking (2014-2018)
    df_cinema_tickets = pd.read_sql(queries["cinema_ticket_sales"], engine)
    df_cinema_tickets.columns = df_cinema_tickets.columns.str.lower()
    if 'city' in df_cinema_tickets.columns:
        df_cinema_tickets["rank"] = df_cinema_tickets.groupby("city")["totaltickets"].rank(ascending=False,method="dense")
        df_cinema_tickets = df_cinema_tickets.sort_values(by=["city", "rank"], ascending=[True, True])

    # Query: Compute 8-Week Moving Average (2018)
    df_weekly_sales = pd.read_sql(queries["weekly_sales_2018"], engine)
    df_weekly_sales.columns = df_weekly_sales.columns.str.lower()
    df_weekly_sales["8-week_moving_avg"] = df_weekly_sales["totalsales"].rolling(window=8).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(df_weekly_sales["weeknumber"], df_weekly_sales["totalsales"], label="Total Sales", marker="o")
    plt.plot(df_weekly_sales["weeknumber"], df_weekly_sales["8-week_moving_avg"], label="8-Week Moving Avg",
             linestyle="dashed", color="red")

    # Customize plot
    plt.xlabel("Week Number (2018)")
    plt.ylabel("Total Sales Amount")
    plt.title("Weekly Sales and 8-Week Moving Average (2018)")
    plt.legend()
    plt.grid(True)

    # Show plot
    plt.show()

    # Query: Compute Largest 4-Week Moving Average (2010-2018) by City
    df_weekly_sales_2010_2018 = pd.read_sql(queries["weekly_sales_2010_2018"], engine)
    df_weekly_sales_2010_2018.columns = df_weekly_sales_2010_2018.columns.str.lower()
    df_weekly_sales_2010_2018["4-week_moving_avg"] = df_weekly_sales_2010_2018.groupby("city")["totalsales"].rolling(
        window=4).mean().reset_index(level=0, drop=True)
    df_largest_4week_city = df_weekly_sales_2010_2018.groupby("city")["4-week_moving_avg"].max().reset_index()

    # Query: Compute 3 Largest 4-Week Moving Averages of Total Sales (2018)
    df_weekly_sales["4-week_moving_avg"] = df_weekly_sales["totalsales"].rolling(window=4).mean()
    df_largest_4week = df_weekly_sales.nlargest(3, "4-week_moving_avg")

    engine.dispose()  # Close the SQLAlchemy engine connection

    return df_cinema_sales, df_director_sales, df_browser_ranking, df_top_movies, df_cinema_tickets, df_weekly_sales, df_largest_4week_city, df_largest_4week


if __name__ == "__main__":
    # Call the function to get processed data
    df_cinema_sales, df_director_sales, df_browser_ranking, df_top_movies, df_cinema_tickets, df_weekly_sales, df_largest_4week_city, df_largest_4week = fetch_and_process_data()

    # Display results
    print("\n🎬 Cinema Sales Ranking (2018):")
    print(df_cinema_sales.head(10))

    print("\n🎬 Director Movie Sales Ranking (Customers Under 40):")
    print(df_director_sales.head(10))

    print("\n🌐 Browser Ranking for Online Transactions:")
    print(df_browser_ranking.head(10))

    print("\n🎬 Top 10 Movies in 2018 by Gender:")
    print(df_top_movies)

    print("\n🎟️ Cinema Ticket Sales Ranking (2014-2018):")
    print(df_cinema_tickets.head(10))

    print("\n📊 8-Week Moving Average of Sales in 2018:")
    print(df_weekly_sales.head(10))

    print("\n📊 3 Largest 4-Week Moving Averages of Sales in 2018:")
    print(df_largest_4week)

    print("\n🏙️ Largest 4-Week Moving Average Per City (2010-2018):")
    print(df_largest_4week_city)

