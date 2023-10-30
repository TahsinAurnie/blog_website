from django.urls import path

from .views import *
urlpatterns =[
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register_user/', register_user, name='register_user'),
    path('profile/', profile, name='profile'),
    path('profile_picture/', change_profile_picture, name='profile_picture'),
    path('view_user_info/<str:username>/', view_user_info, name='view_user_info'),
    path('follow_or_unfollow/<int:user_id>/', follow_or_unfollow_user, name='follow_or_unfollow_user'),
]