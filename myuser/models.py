from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **fields):
        if not username:
            raise ValueError('Username is required.')

        user = self.model(
            username=username,
            **fields

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **fields):
        fields.setdefault('is_staff', True)
        fields.setdefault('is_superuser', True)

        return self.create_user(username=username, password=password, **fields)


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
        null=True
    )

    is_active = models.BooleanField(
        'Active',
        default=True
    )

    is_staff = models.BooleanField(
        'Is staff',
        default=False
    )

    def get_full_name(self):
        return self.username

    # @property
    # def is_staff(self):
    #     return self.is_admin

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def delete_avatar(self):
        from django.core.files import File
        import os

        if os.path.basename(self.avatar.name) != 'avatar.png':
            self.avatar.delete()
            new_image = File(open('media/avatars/avatar.png', 'rb'))
            os.remove('media/avatars/avatar.png')
            self.avatar.save(name='avatar.png', content=new_image)

    def change_avatar(self):
        from PIL import Image
        from django.core.files import File

        if self.avatar.name != 'avatars/avatar.png':
            user_avatar = Image.open(self.avatar.path)
            user_avatar = user_avatar.rotate(90)
            user_avatar.save(self.avatar.path)
        else:
            changed_avatar = File(open('media/avatars/avatar.png', 'rb'))
            self.avatar.save(name='copy_of_default_avatar.png', content=changed_avatar)
            self.change_avatar()

    def suicide(self):
        self.delete_avatar()
        self.delete()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone', 'firstname', 'lastname', 'date_of_birth']
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'myuser'
