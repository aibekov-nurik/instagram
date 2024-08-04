# inst_web/views.py
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from accounts.models import Subscription
from .forms import PostForm
from .models import Post, Comment


@login_required
def home_view(request):
    subscriptions = Subscription.objects.filter(follower=request.user)
    followed_users = [sub.following for sub in subscriptions]
    posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})
@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', post_id=post.id)

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    text = request.POST.get('text')
    if text:
        Comment.objects.create(post=post, user=request.user, text=text)
    return redirect('post_detail', post_id=post.id)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('created_at')
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'post_detail.html', context)