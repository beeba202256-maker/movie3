from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

MOVIES = [
    {
        "id": 1,
        "title": "Interstellar",
        "year": 2014,
        "genre": ["Sci-Fi", "Drama"],
        "rating": 8.7,
        "duration": "2h 49m",
        "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "poster": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg",
        "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E",
        "director": "Christopher Nolan",
        "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"]
    },
    {
        "id": 2,
        "title": "The Dark Knight",
        "year": 2008,
        "genre": ["Action", "Crime"],
        "rating": 9.0,
        "duration": "2h 32m",
        "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "poster": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/dqK9Hag1054tghRQSqLSfrkvQnA.jpg",
        "trailer": "https://www.youtube.com/embed/EXeTwQWrcwY",
        "director": "Christopher Nolan",
        "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"]
    },
    {
        "id": 3,
        "title": "Inception",
        "year": 2010,
        "genre": ["Sci-Fi", "Thriller"],
        "rating": 8.8,
        "duration": "2h 28m",
        "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "poster": "https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/s3TBrRGB1iav7gFOCNx3H31MoES.jpg",
        "trailer": "https://www.youtube.com/embed/YoHD9XEInc0",
        "director": "Christopher Nolan",
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"]
    },
    {
        "id": 4,
        "title": "Avengers: Endgame",
        "year": 2019,
        "genre": ["Action", "Adventure"],
        "rating": 8.4,
        "duration": "3h 1m",
        "description": "After the devastating events of Infinity War, the universe is in ruins. The Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe.",
        "poster": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/7RyHsO4yDXtBv1zUU3mTpHeQ0d5.jpg",
        "trailer": "https://www.youtube.com/embed/TcMBFSGVi1c",
        "director": "Anthony & Joe Russo",
        "cast": ["Robert Downey Jr.", "Chris Evans", "Mark Ruffalo"]
    },
    {
        "id": 5,
        "title": "Parasite",
        "year": 2019,
        "genre": ["Drama", "Thriller"],
        "rating": 8.5,
        "duration": "2h 12m",
        "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "poster": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/TU9NIjwzjoKPwQHoHshkFcQUCG.jpg",
        "trailer": "https://www.youtube.com/embed/5xH0HfJHsaY",
        "director": "Bong Joon-ho",
        "cast": ["Song Kang-ho", "Lee Sun-kyun", "Cho Yeo-jeong"]
    },
    {
        "id": 6,
        "title": "Dune",
        "year": 2021,
        "genre": ["Sci-Fi", "Adventure"],
        "rating": 8.0,
        "duration": "2h 35m",
        "description": "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset while its heir becomes troubled by visions of a dark future.",
        "poster": "https://wallpapercave.com/wp/wp10254425.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/jYEW5xZkZk2WTrdbMGAPFuBqbDc.jpg",
        "trailer": "https://www.youtube.com/embed/8g18jFHCLXk",
        "director": "Denis Villeneuve",
        "cast": ["Timothée Chalamet", "Rebecca Ferguson", "Oscar Isaac"]
    },
    {
        "id": 7,
        "title": "The Shawshank Redemption",
        "year": 1994,
        "genre": ["Drama"],
        "rating": 9.3,
        "duration": "2h 22m",
        "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "poster": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/kXfqcdQKsToO0OUXHcrrNCHDBzO.jpg",
        "trailer": "https://www.youtube.com/embed/6hB3S9bIaco",
        "director": "Frank Darabont",
        "cast": ["Tim Robbins", "Morgan Freeman", "Bob Gunton"]
    },
    {
        "id": 8,
        "title": "Oppenheimer",
        "year": 2023,
        "genre": ["Drama", "History"],
        "rating": 8.3,
        "duration": "3h 0m",
        "description": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II.",
        "poster": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/fm6KqXpkh7wm1k5qiCDHQQZLYkG.jpg",
        "trailer": "https://www.youtube.com/embed/uYPbbksJxIg",
        "director": "Christopher Nolan",
        "cast": ["Cillian Murphy", "Emily Blunt", "Matt Damon"]
    },
    {
        "id": 9,
        "title": "Spirited Away",
        "year": 2001,
        "genre": ["Animation", "Adventure", "Fantasy"],
        "rating": 8.6,
        "duration": "2h 5m",
        "description": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.",
        "poster": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/Ab8mkHmkYADjU7wQiOkia9BzGvS.jpg",
        "trailer": "https://www.youtube.com/embed/ByXuk9QqQkk",
        "director": "Hayao Miyazaki",
        "cast": ["Daveigh Chase", "Suzanne Pleshette", "Miyu Irino"]
    },
    {
        "id": 10,
        "title": "Joker",
        "year": 2019,
        "genre": ["Drama", "Crime", "Thriller"],
        "rating": 8.4,
        "duration": "2h 2m",
        "description": "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime.",
        "poster": "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/n6bUvigpRFqSwmPp1m2YADdbRBc.jpg",
        "trailer": "https://www.youtube.com/embed/zAGVQLHvwOY",
        "director": "Todd Phillips",
        "cast": ["Joaquin Phoenix", "Robert De Niro", "Zazie Beetz"]
    },
    {
        "id": 11,
        "title": "The Godfather",
        "year": 1972,
        "genre": ["Drama", "Crime"],
        "rating": 9.2,
        "duration": "2h 55m",
        "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        "poster": "https://images5.alphacoders.com/131/thumb-1920-1315822.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/tmU7GeKVybMWFButWEGl2M4GeiP.jpg",
        "trailer": "https://www.youtube.com/embed/sY1S34973zA",
        "director": "Francis Ford Coppola",
        "cast": ["Marlon Brando", "Al Pacino", "James Caan"]
    },
    {
        "id": 12,
        "title": "Whiplash",
        "year": 2014,
        "genre": ["Drama", "Music"],
        "rating": 8.5,
        "duration": "1h 47m",
        "description": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential.",
        "poster": "https://image.tmdb.org/t/p/w500/7fn624j5lj3xTme2SgiLCeuedmO.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/jvCD6k6t6kxj3rzb0Uf7VDkFUMq.jpg",
        "trailer": "https://www.youtube.com/embed/7d_jQycdQGo",
        "director": "Damien Chazelle",
        "cast": ["Miles Teller", "J.K. Simmons", "Paul Reiser"]
    },
    {
        "id": 13,
        "title": "Everything Everywhere All at Once",
        "year": 2022,
        "genre": ["Sci-Fi", "Action", "Comedy"],
        "rating": 7.8,
        "duration": "2h 19m",
        "description": "A middle-aged Chinese immigrant is swept up into an insane adventure in which she alone can save existence by exploring other universes and connecting with the lives she could have led.",
        "poster": "https://image.tmdb.org/t/p/w500/w3LxiVYdWWRvEVdn5RYq6jIqkb1.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/ss0Os3uWJfQAENILHZUdX8Tt1OC.jpg",
        "trailer": "https://www.youtube.com/embed/wxN1T1uxQ2g",
        "director": "Daniel Kwan & Daniel Scheinert",
        "cast": ["Michelle Yeoh", "Ke Huy Quan", "Jamie Lee Curtis"]
    },
    {
        "id": 14,
        "title": "The Grand Budapest Hotel",
        "year": 2014,
        "genre": ["Comedy", "Drama", "Adventure"],
        "rating": 8.1,
        "duration": "1h 39m",
        "description": "The adventures of Gustave H, a legendary concierge at a famous European hotel between the wars, and Zero Moustafa, the lobby boy who becomes his most trusted friend.",
        "poster": "https://image.tmdb.org/t/p/w500/eWdyYQreja6JGCzqHWXpWHDrrPo.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/iJQIbOPm81fPEGKt5BPuZmfnA54.jpg",
        "trailer": "https://www.youtube.com/embed/1Fg5iWmQjwk",
        "director": "Wes Anderson",
        "cast": ["Ralph Fiennes", "Tony Revolori", "Saoirse Ronan"]
    },
    {
        "id": 15,
        "title": "Mad Max: Fury Road",
        "year": 2015,
        "genre": ["Action", "Adventure", "Sci-Fi"],
        "rating": 8.1,
        "duration": "2h 0m",
        "description": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners, a psychotic worshiper, and a drifter named Max.",
        "poster": "https://image.tmdb.org/t/p/w500/8tZYtuWezp8JbcsvHYO0O46tFbo.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/phszHPFnhKBbkMM8Lo1Uorkgb3l.jpg",
        "trailer": "https://www.youtube.com/embed/hEJnMQG9ev8",
        "director": "George Miller",
        "cast": ["Tom Hardy", "Charlize Theron", "Nicholas Hoult"]
    },
    {
        "id": 16,
        "title": "Amélie",
        "year": 2001,
        "genre": ["Romance", "Comedy", "Drama"],
        "rating": 8.3,
        "duration": "2h 2m",
        "description": "Amélie is an innocent and naive girl in Paris with her own sense of justice. She decides to help those around her and, in the process, discovers love.",
        "poster": "https://i.pinimg.com/1200x/ca/ff/0f/caff0f5ae39909b277c8c55e021160c1.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/pJiirRHbfVJfxPEUXFRFUhMn9tP.jpg",
        "trailer": "https://www.youtube.com/embed/QexyKjFVR-U",
        "director": "Jean-Pierre Jeunet",
        "cast": ["Audrey Tautou", "Mathieu Kassovitz", "Rufus"]
    },
    {
        "id": 17,
        "title": "Blade Runner 2049",
        "year": 2017,
        "genre": ["Sci-Fi", "Drama", "Thriller"],
        "rating": 8.0,
        "duration": "2h 44m",
        "description": "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who's been missing for thirty years.",
        "poster": "https://image.tmdb.org/t/p/w500/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/sOHqdY9c1CcQO1k4f7HKQKWH7sH.jpg",
        "trailer": "https://www.youtube.com/embed/gCcx85zbxz4",
        "director": "Denis Villeneuve",
        "cast": ["Ryan Gosling", "Harrison Ford", "Ana de Armas"]
    },
    {
        "id": 18,
        "title": "Spider-Man: Into the Spider-Verse",
        "year": 2018,
        "genre": ["Animation", "Action", "Adventure"],
        "rating": 8.4,
        "duration": "1h 57m",
        "description": "Teen Miles Morales becomes the Spider-Man of his universe, and must join with five spider-powered individuals from other dimensions to stop a threat for all realities.",
        "poster": "https://image.tmdb.org/t/p/w500/iiZZdoQBEYBv6id8su7ImL0oCbD.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/9xeEGUZjgiKlI69jwIOi0hjKUIk.jpg",
        "trailer": "https://www.youtube.com/embed/tg52up16eq0",
        "director": "Bob Persichetti & Peter Ramsey",
        "cast": ["Shameik Moore", "Jake Johnson", "Hailee Steinfeld"]
    },
    {
        "id": 19,
        "title": "Oldboy",
        "year": 2003,
        "genre": ["Drama", "Thriller", "Crime"],
        "rating": 8.4,
        "duration": "2h 0m",
        "description": "After being inexplicably imprisoned for 15 years, Oh Dae-su is released, only to find himself trapped in another conspiracy as he searches for his captor.",
        "poster": "https://image.tmdb.org/t/p/w500/pWDtjs568ZfOTMbURQBYuT4Qxka.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/cHPGpIleE0hv2oH81Rd6NMmHMSJ.jpg",
        "trailer": "https://www.youtube.com/embed/2GaC4ykTO_Q",
        "director": "Park Chan-wook",
        "cast": ["Choi Min-sik", "Yoo Ji-tae", "Gang Hye-jung"]
    },
    {
        "id": 20,
        "title": "La La Land",
        "year": 2016,
        "genre": ["Romance", "Drama", "Music"],
        "rating": 8.0,
        "duration": "2h 8m",
        "description": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.",
        "poster": "https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg",
        "backdrop": "https://image.tmdb.org/t/p/w1280/3ENSZAqObIrngam6b5AXUl7GUwI.jpg",
        "trailer": "https://www.youtube.com/embed/0pdqf4P9MB8",
        "director": "Damien Chazelle",
        "cast": ["Ryan Gosling", "Emma Stone", "John Legend"]
    }
]

@app.route('/')
def index():
    return render_template('index.html', movies=MOVIES)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = next((m for m in MOVIES if m['id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('detail.html', movie=movie, movies=MOVIES)

@app.route('/api/movies')
def api_movies():
    genre = request.args.get('genre', '')
    search = request.args.get('search', '').lower()
    sort = request.args.get('sort', '')

    filtered = MOVIES
    if genre:
        filtered = [m for m in filtered if genre in m['genre']]
    if search:
        filtered = [m for m in filtered if search in m['title'].lower() or search in m['description'].lower()]

    if sort == 'rating':
        filtered = sorted(filtered, key=lambda x: x['rating'], reverse=True)
    elif sort == 'year':
        filtered = sorted(filtered, key=lambda x: x['year'], reverse=True)
    elif sort == 'title':
        filtered = sorted(filtered, key=lambda x: x['title'])

    return jsonify(filtered)

@app.route('/api/movies/<int:movie_id>')
def api_movie(movie_id):
    movie = next((m for m in MOVIES if m['id'] == movie_id), None)
    if not movie:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(movie)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
