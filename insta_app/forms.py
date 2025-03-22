# posts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment
from .models import Profile

# User Registration Form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Post Creation Form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']

# Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

#Create Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']

#Profile Page
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']