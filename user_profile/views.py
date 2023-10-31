from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import *
from .forms import *
from .decorators import *
from notifications.models import Notification

# Create your views here.
@never_cache
@not_login_required
def login_user(request):
    form = LoginForm()
    context = {
        "form": form
    }
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data.get('username'),
                password = form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, 'Wrong credentials')
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')

@never_cache
@not_login_required
def register_user(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)         # initially form is not saved as pw needs to be hashed
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, "Registration successful")
            return redirect('login')
    context= {
        "form": form
    }
    return render(request, 'registration.html', context)

@login_required(login_url='login')
def profile(request):
    account = get_object_or_404(User, pk=request.user.pk)
    form = ProfileUpdateForm(instance = account)
    if request.method == "POST":
        if request.user.pk != account.pk:
            return redirect('home')
        form = ProfileUpdateForm(request.POST, instance = account)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated successfully.")
            return redirect('profile')
    context = {
        "account": account,
        "form": form
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def change_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES['profile_picture']
            user = get_object_or_404(User, pk = request.user.pk)
            if request.user.pk != user.pk:
                return redirect('home')
            user.profile_image = img
            user.save()
            messages.success(request, "Profile picture has been updated successfully.")
    return redirect('profile')

def view_user_info(request, username):
    # Get the user account based on the provided username, or return a 404 error if not found
    account = get_object_or_404(User, username = username)

    # Initialize variables for following and muted
    following = False
    muted = None
    
    # Check if the request is coming from an authenticated user
    if request.user.is_authenticated:
        # Check if the requested user is the same as the logged-in user
        if request.user.id == account.id:   
            # Redirect to the user's own profile      
            return redirect('profile')   

        # Fetch the "followers for the 'account' user" that are "followed by the current logged-in user (request)"    
        # user 'account' ke current logged-in user follow korse se onusare followers(current user) list filter 
        followers = account.followers.filter(
            followed_by__id = request.user.id     
            )
        # Check if any followers exist for this relationship
        if followers.exists(): 
             # Set 'following' to True if the current user follows the 'account' user       
            following = True                     
    
    # If the current user is following the 'account' user, further actions are taken
    if following:              
        # Retrieve the first follower in the queryset                   
        queryset = followers.first()    
        # Check if the follower is muted the account he's following, then he will not get any notification        
        if queryset.muted:
            muted = True
        else:
            muted = False

    context = {
        "account": account,
        "following": following,
        "muted": muted
    }
    return render(request, 'user_info.html', context)

@login_required(login_url='login')
def follow_or_unfollow_user(request, user_id):
    followed = get_object_or_404(User, id = user_id)
    followed_by = get_object_or_404(User, id = request.user.id)

    # if there is a instance in Follow class of these id(s) then already following, otherwise not
    follow, created = Follow.objects.get_or_create(followed=followed, followed_by=followed_by)
    if created:   # relation built i.e follow instance
        followed.followers.add(follow)
    else:
        followed.followers.remove(follow)
        follow.delete()
    return redirect('view_user_info', username = followed.username)

@login_required(login_url='login')
def user_notifications(request):
    notifications = Notification.objects.filter(
        user = request.user,
        is_seen = False
    )
    for nf in notifications:
        nf.is_seen = True
        nf.save()
    return render(request, 'notifications.html')

@login_required(login_url='login')
def mute_or_unmute_user(request, user_id):      # kake ami mute korte chacci tar user_id
    user = get_object_or_404(User, pk = user_id)
    follower = get_object_or_404(User, pk = request.user.pk)

    instance = get_object_or_404(
        Follow,
        followed = user, 
        followed_by = follower
        )
    if instance.muted:   
        instance.muted = False
        instance.save()
    else:
        instance.muted = True
        instance.save()
    return redirect('view_user_info', username = user.username)