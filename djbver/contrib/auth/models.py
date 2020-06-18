from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from djbver.db.models import GenericActiveModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('이메일이 필수입니다.')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(GenericActiveModel):
    email = models.EmailField('이메일', unique=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        abstract = True
        db_table = 'users'
        verbose_name = '유저'
        verbose_name_plural = '유저들'

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_active and self.is_superuser
