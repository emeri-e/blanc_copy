from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
            # admin users only can see list view
        if request.user.is_staff:
            return True
        return False
    def has_object_permission(self, request, view, obj):

        if request.method == 'DELETE' and not request.user.is_staff:
            return False
        
        return obj.user == request.user or request.user.is_staff

class IsOwnerOrAdminCanDelete(permissions.BasePermission):
    def has_permission(self, request, view):
            # admin users only can see list view
        if request.user.is_staff:
            return True
        return False
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
