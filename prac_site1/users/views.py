from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .forms import CustomUserCreationForm, CustomUserLoginForm, UserButtonChoice
from .models import CustomUser 
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
    
    
def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('users:profile')
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'users/dashboard.html', {'user': request.user})

@login_required
def save_user_request(request):
    """Сохранение выбранной кнопки в БД"""
    if request.method == 'POST':
        button_value = request.POST.get('button_value')
        
        if button_value and button_value in ['1', '2', '3', '4']:
            UserButtonChoice.objects.create(
                user=request.user,
                button_value=int(button_value)
            )
            messages.success(request, f'Кнопка {button_value} успешно сохранена!')
        else:
            messages.error(request, 'Пожалуйста, выберите кнопку')
        
        return redirect('users:profile')
    
    return redirect('users:profile')