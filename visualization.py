import pandas as pd
import matplotlib.pyplot as plt
import textwrap
from data import connect_to_database  


def run_query(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    return pd.DataFrame(rows, columns=columns)


def plot_bar(df, x, y, title, xlabel, ylabel, horizontal=False):
    plt.figure(figsize=(12, 6))
    df[x] = df[x].apply(lambda val: '\n'.join(textwrap.wrap(str(val), width=15)))

    if horizontal:
        plt.barh(df[x], df[y], color='skyblue')
        plt.xlabel(ylabel)
        plt.ylabel(xlabel)
    else:
        plt.bar(df[x], df[y], color='skyblue')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45, ha='right')

    plt.title(title)
    plt.tight_layout()
    plt.show()


def plot_line(df, x, y, title, xlabel, ylabel):
    plt.figure(figsize=(12, 6))
    df[x] = df[x].apply(lambda val: '\n'.join(textwrap.wrap(str(val), width=15)))
    plt.plot(df[x], df[y], marker='o', color='green')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def plot_histogram(df, column, bins=10, title=None):
    plt.figure(figsize=(10, 5))
    plt.hist(df[column], bins=bins, color='orange', edgecolor='black')
    plt.title(title or f"Histogram of {column}")
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()


def plot_scatter(df, x, y, title, xlabel, ylabel):
    plt.figure(figsize=(10, 5))
    plt.scatter(df[x], df[y], color='red')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def plot_pie(df, labels_col, values_col, title):
    plt.figure(figsize=(8, 8))
    plt.pie(df[values_col], labels=df[labels_col], autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def show_menu():
    print("\nChoose a query to visualize:")
    print("1. Top IMDb movies")
    print("2. Avg IMDb by language")
    print("3. Avg gross by country")
    print("4. Top directors by count")
    print("5. Top genres by IMDb score")
    print("6. Most reviewed movies")
    print("7. Best movies after 2010")
    print("8. Top actors by likes")
    print("9. Avg duration by genre")
    print("10. Year-wise movie count")
    print("0. Exit")


def choose_plot(df, x, y, title):
    print("\nChoose chart type:")
    print("1. Bar chart")
    print("2. Line chart")
    print("3. Histogram")
    print("4. Scatter plot")
    print("5. Pie chart")  # Pie option
    try:
        choice = int(input("Enter chart type (1-5): "))
        if choice == 1:
            plot_bar(df, x, y, title, x.title(), y.title())
        elif choice == 2:
            plot_line(df, x, y, title, x.title(), y.title())
        elif choice == 3:
            plot_histogram(df, y, title=title)
        elif choice == 4:
            plot_scatter(df, x, y, title, x.title(), y.title())
        elif choice == 5:
            plot_pie(df, x, y, title)
        else:
            print("Invalid chart type.")
    except:
        print("Invalid input. Showing bar chart by default.")
        plot_bar(df, x, y, title, x.title(), y.title())


def visualize_query(choice, cursor):
    queries = {
        1: (
            "SELECT LEFT(movie_title, 25) AS short_title, imdb_score "
            "FROM movie_Data ORDER BY imdb_score DESC LIMIT 10",
            "short_title", "imdb_score", "Top IMDb Movies"
        ),
        2: (
            "SELECT language, ROUND(AVG(imdb_score), 2) AS avg_rating "
            "FROM movie_Data GROUP BY language",
            "language", "avg_rating", "Average IMDb by Language"
        ),
        3: (
            "SELECT LEFT(country, 20) AS short_country, ROUND(AVG(gross), 2) AS avg_gross "
            "FROM movie_Data GROUP BY short_country ORDER BY avg_gross DESC LIMIT 6",
            "short_country", "avg_gross", "Average Gross by Country"
        ),
        4: (
            "SELECT LEFT(director_name, 25) AS director, COUNT(*) AS movie_count "
            "FROM movie_Data GROUP BY director ORDER BY movie_count DESC LIMIT 5",
            "director", "movie_count", "Top Directors by Movie Count"
        ),
        5: (
            "SELECT SUBSTRING_INDEX(genres, '|', 1) AS genre, "
            "ROUND(AVG(imdb_score), 2) AS avg_imdb "
            "FROM movie_Data "
            "GROUP BY genre "
            "ORDER BY avg_imdb DESC "
            "LIMIT 5",
            "genre", "avg_imdb", "Top Genres by IMDb Score"
        ),
        6: (
            "SELECT LEFT(movie_title, 25) AS short_title, num_user_for_reviews "
            "FROM movie_Data ORDER BY num_user_for_reviews DESC LIMIT 10",
            "short_title", "num_user_for_reviews", "Most Reviewed Movies"
        ),
        7: (
            "SELECT LEFT(movie_title, 25) AS short_title, imdb_score "
            "FROM movie_Data WHERE title_year > 2010 AND imdb_score > 8 "
            "ORDER BY imdb_score DESC LIMIT 10",
            "short_title", "imdb_score", "Best Movies After 2010"
        ),
        8: (
            "SELECT LEFT(actor_1_name, 20) AS actor, SUM(actor_1_facebook_likes) AS total_likes "
            "FROM movie_Data GROUP BY actor ORDER BY total_likes DESC LIMIT 5",
            "actor", "total_likes", "Top Actors by Facebook Likes"
        ),
        9: (
            "SELECT SUBSTRING_INDEX(genres, '|', 1) AS genre, ROUND(AVG(duration), 2) AS avg_duration "
            "FROM movie_Data GROUP BY genre ORDER BY avg_duration DESC",
            "genre", "avg_duration", "Avg Duration by Primary Genre"
        ),
        10: (
            "SELECT title_year, COUNT(*) AS movie_count "
            "FROM movie_Data GROUP BY title_year ORDER BY title_year",
            "title_year", "movie_count", "Movies per Year"
        )
    }

    if choice in queries:
        query, x, y, title = queries[choice]
        df = run_query(cursor, query)
        if not df.empty:
            choose_plot(df, x, y, title)
        else:
            print("No data returned for this query.")
    else:
        print("Invalid query choice.")


if __name__ == "__main__":
    conn, cursor = connect_to_database()
    if conn and cursor:
        while True:
            show_menu()
            try:
                choice = int(input("Enter your choice (0 to exit): "))
                if choice == 0:
                    print("Exiting visualization.")
                    break
                visualize_query(choice, cursor)
            except ValueError:
                print("Please enter a valid number.")

        cursor.close()
        conn.close()
