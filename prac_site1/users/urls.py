from django.urls import path
from .  import views

app_name = 'users'
 
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register, name='register'),
    path('save/', views.save_button_choice, name='save_button_choice'),
]