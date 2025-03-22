from django.urls import path
from . import views

app_name='insta_app'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('search/', views.search_posts, name='search_posts'),
    path('create-post/', views.create_post, name='create_post'), 
    path('profile/', views.my_profile, name='my_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('notifications/', views.notifications, name='notifications'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),

    
]