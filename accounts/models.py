from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from typing import Any
import uuid
        
class CustomUserManager(UserManager):

    def create_user(self, email: str, password: str, **extra_fields: Any):
        
        user = self.model(email=email, is_superuser=False, is_staff=False, is_active=True, 
                          **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, password=password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.name = user.email
        user.save(using=self._db)
        return user

class UserWallet(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField('email address', unique=True, max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()
    created = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField('staff status', default=False)
    owned_by = models.UUIDField(default=uuid.uuid4, editable=False)
    
    def __str__(self) -> str:
        return self.name