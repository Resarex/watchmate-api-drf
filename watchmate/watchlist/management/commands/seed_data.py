from django.core.management.base import BaseCommand
from watchlist.models import Credit, Genre, Person, StreamPlatform, WatchList


PLATFORMS = [
    {
        'name': 'Netflix',
        'about': 'Global streaming platform with movies, TV shows, and originals.',
        'website': 'https://www.netflix.com',
    },
    {
        'name': 'Amazon Prime Video',
        'about': 'Amazon streaming service with movies, series, and originals.',
        'website': 'https://www.primevideo.com',
    },
    {
        'name': 'Disney+',
        'about': 'Home of Disney, Marvel, Star Wars, Pixar, and National Geographic.',
        'website': 'https://www.disneyplus.com',
    },
    {
        'name': 'HBO Max',
        'about': 'Premium streaming with HBO, DC, and Warner Bros content.',
        'website': 'https://www.max.com',
    },
    {
        'name': 'Apple TV+',
        'about': "Apple's streaming service with original films and series.",
        'website': 'https://tv.apple.com',
    },
]

GENRES = [
    {'name': 'Action',    'slug': 'action',    'description': 'High-energy films with physical stunts and combat.'},
    {'name': 'Drama',     'slug': 'drama',     'description': 'Character-driven stories with emotional depth.'},
    {'name': 'Comedy',    'slug': 'comedy',    'description': 'Films designed to entertain and make you laugh.'},
    {'name': 'Thriller',  'slug': 'thriller',  'description': 'Suspenseful films that keep you on the edge of your seat.'},
    {'name': 'Sci-Fi',    'slug': 'sci-fi',    'description': 'Science fiction exploring futuristic concepts.'},
    {'name': 'Horror',    'slug': 'horror',    'description': 'Films designed to frighten and unsettle.'},
    {'name': 'Romance',   'slug': 'romance',   'description': 'Stories centered around love and relationships.'},
    {'name': 'Animation', 'slug': 'animation', 'description': 'Animated films for all ages.'},
    {'name': 'Crime',     'slug': 'crime',     'description': 'Films involving criminal activities and investigations.'},
    {'name': 'Adventure', 'slug': 'adventure', 'description': 'Exciting journeys and explorations.'},
    {'name': 'Fantasy',   'slug': 'fantasy',   'description': 'Magical worlds and supernatural elements.'},
    {'name': 'Mystery',   'slug': 'mystery',   'description': 'Puzzling stories with secrets to uncover.'},
]

MOVIES = [
    {
        'title': 'The Dark Knight',
        'storyline': 'Batman faces the Joker, a criminal mastermind who plunges Gotham City into anarchy.',
        'platform': 'Netflix',
        'genres': ['Action', 'Crime', 'Drama'],
        'release_year': 2008,
        'duration': 152,
        'poster': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=EXeTwQWrcwY',
    },
    {
        'title': 'Inception',
        'storyline': 'A thief who steals secrets through dreams is given a chance to have his past erased.',
        'platform': 'Netflix',
        'genres': ['Sci-Fi', 'Action', 'Thriller'],
        'release_year': 2010,
        'duration': 148,
        'poster': 'https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=YoHD9XEInc0',
    },
    {
        'title': 'Interstellar',
        'storyline': "A team of explorers travel through a wormhole in space to ensure humanity's survival.",
        'platform': 'Amazon Prime Video',
        'genres': ['Sci-Fi', 'Drama', 'Adventure'],
        'release_year': 2014,
        'duration': 169,
        'poster': 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=zSWdZVtXT7E',
    },
    {
        'title': 'The Shawshank Redemption',
        'storyline': 'Two imprisoned men bond over years, finding solace and redemption through acts of decency.',
        'platform': 'Amazon Prime Video',
        'genres': ['Drama', 'Crime'],
        'release_year': 1994,
        'duration': 142,
        'poster': 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=6hB3S9bIaco',
    },
    {
        'title': 'Pulp Fiction',
        'storyline': 'The lives of two mob hitmen, a boxer, and a gangster intertwine in four tales of violence.',
        'platform': 'Netflix',
        'genres': ['Crime', 'Drama', 'Thriller'],
        'release_year': 1994,
        'duration': 154,
        'poster': 'https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=s7EdQ4FqbhY',
    },
    {
        'title': 'The Godfather',
        'storyline': 'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.',
        'platform': 'Amazon Prime Video',
        'genres': ['Crime', 'Drama'],
        'release_year': 1972,
        'duration': 175,
        'poster': 'https://image.tmdb.org/t/p/w500/wWJbBo5yjw22AIjE8isBFoiBI3S.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=sY1S34973zA',
    },
    {
        'title': 'Fight Club',
        'storyline': 'An insomniac office worker forms an underground fight club with a soap salesman.',
        'platform': 'HBO Max',
        'genres': ['Drama', 'Thriller'],
        'release_year': 1999,
        'duration': 139,
        'poster': 'https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=SUXWAEX2jlg',
    },
    {
        'title': 'Forrest Gump',
        'storyline': 'The story of a man with low IQ who witnesses and influences several defining moments in history.',
        'platform': 'Disney+',
        'genres': ['Drama', 'Comedy', 'Romance'],
        'release_year': 1994,
        'duration': 142,
        'poster': 'https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=bLvqoHBptjg',
    },
    {
        'title': 'The Matrix',
        'storyline': 'A hacker discovers the world is a simulation and joins a rebellion against its machine overlords.',
        'platform': 'HBO Max',
        'genres': ['Sci-Fi', 'Action'],
        'release_year': 1999,
        'duration': 136,
        'poster': 'https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=vKQi3bBA1y8',
    },
    {
        'title': 'Avengers: Endgame',
        'storyline': "The Avengers assemble once more to reverse Thanos's actions and restore balance to the universe.",
        'platform': 'Disney+',
        'genres': ['Action', 'Adventure', 'Sci-Fi'],
        'release_year': 2019,
        'duration': 181,
        'poster': 'https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=TcMBFSGVi1c',
    },
    {
        'title': 'Parasite',
        'storyline': 'A poor family schemes to become employed by a wealthy family, leading to dark consequences.',
        'platform': 'Amazon Prime Video',
        'genres': ['Drama', 'Thriller', 'Comedy'],
        'release_year': 2019,
        'duration': 132,
        'poster': 'https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=5xH0HfJHsaY',
    },
    {
        'title': 'Joker',
        'storyline': 'A failed comedian descends into madness and becomes the iconic villain of Gotham City.',
        'platform': 'HBO Max',
        'genres': ['Drama', 'Thriller', 'Crime'],
        'release_year': 2019,
        'duration': 122,
        'poster': 'https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=zAGVQLHvwOY',
    },
    {
        'title': 'The Silence of the Lambs',
        'storyline': 'A young FBI trainee seeks the help of an imprisoned cannibal to catch another serial killer.',
        'platform': 'Netflix',
        'genres': ['Horror', 'Thriller', 'Crime'],
        'release_year': 1991,
        'duration': 118,
        'poster': 'https://image.tmdb.org/t/p/w500/uS9m8OBk1A8eM9I042bx8XXpqAq.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=6iB21hailEc',
    },
    {
        'title': 'Goodfellas',
        'storyline': 'The rise and fall of Henry Hill and his mob associates in the New York crime world.',
        'platform': 'Netflix',
        'genres': ['Crime', 'Drama'],
        'release_year': 1990,
        'duration': 146,
        'poster': 'https://image.tmdb.org/t/p/w500/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=qo5jJpHtI1Y',
    },
    {
        'title': "Schindler's List",
        'storyline': 'In German-occupied Poland, Oskar Schindler saves the lives of over a thousand Jewish refugees.',
        'platform': 'Amazon Prime Video',
        'genres': ['Drama', 'Mystery'],
        'release_year': 1993,
        'duration': 195,
        'poster': 'https://image.tmdb.org/t/p/w500/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=gG22M75M5oE',
    },
    {
        'title': 'The Lion King',
        'storyline': "A young lion prince flees his kingdom after his father's murder and must reclaim his throne.",
        'platform': 'Disney+',
        'genres': ['Animation', 'Adventure', 'Drama'],
        'release_year': 1994,
        'duration': 88,
        'poster': 'https://image.tmdb.org/t/p/w500/sKCr78MXSLixwmZ8DyJLrpMsd15.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=4sj1MT05lAA',
    },
    {
        'title': 'Spider-Man: No Way Home',
        'storyline': "Spider-Man asks Doctor Strange for help after his identity is revealed, unleashing the multiverse.",
        'platform': 'Netflix',
        'genres': ['Action', 'Adventure', 'Sci-Fi'],
        'release_year': 2021,
        'duration': 148,
        'poster': 'https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=JfVOs4VSpmA',
    },
    {
        'title': 'Dune',
        'storyline': "A noble family becomes embroiled in a war for control of the universe's most valuable asset.",
        'platform': 'HBO Max',
        'genres': ['Sci-Fi', 'Adventure', 'Drama'],
        'release_year': 2021,
        'duration': 155,
        'poster': 'https://image.tmdb.org/t/p/w500/pc15b0pi8o1oUv9vNhakwMQ9TxA.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=n9xhJrPXop4',
    },
    {
        'title': 'The Batman',
        'storyline': "Batman ventures into Gotham's underworld to unmask the Riddler, a sadistic serial killer.",
        'platform': 'HBO Max',
        'genres': ['Action', 'Crime', 'Mystery'],
        'release_year': 2022,
        'duration': 176,
        'poster': 'https://image.tmdb.org/t/p/w500/djCPA8NYhhsDT1DVTViOgH4INqY.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=mqqft2x_Aa4',
    },
    {
        'title': 'Everything Everywhere',
        'storyline': 'A laundromat owner must connect with parallel universe versions of herself to save the world.',
        'platform': 'Amazon Prime Video',
        'genres': ['Sci-Fi', 'Comedy', 'Action'],
        'release_year': 2022,
        'duration': 139,
        'poster': 'https://image.tmdb.org/t/p/w500/w3LxiVYdWWRvEVdn5RYq6jIqkb1.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=wxN1T1uxQ2g',
    },
]

CAST = [
    {
        'movie': 'The Dark Knight',
        'credits': [
            {'name': 'Christopher Nolan', 'role': 'director', 'character_name': '', 'order': 0},
            {'name': 'Christian Bale',    'role': 'actor',    'character_name': 'Bruce Wayne / Batman', 'order': 1},
            {'name': 'Heath Ledger',      'role': 'actor',    'character_name': 'Joker',                'order': 2},
            {'name': 'Aaron Eckhart',     'role': 'actor',    'character_name': 'Harvey Dent',          'order': 3},
        ],
    },
    {
        'movie': 'Inception',
        'credits': [
            {'name': 'Christopher Nolan',       'role': 'director', 'character_name': '',        'order': 0},
            {'name': 'Leonardo DiCaprio',        'role': 'actor',    'character_name': 'Dom Cobb', 'order': 1},
            {'name': 'Joseph Gordon-Levitt',     'role': 'actor',    'character_name': 'Arthur',  'order': 2},
            {'name': 'Elliot Page',              'role': 'actor',    'character_name': 'Ariadne', 'order': 3},
        ],
    },
    {
        'movie': 'Interstellar',
        'credits': [
            {'name': 'Christopher Nolan',   'role': 'director', 'character_name': '',         'order': 0},
            {'name': 'Matthew McConaughey', 'role': 'actor',    'character_name': 'Cooper',   'order': 1},
            {'name': 'Anne Hathaway',       'role': 'actor',    'character_name': 'Brand',    'order': 2},
            {'name': 'Jessica Chastain',    'role': 'actor',    'character_name': 'Murph',    'order': 3},
        ],
    },
    {
        'movie': 'The Shawshank Redemption',
        'credits': [
            {'name': 'Frank Darabont', 'role': 'director', 'character_name': '',            'order': 0},
            {'name': 'Tim Robbins',    'role': 'actor',    'character_name': 'Andy Dufresne', 'order': 1},
            {'name': 'Morgan Freeman', 'role': 'actor',    'character_name': 'Red',           'order': 2},
        ],
    },
    {
        'movie': 'Pulp Fiction',
        'credits': [
            {'name': 'Quentin Tarantino',  'role': 'director', 'character_name': '',              'order': 0},
            {'name': 'John Travolta',      'role': 'actor',    'character_name': 'Vincent Vega',   'order': 1},
            {'name': 'Samuel L. Jackson',  'role': 'actor',    'character_name': 'Jules Winnfield', 'order': 2},
            {'name': 'Uma Thurman',        'role': 'actor',    'character_name': 'Mia Wallace',     'order': 3},
        ],
    },
    {
        'movie': 'The Godfather',
        'credits': [
            {'name': 'Francis Ford Coppola', 'role': 'director', 'character_name': '',                  'order': 0},
            {'name': 'Marlon Brando',         'role': 'actor',    'character_name': 'Don Vito Corleone', 'order': 1},
            {'name': 'Al Pacino',             'role': 'actor',    'character_name': 'Michael Corleone',  'order': 2},
            {'name': 'James Caan',            'role': 'actor',    'character_name': 'Sonny Corleone',    'order': 3},
        ],
    },
    {
        'movie': 'Fight Club',
        'credits': [
            {'name': 'David Fincher',       'role': 'director', 'character_name': '',             'order': 0},
            {'name': 'Brad Pitt',           'role': 'actor',    'character_name': 'Tyler Durden',  'order': 1},
            {'name': 'Edward Norton',       'role': 'actor',    'character_name': 'The Narrator',  'order': 2},
            {'name': 'Helena Bonham Carter','role': 'actor',    'character_name': 'Marla Singer',  'order': 3},
        ],
    },
    {
        'movie': 'Forrest Gump',
        'credits': [
            {'name': 'Robert Zemeckis', 'role': 'director', 'character_name': '',           'order': 0},
            {'name': 'Tom Hanks',       'role': 'actor',    'character_name': 'Forrest Gump', 'order': 1},
            {'name': 'Robin Wright',    'role': 'actor',    'character_name': 'Jenny',        'order': 2},
            {'name': 'Gary Sinise',     'role': 'actor',    'character_name': 'Lt. Dan',      'order': 3},
        ],
    },
    {
        'movie': 'The Matrix',
        'credits': [
            {'name': 'Lana Wachowski',    'role': 'director', 'character_name': '',      'order': 0},
            {'name': 'Lilly Wachowski',   'role': 'director', 'character_name': '',      'order': 1},
            {'name': 'Keanu Reeves',      'role': 'actor',    'character_name': 'Neo',   'order': 2},
            {'name': 'Laurence Fishburne','role': 'actor',    'character_name': 'Morpheus', 'order': 3},
            {'name': 'Carrie-Anne Moss',  'role': 'actor',    'character_name': 'Trinity', 'order': 4},
        ],
    },
    {
        'movie': 'Avengers: Endgame',
        'credits': [
            {'name': 'Anthony Russo',       'role': 'director', 'character_name': '',                    'order': 0},
            {'name': 'Joe Russo',           'role': 'director', 'character_name': '',                    'order': 1},
            {'name': 'Robert Downey Jr.',   'role': 'actor',    'character_name': 'Tony Stark / Iron Man', 'order': 2},
            {'name': 'Chris Evans',         'role': 'actor',    'character_name': 'Steve Rogers / Captain America', 'order': 3},
            {'name': 'Scarlett Johansson',  'role': 'actor',    'character_name': 'Natasha Romanoff',    'order': 4},
        ],
    },
    {
        'movie': 'Parasite',
        'credits': [
            {'name': 'Bong Joon-ho',    'role': 'director', 'character_name': '',             'order': 0},
            {'name': 'Song Kang-ho',    'role': 'actor',    'character_name': 'Ki-taek',       'order': 1},
            {'name': 'Lee Sun-kyun',    'role': 'actor',    'character_name': 'Park Dong-ik',  'order': 2},
            {'name': 'Cho Yeo-jeong',   'role': 'actor',    'character_name': 'Yeon-gyo',      'order': 3},
        ],
    },
    {
        'movie': 'Joker',
        'credits': [
            {'name': 'Todd Phillips',   'role': 'director', 'character_name': '',                      'order': 0},
            {'name': 'Joaquin Phoenix', 'role': 'actor',    'character_name': 'Arthur Fleck / Joker',  'order': 1},
            {'name': 'Robert De Niro',  'role': 'actor',    'character_name': 'Murray Franklin',       'order': 2},
            {'name': 'Zazie Beetz',     'role': 'actor',    'character_name': 'Sophie Dumond',         'order': 3},
        ],
    },
    {
        'movie': 'The Silence of the Lambs',
        'credits': [
            {'name': 'Jonathan Demme',   'role': 'director', 'character_name': '',                  'order': 0},
            {'name': 'Jodie Foster',     'role': 'actor',    'character_name': 'Clarice Starling',  'order': 1},
            {'name': 'Anthony Hopkins',  'role': 'actor',    'character_name': 'Hannibal Lecter',   'order': 2},
        ],
    },
    {
        'movie': 'Goodfellas',
        'credits': [
            {'name': 'Martin Scorsese', 'role': 'director', 'character_name': '',              'order': 0},
            {'name': 'Ray Liotta',      'role': 'actor',    'character_name': 'Henry Hill',    'order': 1},
            {'name': 'Robert De Niro',  'role': 'actor',    'character_name': 'Jimmy Conway',  'order': 2},
            {'name': 'Joe Pesci',       'role': 'actor',    'character_name': 'Tommy DeVito',  'order': 3},
        ],
    },
    {
        'movie': "Schindler's List",
        'credits': [
            {'name': 'Steven Spielberg', 'role': 'director', 'character_name': '',                  'order': 0},
            {'name': 'Liam Neeson',      'role': 'actor',    'character_name': 'Oskar Schindler',   'order': 1},
            {'name': 'Ben Kingsley',     'role': 'actor',    'character_name': 'Itzhak Stern',      'order': 2},
            {'name': 'Ralph Fiennes',    'role': 'actor',    'character_name': 'Amon Goeth',        'order': 3},
        ],
    },
    {
        'movie': 'The Lion King',
        'credits': [
            {'name': 'Roger Allers',    'role': 'director', 'character_name': '',       'order': 0},
            {'name': 'Rob Minkoff',     'role': 'director', 'character_name': '',       'order': 1},
            {'name': 'Matthew Broderick','role': 'actor',   'character_name': 'Simba',  'order': 2},
            {'name': 'Jeremy Irons',    'role': 'actor',    'character_name': 'Scar',   'order': 3},
            {'name': 'James Earl Jones','role': 'actor',    'character_name': 'Mufasa', 'order': 4},
        ],
    },
    {
        'movie': 'Spider-Man: No Way Home',
        'credits': [
            {'name': 'Jon Watts',               'role': 'director', 'character_name': '',                    'order': 0},
            {'name': 'Tom Holland',             'role': 'actor',    'character_name': 'Peter Parker / Spider-Man', 'order': 1},
            {'name': 'Zendaya',                 'role': 'actor',    'character_name': 'MJ',                  'order': 2},
            {'name': 'Benedict Cumberbatch',    'role': 'actor',    'character_name': 'Doctor Strange',      'order': 3},
        ],
    },
    {
        'movie': 'Dune',
        'credits': [
            {'name': 'Denis Villeneuve',  'role': 'director', 'character_name': '',               'order': 0},
            {'name': 'Timothee Chalamet', 'role': 'actor',    'character_name': 'Paul Atreides',  'order': 1},
            {'name': 'Rebecca Ferguson',  'role': 'actor',    'character_name': 'Lady Jessica',   'order': 2},
            {'name': 'Oscar Isaac',       'role': 'actor',    'character_name': 'Duke Leto',       'order': 3},
        ],
    },
    {
        'movie': 'The Batman',
        'credits': [
            {'name': 'Matt Reeves',      'role': 'director', 'character_name': '',                        'order': 0},
            {'name': 'Robert Pattinson', 'role': 'actor',    'character_name': 'Bruce Wayne / Batman',    'order': 1},
            {'name': 'Zoe Kravitz',      'role': 'actor',    'character_name': 'Selina Kyle / Catwoman',  'order': 2},
            {'name': 'Paul Dano',        'role': 'actor',    'character_name': 'The Riddler',             'order': 3},
        ],
    },
    {
        'movie': 'Everything Everywhere',
        'credits': [
            {'name': 'Daniel Kwan',      'role': 'director', 'character_name': '',                       'order': 0},
            {'name': 'Daniel Scheinert', 'role': 'director', 'character_name': '',                       'order': 1},
            {'name': 'Michelle Yeoh',    'role': 'actor',    'character_name': 'Evelyn Wang',             'order': 2},
            {'name': 'Ke Huy Quan',      'role': 'actor',    'character_name': 'Waymond Wang',            'order': 3},
            {'name': 'Jamie Lee Curtis', 'role': 'actor',    'character_name': 'Deirdre Beaubeirdre',     'order': 4},
        ],
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with platforms, genres, movies, and cast'

    def handle(self, *args, **options):
        self._seed_platforms()
        self._seed_genres()
        self._seed_movies()
        self._seed_cast()
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def _seed_platforms(self):
        for data in PLATFORMS:
            _, created = StreamPlatform.objects.get_or_create(
                name=data['name'],
                defaults={'about': data['about'], 'website': data['website']}
            )
            if created:
                self.stdout.write(f'  Created platform: {data["name"]}')

    def _seed_genres(self):
        for data in GENRES:
            _, created = Genre.objects.get_or_create(
                slug=data['slug'],
                defaults={'name': data['name'], 'description': data['description']}
            )
            if created:
                self.stdout.write(f'  Created genre: {data["name"]}')

    def _seed_movies(self):
        for data in MOVIES:
            try:
                platform = StreamPlatform.objects.get(name=data['platform'])
            except StreamPlatform.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f'  Platform not found: {data["platform"]}, skipping {data["title"]}'
                ))
                continue

            movie, created = WatchList.objects.update_or_create(
                title=data['title'],
                defaults={
                    'storyline': data['storyline'],
                    'platform': platform,
                    'release_year': data['release_year'],
                    'duration': data['duration'],
                    'poster': data['poster'],
                    'trailer_url': data['trailer_url'],
                    'active': True,
                }
            )

            genres = Genre.objects.filter(name__in=data['genres'])
            movie.genres.set(genres)

            if created:
                self.stdout.write(f'  Created movie: {data["title"]}')
            else:
                self.stdout.write(f'  Updated movie: {data["title"]}')

    def _seed_cast(self):
        for entry in CAST:
            try:
                movie = WatchList.objects.get(title=entry['movie'])
            except WatchList.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Movie not found: {entry["movie"]}, skipping cast'))
                continue

            for credit_data in entry['credits']:
                person, _ = Person.objects.get_or_create(name=credit_data['name'])
                _, created = Credit.objects.get_or_create(
                    person=person,
                    watchlist=movie,
                    role=credit_data['role'],
                    character_name=credit_data['character_name'],
                    defaults={'order': credit_data['order']}
                )
                if created:
                    self.stdout.write(f'    Added {credit_data["role"]}: {credit_data["name"]} → {entry["movie"]}')
