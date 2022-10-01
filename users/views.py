from django.shortcuts import render, redirect
from users.forms import RegiserForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
# Create your views here.
def register_view(request):
    if request.method == 'GET':
        return render(request, 'users/register.html', context={'form': RegiserForm})

    if request.method =='POST':
        form = RegiserForm(request.POST)

    if form.is_valid():
        User.objects.create_user(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password'),
            email=form.cleaned_data.get('email'),
            is_active=True
        )
        return redirect('/users/login/')
    else:
        return render(request, 'users/register.html', context={'form':form})


def login_view(request):
    if request.method == 'GET':
        return render(request, 'users/logiin.html', context={'form': LoginForm})

    if request.method == 'POST':
        form = LoginForm(request.POST)

    if form.is_valid():
        user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )
        if user:
            login(request, user)
            return redirect('/')

        else:
            return render(request, 'users/logiin.html', context={'form': form})



def logout_view(request):
    if request.method == 'GET':
        logout((request))
        return redirect('/')
