from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Genre(models.Model):
    """Movie/Show genres like Action, Drama, Comedy, etc."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
    active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    
    # NEW FIELDS
    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(help_text="Duration in minutes", null=True, blank=True)
    poster = models.URLField(max_length=200, blank=True, help_text="URL to poster image")
    trailer_url = models.URLField(max_length=200, blank=True, help_text="YouTube trailer URL")

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']


class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    # NEW FIELDS
    is_spoiler = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.rating) + " | " + self.watchlist.title + " | " + str(self.review_user)
    
    class Meta:
        unique_together = ('review_user', 'watchlist')  # One review per user per movie
        ordering = ['-created']


class UserProfile(models.Model):
    """Extended user profile with additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class UserWatchlist(models.Model):
    """User's personal watchlist (movies they want to watch)"""
    STATUS_CHOICES = [
        ('want_to_watch', 'Want to Watch'),
        ('watching', 'Currently Watching'),
        ('watched', 'Watched'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_watchlist')
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='want_to_watch')
    added_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'watchlist')
        ordering = ['-added_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.watchlist.title}"


class Person(models.Model):
    """Actors, Directors, Writers, etc."""
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "People"
        ordering = ['name']


class Credit(models.Model):
    """Cast and Crew credits for movies/shows"""
    ROLE_CHOICES = [
        ('actor', 'Actor'),
        ('director', 'Director'),
        ('writer', 'Writer'),
        ('producer', 'Producer'),
    ]
    
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='credits')
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='credits')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    character_name = models.CharField(max_length=100, blank=True)  # For actors
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    
    class Meta:
        ordering = ['order', 'person__name']
        unique_together = ('person', 'watchlist', 'role', 'character_name')
    
    def __str__(self):
        if self.character_name:
            return f"{self.person.name} as {self.character_name} in {self.watchlist.title}"
        return f"{self.person.name} - {self.role} - {self.watchlist.title}"