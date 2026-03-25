from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.html import strip_tags

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None,**extra_fields):
        if not email:
            raise ValueError('Должен быть email')
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
    
    def create_superuser(self, email, first_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('должен быть работником')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('должен быть суперпользователем')
        
        return self.create_user(email, first_name, password, **extra_fields)
        
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=50)

    username = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name',]
    
    def __str__(self):
        return self.email


class UserButtonChoice(models.Model):
    """Модель для хранения выбора пользователя"""
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    
    button_value = models.PositiveSmallIntegerField(
        verbose_name="Выбранная кнопка"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания"
    )
    
    class Meta:
        verbose_name = "Выбор пользователя"
        verbose_name_plural = "Выборы пользователей"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} нажал кнопку {self.button_value}"