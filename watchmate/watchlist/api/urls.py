from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist.api import views

router = DefaultRouter()
router.register('stream', views.StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    # Stream Platform (via router)
    path('', include(router.urls)),
    
    # WatchList/Movies
    path('list/', views.WatchListGV.as_view(), name='movie-list'),  # NEW: with search/filter
    path('list-old/', views.WatchListAV.as_view(), name='movie-list-old'),  # Old endpoint
    path('<int:pk>/', views.WatchDetailAV.as_view(), name='movie-details'),
    path('<int:pk>/similar/', views.SimilarMoviesView.as_view(), name='similar-movies'),  # NEW
    
    # Reviews
    path('<int:pk>/reviews/create/', views.ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', views.ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),
    path('user-reviews/', views.UserReview.as_view(), name='user-review-detail'),
    
    # Genres (NEW)
    path('genres/', views.GenreListCreateView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', views.GenreDetailView.as_view(), name='genre-detail'),
    
    # User Profile (NEW)
    path('profile/me/', views.UserProfileView.as_view(), name='my-profile'),
    path('profile/<str:username>/', views.PublicUserProfileView.as_view(), name='user-profile'),
    
    # User Watchlist (NEW)
    path('my-watchlist/', views.MyWatchlistView.as_view(), name='my-watchlist'),
    path('my-watchlist/<int:pk>/', views.MyWatchlistDetailView.as_view(), name='my-watchlist-detail'),
    
    # People & Credits (NEW)
    path('people/', views.PersonListCreateView.as_view(), name='person-list'),
    path('people/<int:pk>/', views.PersonDetailView.as_view(), name='person-detail'),
    path('<int:pk>/credits/', views.CreditListCreateView.as_view(), name='credit-list'),
    
    # Trending & Statistics (PHASE 2)
    path('trending/', views.TrendingMoviesView.as_view(), name='trending-movies'),
    path('popular/', views.PopularMoviesView.as_view(), name='popular-movies'),
    path('recent/', views.RecentMoviesView.as_view(), name='recent-movies'),
    path('top-rated/', views.TopRatedMoviesView.as_view(), name='top-rated-movies'),
    path('statistics/', views.MovieStatisticsView.as_view(), name='movie-statistics'),
    path('my-statistics/', views.UserStatisticsView.as_view(), name='user-statistics'),
    
    # Review Voting (PHASE 2)
    path('reviews/<int:pk>/helpful/', views.ReviewHelpfulView.as_view(), name='review-helpful'),
]