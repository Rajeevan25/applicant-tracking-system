from django.db import models
from .recruiter  import CustomUserManager
from datetime import datetime, timezone 
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from common.models import BaseModel

class CustomUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username

class PendingUser(BaseModel):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    verification_code = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_valid(self) -> bool:
        lifespan_seconds = 15 * 60  # 15 minutes
        now  = datetime.now(timezone.utc)
        time_elapsed = (now  - self.created_at).total_seconds()
        if time_elapsed <= lifespan_seconds:
            return True
        return False
    def __str__(self):
        return self.email