from movie_data_processing import load_movie_data, clean_movie_data
from loading_data_mysql import loading_data
from data import connect_to_database
from visualization import run_query, choose_plot

def show_menu():
    print("\n=== Movie Query & Visualization Menu ===")
    print("1. Top IMDb movies")
    print("2. Avg IMDb by language")
    print("3. Avg gross by country")
    print("4. Top directors by count")
    print("5. Avg budget by genre")
    print("6. Most reviewed movies")
    print("7. Best movies after 2010")
    print("8. Top actors by likes")
    print("9. Avg duration by genre")
    print("10. Year-wise movie count")
    print("0. Exit")

def main():
    # Step 1: Load raw data
    filepath = r"D:\project-1\movie_metadata.csv"
    df_raw = load_movie_data(filepath)

    if df_raw.empty:
        print("Data loading failed. Check file path.")
        return

    # Step 2: Clean data
    df_clean = clean_movie_data(df_raw)
    if df_clean.empty:
        print("Cleaning returned empty DataFrame.")
        return

    # Step 3: Load to MySQL
    loading_data(df_clean)

    # Step 4: Connect to MySQL and Run Queries
    conn, cursor = connect_to_database()
    if not conn or not cursor:
        print("Could not connect to MySQL.")
        return

    queries = {
        1: ("SELECT LEFT(movie_title, 25) AS short_title, imdb_score "
            "FROM movie_Data ORDER BY imdb_score DESC LIMIT 10",
            "short_title", "imdb_score", "Top IMDb Movies"),

        2: ("SELECT language, ROUND(AVG(imdb_score), 2) AS avg_rating "
            "FROM movie_Data GROUP BY language",
            "language", "avg_rating", "Average IMDb by Language"),

        3: ("SELECT LEFT(country, 20) AS short_country, ROUND(AVG(gross), 2) AS avg_gross "
            "FROM movie_Data GROUP BY short_country ORDER BY avg_gross DESC LIMIT 6",
            "short_country", "avg_gross", "Average Gross by Country"),

        4: ("SELECT LEFT(director_name, 25) AS director, COUNT(*) AS movie_count "
            "FROM movie_Data GROUP BY director ORDER BY movie_count DESC LIMIT 5",
            "director", "movie_count", "Top Directors by Movie Count"),

        5: ("SELECT SUBSTRING_INDEX(genres, '|', 1) AS genre, "
            "ROUND(AVG(budget), 2) AS avg_budget "
            "FROM movie_Data "
            "GROUP BY genre "
            "ORDER BY avg_budget DESC "
            "LIMIT 4",
            "genre", "avg_budget", "Avg Budget by Primary Genre"),

        6: ("SELECT LEFT(movie_title, 25) AS short_title, num_user_for_reviews "
            "FROM movie_Data ORDER BY num_user_for_reviews DESC LIMIT 10",
            "short_title", "num_user_for_reviews", "Most Reviewed Movies"),

        7: ("SELECT LEFT(movie_title, 25) AS short_title, imdb_score "
            "FROM movie_Data WHERE title_year > 2010 AND imdb_score > 8 "
            "ORDER BY imdb_score DESC LIMIT 10",
            "short_title", "imdb_score", "Best Movies After 2010"),

        8: ("SELECT LEFT(actor_1_name, 20) AS actor, SUM(actor_1_facebook_likes) AS total_likes "
            "FROM movie_Data GROUP BY actor ORDER BY total_likes DESC LIMIT 5",
            "actor", "total_likes", "Top Actors by Facebook Likes"),

        9: ("SELECT SUBSTRING_INDEX(genres, '|', 1) AS genre, ROUND(AVG(duration), 2) AS avg_duration "
            "FROM movie_Data GROUP BY genre ORDER BY avg_duration DESC",
            "genre", "avg_duration", "Avg Duration by Primary Genre"),

        10: ("SELECT title_year, COUNT(*) AS movie_count "
             "FROM movie_Data GROUP BY title_year ORDER BY title_year",
             "title_year", "movie_count", "Movies per Year")
    }

    while True:
        show_menu()
        try:
            choice = int(input("Enter your choice (0 to exit): "))
            if choice == 0:
                print("Exiting program.")
                break

            if choice in queries:
                query, x, y, title = queries[choice]
                df = run_query(cursor, query)
                if not df.empty:
                    print("\n--- Query Result ---")
                    print(df.head(10))
                    choose_plot(df, x, y, title)
                else:
                    print("No data returned for this query.")
            else:
                print("Invalid choice. Choose 1 to 10.")
        except ValueError:
            print("Please enter a valid number.")

    cursor.close()
    conn.close()
    print("MySQL connection closed. Program complete.")

if __name__ == "__main__":
    main()
