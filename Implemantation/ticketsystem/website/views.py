from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import UserReg
from .models import User


def home(request):
    return render(request, 'home.html')


def signup(request):
    form = UserReg(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/home.html')
    return render(request, 'registration/signup.html',
                  {'form': UserReg})
