# accounts/urls.py
from django.urls import path
from . import views
from .models import follow_view, unfollow_view
from .views import search_view, profile_view

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('search/', search_view, name='search'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('follow/<str:username>/', follow_view, name='follow'),
    path('unfollow/<str:username>/', unfollow_view, name='unfollow'),
    path('logout/', views.logout_view, name='logout'),


]
