# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout
from .models import Subscription
from .forms import RegisterForm, LoginForm, UserSearchForm
from inst_web.models import Post

User = get_user_model()

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    posts_count = posts.count()
    followers_count = Subscription.objects.filter(following=user).count()
    following_count = Subscription.objects.filter(follower=user).count()

    is_following = request.user.is_authenticated and Subscription.objects.filter(follower=request.user, following=user).exists()

    context = {
        'user': user,
        'posts': posts,
        'posts_count': posts_count,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    }

    return render(request, 'profile.html', context)

@login_required
def follow_view(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        Subscription.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile', username=username)

@login_required
def unfollow_view(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Subscription.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', username=username)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def search_view(request):
    query = request.GET.get('query')
    users = User.objects.none()

    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query)
        )

    context = {
        'form': UserSearchForm(),
        'users': users,
    }

    return render(request, 'search_results.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def home_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'home.html', context)