# urls.py
from django.urls import path
from accounts.views import register_user,login_user,logout_user

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='loginn'),
    path('logout/', logout_user, name='logout'),
]
