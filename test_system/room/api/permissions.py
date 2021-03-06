from rest_framework import permissions


class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Teacher's and Admin's actions permission towards Room object
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return True
        return False


class IsStudent(permissions.BasePermission):
    """
    Student's actions permission towards Room object
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
        return False


class EmptyPermission(permissions.BasePermission):
    """
    Anonymous user actions permission towards Room object
    """

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False
