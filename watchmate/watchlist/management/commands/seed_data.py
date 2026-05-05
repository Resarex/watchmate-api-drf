from django.core.management.base import BaseCommand
from watchlist.models import Genre, StreamPlatform, WatchList


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
        'storyline': 'A team of explorers travel through a wormhole in space to ensure humanity\'s survival.',
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
        'poster': 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsLegHnDmni1B.jpg',
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
        'storyline': 'The Avengers assemble once more to reverse Thanos\'s actions and restore balance to the universe.',
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
        'poster': 'https://image.tmdb.org/t/p/w500/rplLJ2hPcOQmkFhTqUte0MkosOe.jpg',
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
        'storyline': 'A young lion prince flees his kingdom after his father\'s murder and must reclaim his throne.',
        'platform': 'Disney+',
        'genres': ['Animation', 'Adventure', 'Drama'],
        'release_year': 1994,
        'duration': 88,
        'poster': 'https://image.tmdb.org/t/p/w500/sKCr78MXSuC27BpF4HHFxKMxnkp.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=4sj1MT05lAA',
    },
    {
        'title': 'Spider-Man: No Way Home',
        'storyline': 'Spider-Man asks Doctor Strange for help after his identity is revealed, unleashing the multiverse.',
        'platform': 'Netflix',
        'genres': ['Action', 'Adventure', 'Sci-Fi'],
        'release_year': 2021,
        'duration': 148,
        'poster': 'https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=JfVOs4VSpmA',
    },
    {
        'title': 'Dune',
        'storyline': 'A noble family becomes embroiled in a war for control of the universe\'s most valuable asset.',
        'platform': 'HBO Max',
        'genres': ['Sci-Fi', 'Adventure', 'Drama'],
        'release_year': 2021,
        'duration': 155,
        'poster': 'https://image.tmdb.org/t/p/w500/d5NXSklpcvksHi3nXBCTIJNFhBs.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=n9xhJrPXop4',
    },
    {
        'title': 'The Batman',
        'storyline': 'Batman ventures into Gotham\'s underworld to unmask the Riddler, a sadistic serial killer.',
        'platform': 'HBO Max',
        'genres': ['Action', 'Crime', 'Mystery'],
        'release_year': 2022,
        'duration': 176,
        'poster': 'https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpocon6I4AkyrRYv.jpg',
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


class Command(BaseCommand):
    help = 'Seeds the database with platforms, genres, and movies'

    def handle(self, *args, **options):
        self._seed_platforms()
        self._seed_genres()
        self._seed_movies()
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
                self.stdout.write(self.style.WARNING(f'  Platform not found: {data["platform"]}, skipping {data["title"]}'))
                continue

            movie, created = WatchList.objects.get_or_create(
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

            if created:
                genres = Genre.objects.filter(name__in=data['genres'])
                movie.genres.set(genres)
                self.stdout.write(f'  Created movie: {data["title"]}')
