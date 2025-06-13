from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.urls import reverse

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    profile_picture = models.ImageField(default='default_picture.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['username', 'email']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
        ]
        verbose_name = 'user'
        verbose_name_plural = 'users'
