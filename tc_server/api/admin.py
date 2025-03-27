from django.contrib import admin
from .models import User, Task
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("email", "name", "telegram_id")
    list_filter = ("email", "name", "telegram_id")
    fieldsets = (
        (None, {"fields": (("email", "name", "telegram_id"), "password", "key")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "name", "telegram_id", "password1", "password2", "is_staff", "is_active"
            )}
        ),
    )
    search_fields = ("telegram_id", "email")
    ordering = ("telegram_id", "email")


admin.site.register(User, CustomUserAdmin)


@admin.register(Task)
class UserAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'creationDate', 'updateDate', 'expirationDate', 'priority', 'status']
