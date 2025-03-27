from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.user)
        print(request.user)
        return obj.user == request.user
