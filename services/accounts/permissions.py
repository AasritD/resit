from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Allows access to users with role 'admin' or 'super'.
    """
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role in ['admin', 'super']
        )

class IsSuperAdmin(permissions.BasePermission):
    """
    Allows access only to users with role 'super'.
    """
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'super'
        )

class IsCustomerOrReadOnly(permissions.BasePermission):
    """
    Customers may only read; admin/super may read & write.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role in ['admin', 'super']
        )
