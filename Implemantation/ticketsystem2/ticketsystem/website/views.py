from django.contrib import messages
# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import UserReg, ExtendedUserCreationForm


def home(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'not logged in'
    context = {'username': username}
    return render(request, 'home.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password not correct')
            return redirect('login')
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html',
                      {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def signup(request):
    form = ExtendedUserCreationForm(request.POST or None)
    profile_form = UserReg(request.POST or None)
    print(form.errors)
    if form.is_valid() and profile_form.is_valid():
        user = form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'registration/signup.html',
                  {'form': ExtendedUserCreationForm, 'profile_form': UserReg})
