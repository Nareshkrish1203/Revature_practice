import pandas as pd
import sqlalchemy
from urllib.parse import quote_plus
from movie_data_processing import load_movie_data, clean_movie_data

def loading_data(df):
    if df.empty:
        print("DataFrame is empty. Skipping upload.")
        return

    # MySQL connection details
    host = "localhost"
    port = 3306
    user = "root"
    password = "root"
    database = "Mydatabase"
    table_name = "movie_Data"

    try:
        encoded_pw = quote_plus(password)
        connection_string = f"mysql+mysqlconnector://{user}:{encoded_pw}@{host}:{port}/{database}"
        engine = sqlalchemy.create_engine(connection_string)

        # Upload to MySQL
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Data uploaded to table '{table_name}' in database '{database}'.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    path = r"D:\project-1\movie_metadata.csv"
    df_raw = load_movie_data(path)
    df_clean = clean_movie_data(df_raw)
    loading_data(df_clean)