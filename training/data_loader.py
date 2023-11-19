import os
import pandas as pd

script_directory = os.path.dirname(os.path.abspath(__file__))
csv_directory = os.path.join(script_directory, "csv")


# Função para carregar os dados dos filmes
def load_movies():
    movies_file = os.path.join(csv_directory, "movies_metadata.csv")
    movies = pd.read_csv(movies_file, low_memory=False)
    movies = movies[
        ["id", "original_title", "original_language", "vote_count", "imdb_id"]
    ]
    movies.rename(
        columns={
            "id": "MOVIE_ID",
            "original_title": "TITLE",
            "original_language": "LANGUAGE",
            "vote_count": "VOTE_COUNT",
            "imdb_id": "IMDB_ID",
        },
        inplace=True,
    )
    movies.dropna(inplace=True)
    movies = movies[movies["VOTE_COUNT"] > 999]

    movies = movies[movies["LANGUAGE"] == "en"]
    movies["MOVIE_ID"] = movies["MOVIE_ID"].astype(int)

    return movies


# Função para carregar os dados das avaliações
def load_ratings():
    ratings_file = os.path.join(csv_directory, "ratings.csv")
    ratings = pd.read_csv(ratings_file)
    ratings = ratings[["userId", "movieId", "rating"]]
    ratings.rename(
        columns={"userId": "USER_ID", "movieId": "MOVIE_ID", "rating": "RATING"},
        inplace=True,
    )

    user_ratings_count = ratings["USER_ID"].value_counts() > 999
    valid_users = user_ratings_count[user_ratings_count].index

    ratings = ratings[ratings["USER_ID"].isin(valid_users)]

    return ratings


movies = load_movies()
ratings = load_ratings()


# Função para processar e combinar os dados de filmes e avaliações
def get_combined_ratings_and_movies():
    ratings_and_movies = ratings.merge(movies, on="MOVIE_ID")
    ratings_and_movies.head()

    ratings_and_movies.drop_duplicates(["USER_ID", "MOVIE_ID"], inplace=True)
    del ratings_and_movies["MOVIE_ID"]

    return ratings_and_movies


ratings_and_movies = get_combined_ratings_and_movies()
