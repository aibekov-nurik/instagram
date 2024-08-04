# accounts/models.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.shortcuts import get_object_or_404, redirect

from instagram import settings

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    post_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)


class Subscription(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} follows {self.following}'

# accounts/views.py
from django.contrib.auth import get_user_model

User = get_user_model()

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
