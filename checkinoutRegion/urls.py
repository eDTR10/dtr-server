from django.urls import path
from .views import (
    AdminCheckinOutRegionViewSet,
    UserCheckinOutRegionViewSet,
    BulkCreateCheckinOutRegionView
)

urlpatterns = [
    # Admin routes
    path('all/', AdminCheckinOutRegionViewSet.as_view({
        'get': 'list', 
        'post': 'create'
    }), name='checkinoutregion-list-create'),
    
    path('user-all/', AdminCheckinOutRegionViewSet.as_view({
        'get': 'list', 
        'post': 'create'
    }), name='checkinoutregion-list-create'),

    # Base create route
    path('', AdminCheckinOutRegionViewSet.as_view({
        'post': 'create'
    }), name='checkinoutregion-create'),

    # Single record operations
    path('<int:pk>/', AdminCheckinOutRegionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='checkinoutregion-detail'),

    # Today's records
    path('today/', AdminCheckinOutRegionViewSet.as_view({
        'get': 'today_records'
    }), name='checkinoutregion-today-records'),

    # User routes
    path('user_filter_by_user_date/', UserCheckinOutRegionViewSet.as_view(), 
        name='user-checkinoutregion-list'),

    # Bulk operations
    path('bulk/', BulkCreateCheckinOutRegionView.as_view(), 
        name='bulk-create-checkinoutregion'),
]