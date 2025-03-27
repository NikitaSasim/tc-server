from rest_framework import viewsets, permissions, filters, generics
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer, CreateUserSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model


class UserViewSet(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)



class TaskViewSet(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateUserSerializer

    






