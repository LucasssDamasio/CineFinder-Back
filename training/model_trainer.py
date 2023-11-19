import os
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import joblib

script_directory = os.path.dirname(os.path.abspath(__file__))
model_directory = os.path.join(script_directory, "model")  # Novo diretório "model"

if not os.path.exists(model_directory):
    os.makedirs(model_directory)

model_save_path = os.path.join(model_directory, "model.joblib")


# Função para criar uma tabela esparsa para recomendações
def get_sparse_and_pivot_tables(data):
    pivot_table = data.pivot_table(columns="USER_ID", index="TITLE", values="RATING")
    pivot_table.fillna(0, inplace=True)
    sparse_table = csr_matrix(pivot_table)

    return sparse_table, pivot_table


# Função para treinar o modelo de recomendação
def train_model(pivot_table):
    print("Training model...")
    sparse_table = csr_matrix(pivot_table)

    model = NearestNeighbors(algorithm="brute")
    model.fit(sparse_table)

    joblib.dump(model, model_save_path)

    return model
