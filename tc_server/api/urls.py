from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, TaskViewSet, TaskDetailView, CreateUserView, AssistantView

# router = routers.DefaultRouter()
# router.register(r'user/me', UserViewSet)
# router.register(r'tasks', TaskViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('user/me', UserViewSet.as_view(), name='api-user'),
    path('tasks/', TaskViewSet.as_view(), name='api-task'),
    path('tasks/<int:pk>', TaskDetailView.as_view(), name='api-task-id'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/signup/', CreateUserView.as_view(), name='api-signup'),
    path('assistant/', AssistantView.as_view(), name='assistant'),
]
