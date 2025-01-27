from django.urls import path
from .views import HolidayViewSet

urlpatterns = [
    path('', HolidayViewSet.as_view(), name='holiday-list'),  # Handles POST (create) and GET (list)
    path('<int:pk>/', HolidayViewSet.as_view(), name='get_holiday'),  # GET a single holiday by ID
    path('update/<int:pk>/', HolidayViewSet.as_view(), name='update_holiday'),  # PUT to update holiday
    path('delete/<int:pk>/', HolidayViewSet.as_view(), name='delete_holiday'),  # DELETE holiday
]
