from fastapi import FastAPI, Query
from training.reccomendation_engine import get_suggestion
from pydantic import BaseModel
from service.api import get_movie_details
import random

app = FastAPI()

print("[API Started]")


class Movie(BaseModel):
    name: str


# Endpoint para obter sugestões de filmes
@app.get("/get_suggestions")
def get_suggestions(movie_title: str = Query()):
    suggestions = get_suggestion(movie_title)

    # Escolhe uma sugestão aleatória, se houver sugestões
    if suggestions:
        random_suggestion = random.choice(suggestions)
        movie = get_movie_details(random_suggestion)
        return movie
    else:
        return {"message": "No suggestions available"}
