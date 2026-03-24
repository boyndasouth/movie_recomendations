import requests
import json
import serpapi

TMDB_API_KEY = "99c2eaac5c12acf7c27c2583fa730d8e"
SERP_API_KEY = "f2875a4a34314d7c67cb862e724b90f54e3d32b6c20498a926b88245b5677c23"

def movie_recomender(genre_id):
    movie_list = []
    for page in range(1, 6):
        url = "https://api.themoviedb.org/3/discover/movie"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5OWMyZWFhYzVjMTJhY2Y3YzI3YzI1ODNmYTczMGQ4ZSIsIm5iZiI6MTc3MjA2MDY5MC4xOTcsInN1YiI6IjY5OWY4MDEyMTliMjE5ZGY0OGY1YzdkYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Rr9Vcru9Cw54-GmFHu6P7cNftmYDZCROQblPhIxinFg"
        }

        params = {
            "api_key": TMDB_API_KEY,
            "with_genres": genre_id,
            "page": page
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()


        for movie in data['results']:
            movie_list.append({
                "id": movie['id'],
                "title": movie['original_title'],
                "movie_genre": movie['genre_ids'],
                "overview": movie['overview'],
                "vote_average": movie['vote_average'],
                "poster_path": movie['poster_path'],
                "release_date": movie['release_date']
            })

    return movie_list


def movie_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5OWMyZWFhYzVjMTJhY2Y3YzI3YzI1ODNmYTczMGQ4ZSIsIm5iZiI6MTc3MjA2MDY5MC4xOTcsInN1YiI6IjY5OWY4MDEyMTliMjE5ZGY0OGY1YzdkYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Rr9Vcru9Cw54-GmFHu6P7cNftmYDZCROQblPhIxinFg"
    }

    params = {
        "api_key" : TMDB_API_KEY,
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data['results'][0]['key']

def theatre_search(movie_name, zip_code):
    showtimes = []

    client = serpapi.Client(api_key=SERP_API_KEY)
    
    results = client.search({
        "q": movie_name + " theater",
        "location": zip_code,
        "hl": "en",
        "gl": "us"
    })

    """
    for showtime in results["showtimes"]:
        for theater in showtime["theaters"]:
            showtimes.append({
                "show_date" : showtime["date"],
                "theatre_name" : theater["name"],
                "address" : theater["address"]
            })
    """

    showtimes = [
        {
            "theatre_name": theater["name"],
            "date": showtime["date"],
            "address": theater["address"],
            "time": time,
            "type": showing["type"]
        }
        for showtime in results["showtimes"]
        for theater in showtime["theaters"]
        for showing in theater["showing"]
        for time in showing["time"]
    ]

    return showtimes