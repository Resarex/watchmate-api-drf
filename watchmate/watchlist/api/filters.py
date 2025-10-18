from django_filters import rest_framework as filters
from watchlist.models import WatchList


class WatchListFilter(filters.FilterSet):
    """Custom filters for WatchList"""
    
    # Filter by multiple genres (comma-separated IDs)
    genres = filters.BaseInFilter(field_name='genres__id', lookup_expr='in')
    
    # Filter by year range
    year_min = filters.NumberFilter(field_name='release_year', lookup_expr='gte')
    year_max = filters.NumberFilter(field_name='release_year', lookup_expr='lte')
    
    # Filter by rating range
    rating_min = filters.NumberFilter(field_name='avg_rating', lookup_expr='gte')
    rating_max = filters.NumberFilter(field_name='avg_rating', lookup_expr='lte')
    
    # Filter by duration range
    duration_min = filters.NumberFilter(field_name='duration', lookup_expr='gte')
    duration_max = filters.NumberFilter(field_name='duration', lookup_expr='lte')
    
    class Meta:
        model = WatchList
        fields = ['platform', 'active', 'release_year', 'genres']