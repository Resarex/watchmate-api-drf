from rest_framework import serializers
from watchlist.models import (
    WatchList, StreamPlatform, Review, Genre,
    UserProfile, UserWatchlist, Person, Credit
)
from django.contrib.auth.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug', 'description']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'bio', 'birth_date']


class CreditSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    person_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Credit
        fields = ['id', 'person', 'person_id', 'role', 'character_name', 'order']


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        exclude = ("watchlist",)
        read_only_fields = ['helpful_count']


class WatchListSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source='platform.name', read_only=True)
    platform_id = serializers.PrimaryKeyRelatedField(
        queryset=StreamPlatform.objects.all(),
        source='platform',
        write_only=True
    )
    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        write_only=True,
        source='genres'
    )
    
    class Meta:
        model = WatchList
        fields = [
            'id', 'title', 'storyline', 'platform', 'platform_id',
            'genres', 'genre_ids', 'release_year', 'duration',
            'poster', 'trailer_url', 'avg_rating', 'number_rating',
            'active', 'created'
        ]


class WatchListDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with reviews and credits"""
    platform = serializers.CharField(source='platform.name', read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    credits = CreditSerializer(many=True, read_only=True)
    
    # Aggregate data
    actors = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()
    
    class Meta:
        model = WatchList
        fields = [
            'id', 'title', 'storyline', 'platform', 'genres',
            'release_year', 'duration', 'poster', 'trailer_url',
            'avg_rating', 'number_rating', 'active', 'created',
            'reviews', 'credits', 'actors', 'directors'
        ]
    
    def get_actors(self, obj):
        actors = obj.credits.filter(role='actor')[:5]  # Top 5 actors
        return CreditSerializer(actors, many=True).data
    
    def get_directors(self, obj):
        directors = obj.credits.filter(role='director')
        return CreditSerializer(directors, many=True).data


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    review_count = serializers.SerializerMethodField()
    watchlist_count = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'bio', 'location', 
                  'birth_date', 'created', 'review_count', 'watchlist_count']
        read_only_fields = ['created']
    
    def get_review_count(self, obj):
        return obj.user.review_set.count()
    
    def get_watchlist_count(self, obj):
        return obj.user.my_watchlist.count()


class UserWatchlistSerializer(serializers.ModelSerializer):
    watchlist_detail = WatchListSerializer(source='watchlist', read_only=True)
    watchlist_id = serializers.PrimaryKeyRelatedField(
        queryset=WatchList.objects.all(),
        source='watchlist',
        write_only=True
    )
    
    class Meta:
        model = UserWatchlist
        fields = ['id', 'watchlist_detail', 'watchlist_id', 'status', 'added_date']
        read_only_fields = ['added_date']



















