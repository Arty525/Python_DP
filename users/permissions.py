from rest_framework.permissions import BasePermission

def IsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return False


def IsCurrentUser(BasePermission):
    def has_object_permission(self, request, view, object):
        if request.user == object.user or request.user.is_superuser:
            return True
        return False