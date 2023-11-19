from .model_handler import model, pivot_table
from .data_loader import movies


def get_suggestion(movie_title: str):
    if movie_title not in pivot_table.index:
        return []

    movie_index = pivot_table.index.get_loc(movie_title)

    # Obter os vizinhos mais próximos usando o modelo
    _, suggestions = model.kneighbors(
        pivot_table.iloc[movie_index].values.reshape(1, -1)
    )

    # Converter os índices dos filmes sugeridos em títulos
    suggested_movies = [pivot_table.index[i] for i in suggestions[0]]

    # Obter os IMDb IDs dos filmes sugeridos
    imdb_ids = movies.loc[movies["TITLE"].isin(suggested_movies), "IMDB_ID"].tolist()

    return imdb_ids
