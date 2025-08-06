import pandas as pd

# Use your specified file path
FILE_PATH = r"D:\project-1\movie_metadata.csv"

def load_movie_data(file_path: str) -> pd.DataFrame:
    """
    Loads the movie dataset from a given CSV file path.
    """
    try:
        data = pd.read_csv(file_path)
        print(f" File successfully loaded from: {file_path}")
        return data
    except FileNotFoundError:
        print(f" File not found at: {file_path}")
        return pd.DataFrame()
    except Exception as error:
        print(f" Error reading file: {error}")
        return pd.DataFrame()


def clean_movie_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the movie dataset:
    - Removes duplicates.
    - Handles nulls in numeric and categorical columns.
    - Converts 'color' to numeric.
    """
    if data.empty:
        print("Dataset is empty. Skipping cleaning process.")
        return data

    print("\n Starting data cleaning process...")

    # Drop duplicate rows
    original_count = data.shape[0]
    data = data.drop_duplicates()
    print(f"Removed {original_count - data.shape[0]} duplicate rows.")

    # Handle 'color' column
    if 'color' in data.columns:
        data['color'].fillna(data['color'].mode()[0], inplace=True)
        data['color'] = data['color'].map({'Color': 1, ' Black and White': 0})
        print("Converted 'color' column to binary format.")

    # Drop rows with missing values in critical categorical columns
    critical_categoricals = ['director_name', 'actor_2_name', 'actor_3_name', 'plot_keywords']
    for col in critical_categoricals:
        if col in data.columns:
            data.dropna(subset=[col], inplace=True)

    # Fill missing values in numerical columns with median/mean
    num_fill_rules = {
        'num_critic_for_reviews': 'median',
        'duration': 'median',
        'director_facebook_likes': 'mean',
        'actor_3_facebook_likes': 'mean',
        'actor_1_facebook_likes': 'mean',
        'facenumber_in_poster': 'median',
    }

    for col, method in num_fill_rules.items():
        if col in data.columns:
            fill_val = data[col].median() if method == 'median' else data[col].mean()
            data[col].fillna(fill_val, inplace=True)

    # Drop rows with null values in financial columns
    for col in ['gross', 'budget']:
        if col in data.columns:
            data.dropna(subset=[col], inplace=True)

    # Fill categorical columns with mode or default
    if 'language' in data.columns:
        data['language'].fillna(data['language'].mode()[0], inplace=True)
    if 'content_rating' in data.columns:
        data['content_rating'].fillna('Not Rated', inplace=True)
    if 'aspect_ratio' in data.columns:
        data['aspect_ratio'].fillna(data['aspect_ratio'].mode()[0], inplace=True)

    print(" Cleaning completed.\n")
    return data


if __name__ == "__main__":
    # Step 1: Load Data
    df_movies = load_movie_data(FILE_PATH)

    # Step 2: Clean Data
    cleaned_movies = clean_movie_data(df_movies)

    
    print(cleaned_movies.head(3))
    print("\n Dataset Info:\n")
    print(cleaned_movies.info())
    print("\n Null values per column:\n")
    print(cleaned_movies.isnull().sum())
