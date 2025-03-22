from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like, Comment
from .forms import RegisterForm, CommentForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import PostForm
from django.contrib.auth.models import User
from .models import Profile, Post
from .forms import ProfileForm
from django.conf import settings
from .models import *
from django.contrib.auth.models import User
from .models import Post, Like, Notification
from .forms import ProfileEditForm



# User Registration
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'insta_app/register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'insta_app/login.html')

# User Logout
def user_logout(request):
    logout(request)
    return redirect('/login')

# Feed View

@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    notification_count = 0
    if request.user.is_authenticated:
        notification_count = Notification.objects.filter(user=request.user, is_read=False).count()
    for post in posts:
        post.has_liked = post.like_set.filter(user=request.user).exists()
    return render(request, 'insta_app/feed.html', {'posts': posts , 'notification_count': notification_count})

# Like a Post
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if created:
        # Create a notification for the post owner
        Notification.objects.create(
            user=post.user,
            sender=request.user,
            notification_type=Notification.LIKE,
            post=post  # Ensure the post is set
        )
    else:
        like.delete()

    return redirect('/')


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'insta_app/post_detail.html', {'post': post})

# Add Comment
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect('/')

@login_required
def search_posts(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(
        Q(caption__icontains=query) | Q(user__username__icontains=query)
    )
    return render(request, 'insta_app/feed.html', {'posts': posts})


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('/')  # Redirect to the home page or post detail page
    else:
        form = PostForm()
    return render(request, 'insta_app/create_post.html', {'form': form})

def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    posts = Post.objects.filter(user=user).order_by('-created_at')

    # Calculate follower and following counts
    follower_count = profile.followers.count()  # Number of users following this profile
    following_count = profile.following.count()  # Number of users this profile is following

    return render(request, 'insta_app/profile.html', {
        'profile': profile,
        'posts': posts,
        'follower_count': follower_count,
        'following_count': following_count,
    })


def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'insta_app/edit_profile.html', {'form': form})


@login_required
def my_profile(request):
    return redirect('insta_app:profile', username=request.user.username)

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    profile_to_follow = user_to_follow.profile
    current_user_profile = request.user.profile

    if profile_to_follow in current_user_profile.following.all():
        current_user_profile.following.remove(profile_to_follow)
    else:
        current_user_profile.following.add(profile_to_follow)
        # Create a notification for the user being followed
        Notification.objects.create(
            user=user_to_follow,
            sender=request.user,
            notification_type=Notification.FOLLOW
        )

    return redirect('/', username=user_to_follow.username)


@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    notification_count = notifications.filter(is_read=False).count()
    # Mark notifications as read when the page is visited
    notifications.update(is_read=True)
    return render(request, 'insta_app/notification.html', {
        'notifications': notifications,
        'notification_count': notification_count,
    })

