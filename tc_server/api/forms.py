from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Task
from django import forms


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email", "name", "telegram_id")


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('description', 'user', 'updateDate', 'expirationDate', 'priority', 'status')
