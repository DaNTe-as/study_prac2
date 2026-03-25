from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.utils.html import strip_tags
from django.core.validators import RegexValidator

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=255, widget=forms.EmailInput(attrs={'id': 'email','name': 'email', 'placeholder': 'example@mail.ru'}))
    first_name = forms.CharField(required=True, max_length=255, widget=forms.TextInput(attrs={'id': 'name','name': 'name', 'placeholder': 'Иванов Иван'}))
    password1 = forms.CharField(required=True, max_length=50,widget=forms.PasswordInput(attrs={'id': 'password','name': 'password', 'placeholder': 'Придумате пароль'}))
    password2 = forms.CharField(required=True, max_length=50,widget=forms.PasswordInput(attrs={'id': 'confirm_password','name': 'confirm_password', 'placeholder': 'Придумате пароль'}))

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('На эту почту уже зарегестрирован аккаунт')
        return email
    
    def save(self, commit = True):
        user = super().save(commit=False)
        user.username = None
        if commit:
            user.save()
        return user
    
class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email',widget=forms.TextInput(attrs={'placeholder': 'example@mail.ru'}))
    password = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))
    
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Данные введены не верно!')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('Пользователь был заблокирован')
        return self.cleaned_data

from .models import UserButtonChoice


class UserButtonChoiceForm(forms.ModelForm):
    class Meta:
        model = UserButtonChoice
        fields = ['button_value']