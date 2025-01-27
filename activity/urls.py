from django.urls import path
from .views import ActivityViewSet,AdminActivityViewSet

urlpatterns = [
    path('', ActivityViewSet.as_view(), name='activity-list'),  # Handles POST (create) and GET (list)
    path('<int:pk>/', AdminActivityViewSet.as_view(), name='activity-list'),  # Handles POST (create) and GET (list)
    path('<int:pk>/', ActivityViewSet.as_view(), name='get_activity'),  # GET a single activity by ID
    path('update/<int:pk>/', ActivityViewSet.as_view(), name='update_activity'),  # PUT to update activity
    path('delete/<int:pk>/', ActivityViewSet.as_view(), name='delete_activity'),  # DELETE activity
]
