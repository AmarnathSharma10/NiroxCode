from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from accounts.models import Profile

# Create your views here.

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        age = request.POST.get('age')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, 'User with this username already exists')
            return redirect("/accounts/register/")

        user = User.objects.create_user(username=username)

        user.set_password(password)
        user.save()
        profile=Profile(user=user,age=age)
        profile.save()

        messages.info(request, 'User created successfully')
        return redirect('/accounts/register/')

    template = loader.get_template('register.html')
    context = {}
    return HttpResponse(template.render(context, request))


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, 'User with this username does not exist')
            return redirect('/accounts/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, 'invalid password')
            return redirect('/accounts/login')

        login(request, user)
        messages.info(request, 'login successful')

        return redirect('/home/all_problems/')

    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))


def logout_user(request):
    logout(request)
    messages.info(request, 'logout successful')
    return redirect('/accounts/login/')
