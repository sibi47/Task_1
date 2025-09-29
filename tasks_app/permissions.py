from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'SUPERADMIN')


class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ('ADMIN','SUPERADMIN'))


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to_id == request.user.id