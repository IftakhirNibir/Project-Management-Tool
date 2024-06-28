from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 

from .models import UserProfile

from django.urls import reverse

from TaskTracker.models import Task

# Create your views here.

def index(request):
    return render(request,'index.html')

def user_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        check_password = request.POST.get('check_password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, 'Username already taken. Please try another')
            return redirect('/signup/')

        if password != check_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup/')  

        try:
            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user.set_password(password) 
            user.save()
            return redirect('/login/')  
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect('/signup/')

    return render(request,'signup.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('projects:project_detail')
        else:
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Invalid Username')
            else:
                messages.error(request, 'Invalid Password')
            return redirect('/login/') 

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

def user_profile(request, id):
    user = get_object_or_404(User, id=id)
    task = Task.objects.filter(assigned_to=user)
    
    try:
        profile = UserProfile.objects.get(user=user)
        profile_photo_url = profile.profile_photo.url if profile.profile_photo else None
    except UserProfile.DoesNotExist:
        profile_photo_url = None
    
    context = {
        'profile_photo_url': profile_photo_url,
        'task':task
    }
    return render(request, 'profilepage.html', context)

def update_user_profile(request, id):
    user = get_object_or_404(User, id=id) 
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        image = request.FILES.get('profile_photo')

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        if image:
            profile.profile_photo = image
            profile.save()

        return redirect(reverse('user_accounts:user_profile', args=[user.id]))

    context = {'data': user}
    return render(request, 'editprofile.html', context)


