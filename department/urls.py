from django.urls import path
from .views import AdminDeparmentViewSet

urlpatterns = [
    # List all departments (GET) or create a new department (POST)
    path('all/', AdminDeparmentViewSet.as_view(), name='department-list-create'),

    # Get, update, or delete a specific department by its ID (GET, PUT, DELETE)
    path('<int:pk>/', AdminDeparmentViewSet.as_view(), name='department-detail'),
]
