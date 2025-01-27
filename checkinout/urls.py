from django.urls import path
from .views import AdminCheckinOutViewSet,UserCheckinOutViewSet,BulkCreateCheckinOutView

urlpatterns = [
    # All records (GET restricted by acc_lvl=14) and create new record
    path('all/', AdminCheckinOutViewSet.as_view({'get': 'list', 'post': 'create'}), name='checkinout-list-create'),
    path('user-all/', AdminCheckinOutViewSet.as_view({'get': 'list', 'post': 'create'}), name='checkinout-list-create'),


    # Create a new record (alternative route to 'all/' POST)
    path('', AdminCheckinOutViewSet.as_view({'post': 'create'}), name='checkinout-create'),

    # Retrieve, update, or delete a specific record by primary key
    path('<int:pk>/', AdminCheckinOutViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='checkinout-detail'),

    # Get records for the currently authenticated user (filtered by today's date)
    path('my_records/', AdminCheckinOutViewSet.as_view({'get': 'my_records'}), name='checkinout-my-records'),

    # Get records for a specific user (restricted by acc_lvl=14)
    path('by_user/', AdminCheckinOutViewSet.as_view({'get': 'by_user'}), name='checkinout-by-user'),

    # Get all records for the current day (restricted by acc_lvl=14)
    path('today/', AdminCheckinOutViewSet.as_view({'get': 'today_records'}), name='checkinout-today-records'),
    path('filter_by_user_date/', AdminCheckinOutViewSet.as_view({'post': 'filter_by_user_date'}), name='checkinout-filter-by-user-date'),
    path('user_filter_by_user_date/', UserCheckinOutViewSet.as_view(), name='user-list'),
    path('bulk/', BulkCreateCheckinOutView.as_view(), name='bulk-create-checkinout'),
]
