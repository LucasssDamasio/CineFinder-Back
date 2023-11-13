
import os
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix


# Diretório onde o script está localizado
script_directory = os.path.dirname(os.path.abspath(__file__))
csv_directory = os.path.join(script_directory, 'csv')

# Função para carregar os dados dos filmes
def load_movies():
    movies_file = os.path.join(csv_directory, 'movies_metadata.csv')
    movies = pd.read_csv(movies_file)
    movies = movies[['id', 'original_title', 'original_language', 'vote_count', 'imdb_id']]
    movies.rename(columns={'id': 'MOVIE_ID', 'original_title': 'TITLE', 'original_language': 'LANGUAGE', 'vote_count': 'VOTE_COUNT', 'imdb_id': 'IMDB_ID'}, inplace=True)
    movies.dropna(inplace=True)
    movies = movies[movies['VOTE_COUNT'] > 999]

    movies = movies[movies['LANGUAGE'] == 'en']
    movies['MOVIE_ID'] = movies['MOVIE_ID'].astype(int)

    return movies

# Função para carregar os dados das avaliações
def load_ratings():
    ratings_file = os.path.join(csv_directory, 'ratings.csv')
    ratings = pd.read_csv(ratings_file)
    ratings = ratings[['userId', 'movieId', 'rating']]
    ratings.rename(columns={'userId': 'USER_ID', 'movieId': 'MOVIE_ID', 'rating': 'RATING'}, inplace=True)

    user_ratings_count = ratings['USER_ID'].value_counts() > 999
    valid_users = user_ratings_count[user_ratings_count].index

    ratings = ratings[ratings['USER_ID'].isin(valid_users)]

    return ratings

# Função para processar e combinar os dados de filmes e avaliações
def combine_ratings_and_movies(ratings, movies):

    ratings_and_movies = ratings.merge(movies, on='MOVIE_ID')
    ratings_and_movies.head()

    ratings_and_movies.drop_duplicates(['USER_ID', 'MOVIE_ID'], inplace=True)
    del ratings_and_movies['MOVIE_ID']

    return ratings_and_movies

# Função para criar uma tabela esparsa para recomendações
def get_sparse_and_pivot_tables(data):
    print('AAAAAAAAAAAAAAAAAAAA')
    print(data)
    pivot_table = data.pivot_table(columns='USER_ID', index='TITLE', values='RATING')
    pivot_table.fillna(0, inplace=True)
    sparse_table = csr_matrix(pivot_table)

    return sparse_table, pivot_table

# Função para treinar o modelo de recomendação
def train_model(pivot_table):
    sparse_table = csr_matrix(pivot_table)
    
    model = NearestNeighbors(algorithm='brute')
    model.fit(sparse_table)
    
    return model

movies_data = load_movies()
ratings_data = load_ratings()
ratings_and_movies_data = combine_ratings_and_movies(ratings_data, movies_data)
sparse_table, pivot_table = get_sparse_and_pivot_tables(ratings_and_movies_data)
model_data = train_model(sparse_table)

def get_suggestion(movie_title):
    # Encontre o índice do filme com base no título
    movie_index = pivot_table.index.get_loc(movie_title)
    
    # Obtenha os índices dos filmes sugeridos
    _, suggestions = model_data.kneighbors(pivot_table.iloc[movie_index].values.reshape(1, -1))
    
    # Converta os índices dos filmes sugeridos em títulos
    suggested_movies = [pivot_table.index[i] for i in suggestions[0]]
    
    # Obtenha os IMDb IDs dos filmes sugeridos
    imdb_ids = []
    for movie_title in suggested_movies:
        imdb_id = movies_data.loc[movies_data['TITLE'] == movie_title, 'IMDB_ID'].values[0]
        imdb_ids.append(imdb_id)
    
    return imdb_ids