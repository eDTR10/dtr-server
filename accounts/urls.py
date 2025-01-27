from django.urls import path
from .views import ListUsersView,ListUsersViewSummary,UsersDetails,ListUsersViewForReport,BulkCreateUsersView

urlpatterns = [
    path('all/', ListUsersView.as_view(), name='user-list'),

    path('all-users/', ListUsersViewForReport.as_view(), name='user-list'),
     path('update/<int:id>/', ListUsersView.as_view(), name='user-detail'),
     path('user_update/', UsersDetails.as_view(), name='user-detail'),

    path('userDetails/', UsersDetails.as_view(), name='user-list'),
    path('summary/', ListUsersViewSummary.as_view(), name='user-list'),
    path('bulk/', BulkCreateUsersView.as_view(), name='bulk-create-users')

    # other paths...
]

