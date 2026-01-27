from django.urls import path
from .views import RegisterView, CustomAuthToken, PendingUsersView, ApproveUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('manager/pending-users/', PendingUsersView.as_view(), name='pending_users'),
    path('manager/approve-user/<int:pk>/', ApproveUserView.as_view(), name='approve_user'),
]
