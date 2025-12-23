from django.db import models
from .recruiter  import CustomUserManager
from datetime import datetime, timezone 
import uuid
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from common.models import BaseModel

class TokenTypes(models.TextChoices): # Enum for token types
    PASSWORD_RESET = 'password_reset', 'Password Reset'
    EMAIL_VERIFICATION = 'email_verification', 'Email Verification'

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
    
class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Unique identifier
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # Link to the user 
    token = models.CharField(max_length=64, unique=True) # Token string
    token_type = models.CharField(max_length=32,choices=TokenTypes.choices) # Type of token (e.g., 'password_reset')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.username} {self.token_type}"
    
    def is_valid(self) -> bool:
        lifespan_seconds = 30 * 60  # 30 minutes
        now  = datetime.now(timezone.utc)
        time_elapsed = (now  - self.created_at).total_seconds()
        if time_elapsed <= lifespan_seconds:
            return True
        return False
    
    def reset_user_password(self, new_password: str):
        user = self.user
        user.set_password(new_password)
        user.save()
        