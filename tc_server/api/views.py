from rest_framework import viewsets, permissions, filters, generics
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer, CreateUserSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from openai import OpenAI
import os


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class AssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user_input = request.data.get("text", "")

        # Получаем и сериализуем задачи
        tasks = Task.objects.filter(user=user)
        serialized_tasks = TaskSerializer(tasks, many=True).data

        # Системный промпт
        system_prompt = """
You are an assistant for me and your job is to pick the most suitable tasks from my list according to my needs. 
Tasks will be provided in JSON format. Tasks have priorities, but don't pay too much attention to it. 
You have to reply with the message explaining your pick shortly, please don't repeat the request, don't use task numbers 
to describe the task, just reply as a human, in simple words, short one paragraph of text and also provide the picked tasks ids in the end. 
Provide answer only in the following JSON format, no quotes, just object, no text outside the object:
{
  answerText: TEXT OF YOUR RESPONSE, ONLY HERE,
  pickedTasksArray: [id1, id2]
}
"""

        user_prompt = f"Tasks:\n{serialized_tasks}\n\nUser input: {user_input}"

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt.strip()},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=700
            )

            reply = response.choices[0].message.content.strip()
            return Response({"response": reply})

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class UserViewSet(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)


class TaskViewSet(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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

    






