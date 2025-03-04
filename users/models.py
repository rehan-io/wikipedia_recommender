from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _



class User(AbstractUser):
    """Custom user model that extends Django's AbstractUser"""
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    
    # Add additional fields as needed
    
    def __str__(self):
        return self.username
