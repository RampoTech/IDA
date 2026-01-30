from django.urls import path
from .views import CustomLoginView, AdminUserCreateView, ProfileRedirectView, logout_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('create-user/', AdminUserCreateView.as_view(), name='create_user'),
    path('profile/', ProfileRedirectView.as_view(), name='profile_redirect'),
]
