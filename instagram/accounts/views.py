# accounts/views.py
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout
from .forms import RegisterForm, LoginForm, UserSearchForm

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


User = get_user_model()

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

User = get_user_model()

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()  # Используем related_name 'posts'

    context = {
        'user': user,
        'posts': posts,
    }

    return render(request, 'profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')