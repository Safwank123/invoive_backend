from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    message = 'You must be an admin to access this endpoint.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == request.user.Role.ADMIN)


class IsApprovedUser(BasePermission):
    message = 'Your account is not approved by an administrator yet.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_approved)
