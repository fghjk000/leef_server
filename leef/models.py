from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, name, password=None):
        if not name:
            raise ValueError('Users must have a name')

        user = self.model(name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password):
        user = self.create_user(name=name, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=10)
    password = models.CharField(max_length=128, null=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'name'

    class Meta:
        app_label = "leef"


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.key
