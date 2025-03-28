from rest_framework import serializers
from .models import User, Task
from django.contrib.auth import get_user_model


class NullableDateTimeField(serializers.DateTimeField):
    def to_internal_value(self, value):
        if value in ("", None):
            return None
        return super().to_internal_value(value)


class TaskSerializer(serializers.ModelSerializer):
    expirationDate = NullableDateTimeField(required=False, allow_null=True)
    due_date = NullableDateTimeField(required=False, allow_null=True)

    class Meta:
        model = Task
        fields = (
            'taskId', 'creationDate', 'status', 'updateDate', 'description',
            'priority', 'expirationDate', 'due_date'
        )


class UserSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'tasks')


UserModel = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
        )

        return user

    class Meta:
        model = UserModel
        fields = ('email', 'password', 'name')
