from django.urls import path

from .views import *
urlpatterns =[
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register_user/', register_user, name='register_user'),
    path('account_verify/<slug:token>/', account_verify, name='account_verify'),
    path('profile/', profile, name='profile'),
    path('profile_picture/', change_profile_picture, name='profile_picture'),
    path('view_user_info/<str:username>/', view_user_info, name='view_user_info'),
    path('follow_or_unfollow/<int:user_id>/', follow_or_unfollow_user, name='follow_or_unfollow_user'),
    path('user_notifications/',user_notifications, name='user_notifications'),
    path('mute_or_unmute_user/<int:user_id>/',mute_or_unmute_user, name='mute_or_unmute_user'),
]