from django.contrib import admin
from watchlist.models import (
    WatchList, StreamPlatform, Review, Genre, 
    UserProfile, UserWatchlist, Person, Credit
)

# Register your models here.

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(StreamPlatform)
class StreamPlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'website']
    search_fields = ['name']


@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ['title', 'platform', 'release_year', 'avg_rating', 'number_rating', 'active', 'created']
    list_filter = ['active', 'platform', 'genres', 'release_year']
    search_fields = ['title', 'storyline']
    filter_horizontal = ['genres']
    list_editable = ['active']
    date_hierarchy = 'created'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['watchlist', 'review_user', 'rating', 'is_spoiler', 'helpful_count', 'active', 'created']
    list_filter = ['rating', 'active', 'is_spoiler', 'created']
    search_fields = ['watchlist__title', 'review_user__username', 'description']
    list_editable = ['active']
    date_hierarchy = 'created'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'created']
    search_fields = ['user__username', 'bio', 'location']


@admin.register(UserWatchlist)
class UserWatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'watchlist', 'status', 'added_date']
    list_filter = ['status', 'added_date']
    search_fields = ['user__username', 'watchlist__title']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date']
    search_fields = ['name', 'bio']


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ['person', 'watchlist', 'role', 'character_name', 'order']
    list_filter = ['role']
    search_fields = ['person__name', 'watchlist__title', 'character_name']
    list_editable = ['order']