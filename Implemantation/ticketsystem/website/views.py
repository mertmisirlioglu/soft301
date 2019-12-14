from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import UserReg 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')


def signup(request):
    form = UserReg(request.POST or None)
    print(form.errors)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/home.html')
    return render(request, 'registration/signup.html',
                  {'form': UserReg})


