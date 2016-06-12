from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password=None,  **fields):

        if not username:
            raise ValueError('Username is required.')

        user = self.model(
            username = username,
            **fields

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **fields):

        fields.setdefault('is_staff',True)
        fields.setdefault('is_superuser',True)
        fields.setdefault('is_admin',True)

        return self.create_user(username=username, password=password,  **fields )


class ExtUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Username',
        max_length=15,
        unique=True,
        db_index=True
    )
    email = models.EmailField(
        'Email',
        max_length=255,
        unique=False,
        null=False,
        blank=False

    )
    phone = models.CharField(
        'Phone',
        max_length=10,
        null=False,
        blank=False

    )
    firstname = models.CharField(
        'First name',
        max_length=40,
        null=False,
        blank=False
    )
    lastname = models.CharField(
        'Last name',
        max_length=40,
        null=False,
        blank=False
    )

    date_of_birth = models.DateField(
        'Date of birth',
        null=False,
        blank=False
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        default="avatars/avatar.png",
        blank=True,
        null=True)
    is_active = models.BooleanField(
        'Active',  
        default=True
    )
    is_admin = models.BooleanField(
        'Is admin',
        default=False
    )


    def get_full_name(self):
        return self.username

    @property
    def is_staff(self):

        return self.is_admin

    def get_short_name(self):

        return self.username

    def __str__(self):

        return self.username

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone', 'firstname', 'lastname', 'date_of_birth']
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'myuser'