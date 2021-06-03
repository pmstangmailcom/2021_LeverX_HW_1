from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    """Allows access only to a teacher."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.level == 'teacher')


class IsStudent(BasePermission):
    """Allows access only to a student."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.level == 'student')


class IsOwner(BasePermission):
    """Allows access only to object owner ."""

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user)
        # return bool(request.user == obj.user or request.user.is_admin)



