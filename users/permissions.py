from rest_framework.permissions import BasePermission

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return False


class IsCurrentUser(BasePermission):
    def has_object_permission(self, request, view, object):
        if request.user == object or request.user.is_superuser:
            return True
        return False