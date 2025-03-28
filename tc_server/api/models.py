from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.TextField(max_length=50)
    telegram_id = models.BigIntegerField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class Task(models.Model):
    taskId = models.BigAutoField(primary_key=True)
    description = models.TextField(max_length=5000)
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name='tasks')

    creationDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    expirationDate = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)

    priority = models.CharField(
        max_length=50,
        blank=True,
        default="sooner"
    )

    status = models.CharField(
        max_length=50,
        blank=True,
        default="created"
    )

    def __str__(self):
        return f"{self.description[:30]}..."
