from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class Myaccountmanager(BaseUserManager):
    def create_user (self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must have email adress")
        
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, verbose_name=_('First name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last name'))
    username = models.CharField(max_length=50, unique=True, verbose_name=_('Username'))
    email = models.EmailField(max_length=100, unique=True, verbose_name=_('Email'))
    phone_number = models.CharField(max_length=50, verbose_name=_('Phone number'))
    
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('Date joined'))
    last_login = models.DateTimeField(auto_now_add=True, verbose_name=_('Last login'))
    is_admin = models.BooleanField(default=False, verbose_name=_('Is admin'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Is staff'))
    is_active = models.BooleanField(default=False, verbose_name=_('Is active'))
    is_superadmin = models.BooleanField(default=False, verbose_name=_('Is superadmin'))
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = Myaccountmanager()
    
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return self.is_admin
    
    def fullname(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, verbose_name=_('User'))
    address_line_1 = models.CharField(blank=True, max_length=100, verbose_name=_('Address line 1'))
    address_line_2 = models.CharField(blank=True, max_length=100, verbose_name=_('Address line 2'))
    profile_picture = models.ImageField(blank=True, upload_to='userprofile', verbose_name=_('Profile picture'))
    city = models.CharField(blank=True, max_length=50, verbose_name=_('City'))
    state = models.CharField(blank=True, max_length=50, verbose_name=_('State'))
    country = models.CharField(blank=True, max_length=50, verbose_name=_('Country'))
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
    
    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
    