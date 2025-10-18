from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from watchlist.api import pagination, permissions, serializers, throttling
from watchlist.models import (
    Review, StreamPlatform, WatchList, Genre,
    UserProfile, UserWatchlist, Person, Credit
)
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg, Q
from watchlist.api.filters import WatchListFilter


# ============================================
# GENRE VIEWS
# ============================================

class GenreListCreateView(generics.ListCreateAPIView):
    """List all genres or create new genre (admin only)"""
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a genre"""
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]


# ============================================
# REVIEW VIEWS
# ============================================

class UserReview(generics.ListAPIView):
    """Get all reviews by a specific user"""
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        
        # Check if user already reviewed this movie
        review_queryset = Review.objects.filter(
            watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")

        # FIXED: Correct average rating calculation
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            # Calculate total rating and divide by new count
            total_rating = watchlist.avg_rating * watchlist.number_rating
            new_rating = serializer.validated_data['rating']
            watchlist.avg_rating = (total_rating + new_rating) / (watchlist.number_rating + 1)

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    """List all reviews for a specific movie"""
    serializer_class = serializers.ReviewSerializer
    throttle_classes = [throttling.ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active', 'rating', 'is_spoiler']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a review"""
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle, AnonRateThrottle]
    throttle_scope = 'review-detail'


# ============================================
# STREAM PLATFORM VIEWS
# ============================================

class StreamPlatformVS(viewsets.ModelViewSet):
    """ViewSet for StreamPlatform CRUD operations"""
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]


# ============================================
# WATCHLIST VIEWS
# ============================================

class WatchListGV(generics.ListCreateAPIView):
    """
    List all movies/shows with search, filter, and ordering
    GET: List with filters
    POST: Create new movie (admin only)
    """
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    
    # Search, Filter, and Ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = WatchListFilter  # Use custom filter
    search_fields = ['title', 'storyline']
    ordering_fields = ['avg_rating', 'created', 'title', 'release_year', 'duration']
    

class WatchListAV(APIView):
    """
    DEPRECATED: Use WatchListGV instead
    Kept for backward compatibility
    """
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = serializers.WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    """Get, update or delete a specific movie/show"""
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.WatchListDetailSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = serializers.WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SimilarMoviesView(generics.ListAPIView):
    """Get similar movies based on genre and platform"""
    serializer_class = serializers.WatchListSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        movie = get_object_or_404(WatchList, pk=pk)
        
        # Get movies with at least one matching genre
        similar = WatchList.objects.filter(
            genres__in=movie.genres.all(),
            active=True
        ).exclude(pk=pk).distinct()[:10]
        
        return similar


# ============================================
# USER PROFILE VIEWS
# ============================================

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get or update user's own profile"""
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        # Get or create profile for current user
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class PublicUserProfileView(generics.RetrieveAPIView):
    """View any user's public profile"""
    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'


# ============================================
# USER WATCHLIST VIEWS
# ============================================

class MyWatchlistView(generics.ListCreateAPIView):
    """
    Get current user's watchlist or add movie to watchlist
    """
    serializer_class = serializers.UserWatchlistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserWatchlist.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyWatchlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Update or remove movie from user's watchlist"""
    serializer_class = serializers.UserWatchlistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserWatchlist.objects.filter(user=self.request.user)


# ============================================
# PERSON & CREDIT VIEWS
# ============================================

class PersonListCreateView(generics.ListCreateAPIView):
    """List all people or create new person (admin only)"""
    queryset = Person.objects.all()
    serializer_class = serializers.PersonSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update or delete person details"""
    queryset = Person.objects.all()
    serializer_class = serializers.PersonSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]


class CreditListCreateView(generics.ListCreateAPIView):
    """List or create credits for a movie"""
    serializer_class = serializers.CreditSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Credit.objects.filter(watchlist_id=pk)
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = get_object_or_404(WatchList, pk=pk)
        serializer.save(watchlist=watchlist)
        
        
# ============================================
# TRENDING & STATISTICS VIEWS
# ============================================

from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg, Q

class TrendingMoviesView(generics.ListAPIView):
    """Get trending movies (most reviewed in last 7 days)"""
    serializer_class = serializers.WatchListSerializer
    
    def get_queryset(self):
        seven_days_ago = timezone.now() - timedelta(days=7)
        
        # Get movies with most reviews in last 7 days
        trending = WatchList.objects.filter(
            reviews__created__gte=seven_days_ago,
            active=True
        ).annotate(
            recent_review_count=Count('reviews')
        ).order_by('-recent_review_count')[:10]
        
        return trending


class PopularMoviesView(generics.ListAPIView):
    """Get most popular movies (highest rated with minimum reviews)"""
    serializer_class = serializers.WatchListSerializer
    
    def get_queryset(self):
        # Movies with at least 5 reviews and high ratings
        return WatchList.objects.filter(
            number_rating__gte=5,
            active=True
        ).order_by('-avg_rating', '-number_rating')[:20]


class RecentMoviesView(generics.ListAPIView):
    """Get recently added movies"""
    serializer_class = serializers.WatchListSerializer
    queryset = WatchList.objects.filter(active=True).order_by('-created')[:20]


class TopRatedMoviesView(generics.ListAPIView):
    """Get top rated movies of all time"""
    serializer_class = serializers.WatchListSerializer
    
    def get_queryset(self):
        return WatchList.objects.filter(
            number_rating__gte=10,  # At least 10 reviews
            active=True
        ).order_by('-avg_rating')[:50]


class MovieStatisticsView(APIView):
    """Get overall statistics about the platform"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        total_movies = WatchList.objects.filter(active=True).count()
        total_reviews = Review.objects.filter(active=True).count()
        total_users = User.objects.count()
        total_platforms = StreamPlatform.objects.count()
        
        # Average rating across all movies
        avg_rating = WatchList.objects.filter(
            number_rating__gt=0
        ).aggregate(Avg('avg_rating'))['avg_rating__avg']
        
        # Most active users (by review count)
        top_reviewers = User.objects.annotate(
            review_count=Count('review')
        ).order_by('-review_count')[:5]
        
        top_reviewers_data = [
            {
                'username': user.username,
                'review_count': user.review_count
            } for user in top_reviewers
        ]
        
        # Most reviewed movie
        most_reviewed = WatchList.objects.order_by('-number_rating').first()
        
        data = {
            'total_movies': total_movies,
            'total_reviews': total_reviews,
            'total_users': total_users,
            'total_platforms': total_platforms,
            'average_rating': round(avg_rating, 2) if avg_rating else 0,
            'top_reviewers': top_reviewers_data,
            'most_reviewed_movie': {
                'id': most_reviewed.id,
                'title': most_reviewed.title,
                'review_count': most_reviewed.number_rating
            } if most_reviewed else None
        }
        
        return Response(data)


class UserStatisticsView(APIView):
    """Get statistics for current user"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # User's review stats
        total_reviews = user.review_set.count()
        avg_user_rating = user.review_set.aggregate(
            Avg('rating')
        )['rating__avg']
        
        # User's watchlist stats
        watchlist_stats = user.my_watchlist.aggregate(
            total=Count('id'),
            want_to_watch=Count('id', filter=Q(status='want_to_watch')),
            watching=Count('id', filter=Q(status='watching')),
            watched=Count('id', filter=Q(status='watched'))
        )
        
        # Favorite genre (most reviewed)
        favorite_genres = Genre.objects.filter(
            movies__reviews__review_user=user
        ).annotate(
            review_count=Count('movies__reviews')
        ).order_by('-review_count')[:3]
        
        favorite_genres_data = [
            {'name': genre.name, 'count': genre.review_count}
            for genre in favorite_genres
        ]
        
        data = {
            'total_reviews': total_reviews,
            'average_rating': round(avg_user_rating, 2) if avg_user_rating else 0,
            'watchlist': watchlist_stats,
            'favorite_genres': favorite_genres_data,
        }
        
        return Response(data)


# ============================================
# REVIEW VOTING (HELPFUL/UNHELPFUL)
# ============================================

class ReviewHelpfulView(APIView):
    """Mark a review as helpful"""
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    def post(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            review.helpful_count += 1
            review.save()
            
            return Response({
                'message': 'Review marked as helpful',
                'helpful_count': review.helpful_count
            }, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response({
                'error': 'Review not found'
            }, status=status.HTTP_404_NOT_FOUND)
