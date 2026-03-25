from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'users'
 
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register, name='register'),
    path('save/', views.save_user_request, name='save_user_request'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)