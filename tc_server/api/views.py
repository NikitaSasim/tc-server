from rest_framework import viewsets, permissions, filters, generics
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError

from .models import User, Task
from .serializers import UserSerializer, TaskSerializer, CreateUserSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from openai import OpenAI
import os


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ValidateTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        access_token_str = request.data.get("access")
        refresh_token_str = request.data.get("refresh")

        if not access_token_str or not refresh_token_str:
            return Response({"detail": "Access and refresh tokens required."}, status=400)

        try:
            AccessToken(access_token_str)
            return Response({"detail": "Access token is valid."}, status=200)

        except TokenError:
            try:
                refresh = RefreshToken(refresh_token_str)
                new_access = str(refresh.access_token)
                return Response({
                    "detail": "Access token refreshed.",
                    "access": new_access
                }, status=200)

            except TokenError:
                return Response({"detail": "Both tokens are invalid or expired."}, status=401)


class AssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user_input = request.data.get("text", "")

        tasks = Task.objects.filter(user=user)
        serialized_tasks = TaskSerializer(tasks, many=True).data

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
        user = self.request.user
        data = self.request.data
        original_description = data.get("description", "")

        # Формируем промпт на английском
        prompt = f"""
You are an assistant helping to analyze a task. The user wrote the following task description:

"{original_description}"

Please:
- Extract the key actionable steps needed to complete this task.
- If possible, provide up to 5 useful links (e.g., tutorials, docs, tools) that can help the user accomplish it.

Respond in English in the following format:

Key Points:
- point 1
- point 2
...

Resources:
1. [title](url)
2. ...
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful task assistant."},
                    {"role": "user", "content": prompt.strip()}
                ],
                temperature=0.7,
                max_tokens=700
            )

            gpt_response = response.choices[0].message.content.strip()

            # Объединяем оригинальное описание + ответ
            combined_description = f"{original_description}\n\n---\n\n{gpt_response}"

            serializer.save(user=user, description=combined_description)

        except Exception as e:
            raise Exception(f"OpenAI request failed: {e}")


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

    






