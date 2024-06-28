from django.urls import path 
from .views import *

app_name = 'user_accounts'

urlpatterns = [
    path('', index),
    path('signup/', user_signup, name="user_signup"),
    path('login/', user_login, name="user_login"),
    path('logout/', user_logout, name="user_logout"),
    path('profile/<id>', user_profile, name="user_profile"),
    path('edit_profile/<id>', update_user_profile, name="update_user_profile"),
]