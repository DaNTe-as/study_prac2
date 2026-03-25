from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .forms import CustomUserCreationForm, CustomUserLoginForm, UserButtonChoice, UserButtonChoiceForm
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
    form = UserButtonChoiceForm()
    return render(request, 'users/dashboard.html', {'user': request.user, 'form': form})

@login_required
def save_user_request(request):
    """Сохранение выбранной кнопки в БД"""
    if request.method == 'POST':
        form = UserButtonChoiceForm(request.POST, request.FILES)
        
        if form.is_valid():
            button_value = form.cleaned_data.get('button_value')
            file = form.cleaned_data.get('file')
            
            # Сохраняем в базу данных
            choice = UserButtonChoice(
                user=request.user,
                button_value=button_value,
                file=file
            )
            choice.save()
            
            if file:
                messages.success(request, f'Кнопка {button_value} и файл "{file.name}" успешно сохранены!')
            else:
                messages.success(request, f'Кнопка {button_value} успешно сохранена!')
        else:
            for error in form.errors.values():
                messages.error(request, error)
        
        return redirect('users:profile')
    
    return redirect('users:profile')