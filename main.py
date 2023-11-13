from fastapi import FastAPI, HTTPException
from src.recomendacao import get_suggestion
from pydantic import BaseModel
from src.service.api import get_movie_details
app = FastAPI()
print('Started API')

class Movie(BaseModel):
    name: str

@app.post("/suggestion/")
def read_root(movie: Movie):
    suggestions = get_suggestion(movie.name)
    movies = []
    for suggestion in suggestions:
        movie = get_movie_details(suggestion)
        movies.append(movie)

    return {"suggestions": movies}


