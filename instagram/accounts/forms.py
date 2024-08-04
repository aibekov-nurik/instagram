from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
    name = forms.CharField(max_length=100, required=False)
    info = forms.CharField(widget=forms.Textarea, required=False)
    phone = forms.CharField(max_length=15, required=False)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'password1', 'password2', 'name', 'info', 'phone', 'gender']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")
