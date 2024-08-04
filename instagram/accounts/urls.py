from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('search/', views.search_view, name='search'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('follow/<str:username>/', views.follow_view, name='follow'),
    path('unfollow/<str:username>/', views.unfollow_view, name='unfollow'),
    path('logout/', views.logout_view, name='logout'),
]
