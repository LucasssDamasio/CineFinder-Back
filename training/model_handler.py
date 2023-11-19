import os
import joblib
from .data_loader import ratings_and_movies
from .model_trainer import get_sparse_and_pivot_tables, train_model

script_directory = os.path.dirname(os.path.abspath(__file__))
model_directory = os.path.join(script_directory, "model")  

if not os.path.exists(model_directory):
    os.makedirs(model_directory)

model_save_path = os.path.join(model_directory, "model.joblib")

sparse_table, pivot_table = get_sparse_and_pivot_tables(ratings_and_movies)


def get_recomendations_model():
    try:
        model_data = joblib.load(model_save_path)
        print("Modelo carregado com sucesso.")
    except FileNotFoundError:
        print("Arquivo do modelo não encontrado. Treinando um novo modelo.")
        model_data = train_model(pivot_table)

    return model_data


def get_movie_index(movie_title: str):
    movie_index = pivot_table.index.get_loc(movie_title)
    return movie_index


def get_movie_attributes(movie_title: str):
    movie_index = get_movie_index(movie_title)
    movie_attributes = pivot_table.iloc[movie_index].values.reshape(1, -1)
    return movie_attributes


model = get_recomendations_model()
