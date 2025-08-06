import mysql.connector
import pandas as pd

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="Mydatabase"
        )
        print("Connected to MySQL.")
        return conn, conn.cursor()
    except:
        print("Connection failed.")
        return None, None

def run_query(cursor, query, label):
    print(f"\n--- {label} ---")
    cursor.execute(query)
    rows = cursor.fetchall()
    cols = [col[0] for col in cursor.description]
    print(pd.DataFrame(rows, columns=cols))

def show_menu():
    menu = [
        "1. Top IMDb movies",
        "2. Avg IMDb by language",
        "3. Avg gross by country",
        "4. Top directors by count",
        "5. Top genres by IMDb score",  # ✅ New description
        "6. Most reviewed movies",
        "7. Best movies after 2010",
        "8. Top actors by likes",
        "9. Avg duration by genre",
        "10. Year-wise movie count",
        "0. Exit"
    ]
    print("\nChoose an option:")
    for item in menu:
        print(item)

def main():
    conn, cur = connect_to_database()
    if not cur:
        return

    queries = {
        1: (
            "SELECT LEFT(movie_title, 25) AS short_title, imdb_score "
            "FROM movie_Data ORDER BY imdb_score DESC LIMIT 10",
            "Top IMDb Movies"
        ),
        2: (
            "SELECT language, ROUND(AVG(imdb_score), 2) AS avg_rating "
            "FROM movie_Data GROUP BY language",
            "Avg IMDb by Language"
        ),
        3: (
            "SELECT LEFT(country, 20) AS short_country, ROUND(AVG(gross), 2) AS avg_gross "
            "FROM movie_Data GROUP BY short_country ORDER BY avg_gross DESC LIMIT 6",
            "Average Gross by Country"
        ),
        4: (
            "SELECT LEFT(director_name, 25) AS director, COUNT(*) AS movie_count "
            "FROM movie_Data GROUP BY director ORDER BY movie_count DESC LIMIT 5",
            "Top Directors by Count"
        ),
        5: (
            "SELECT SUBSTRING_INDEX(genres, '|', 1) AS genre, "
            "ROUND(AVG(imdb_score), 2) AS avg_imdb "
            "FROM movie_Data "
            "GROUP BY genre "
            "ORDER BY avg_imdb DESC "
            "LIMIT 5",
            "Top Genres by IMDb Score"
        ),
        6: (
            "SELECT LEFT(movie_title, 25) AS short_title, num_user_for_reviews "
            "FROM movie_Data ORDER BY num_user_for_reviews DESC LIMIT 10",
            "Most Reviewed Movies"
        ),
        7: (
            "SELECT LEFT(movie_title, 25) AS short_title, imdb_score "
            "FROM movie_Data WHERE title_year > 2010 AND imdb_score > 8 "
            "ORDER BY imdb_score DESC LIMIT 10",
            "Best Movies After 2010"
        ),
        8: (
            "SELECT LEFT(actor_1_name, 20) AS actor, SUM(actor_1_facebook_likes) AS total_likes "
            "FROM movie_Data GROUP BY actor ORDER BY total_likes DESC LIMIT 5",
            "Top Actors by Facebook Likes"
        ),
        9: (
            "SELECT SUBSTRING_INDEX(genres, '|', 1) AS genre, ROUND(AVG(duration), 2) AS avg_duration "
            "FROM movie_Data GROUP BY genre ORDER BY avg_duration DESC",
            "Avg Duration by Genre"
        ),
        10: (
            "SELECT title_year, COUNT(*) AS movie_count "
            "FROM movie_Data GROUP BY title_year ORDER BY title_year",
            "Movies per Year"
        )
    }

    while True:
        show_menu()
        try:
            choice = int(input("Enter choice: "))
            if choice == 0:
                print("Exiting.")
                break
            if choice in queries:
                run_query(cur, *queries[choice])
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")

    cur.close()
    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
