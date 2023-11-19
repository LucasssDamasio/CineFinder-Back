import requests

API_KEY = "a8b2c4f03b827ba269c17ee47ee516c9"
BASE_URL = "https://api.themoviedb.org/3"

base_params = {
    'api_key': API_KEY,
    'language': 'pt-BR',
    'include_adults': False,
}

def get_movie_details(imdb_id: str):
    endpoint = f"{BASE_URL}/find/{imdb_id}?external_source=imdb_id"

    try:
        response = requests.get(endpoint, params=base_params)

        if response.status_code == 200:
            movie_data = response.json()
            return movie_data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None
