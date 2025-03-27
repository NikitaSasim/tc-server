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
    class TaskStatus(models.TextChoices):
        CREATED = 'CRE', _('created'),
        RESOLVED = 'RES', _('resolved'),
        REJECTED = 'REJ', _('rejected')

    class TaskPriority(models.TextChoices):
        SOONER = 'SO', _('sooner'),
        LATER = 'LA', _('later'),
        MAYBENEVER = 'MN', _('maybe never')

    taskId = models.BigAutoField(primary_key=True)
    description = models.TextField(max_length=400)
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name='tasks')
    creationDate = models.DateTimeField(auto_now_add=True, blank=True)
    updateDate = models.DateTimeField(blank=True)
    expirationDate = models.DateTimeField(blank=True)

    priority = models.CharField(
        max_length=2,
        choices=TaskPriority.choices,
        default=TaskPriority.LATER,
    )

    status = models.CharField(
        max_length=3,
        choices=TaskStatus.choices,
        default=TaskStatus.CREATED,
    )
