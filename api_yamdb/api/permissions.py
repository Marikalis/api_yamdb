from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return request.user.is_admin
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsAuthorOrModerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_anonymous:
            return False
        else:
            return (request.user.is_admin
                    or request.user.is_moderator
                    or obj.author == request.user)

class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin'


# class ReadOnly(permissions.BasePermission):

#     def has_view_permission(self, request, view, obj):
#         return request.user.is_authenticated()

#     def has_object_permission(self, request, view, obj):
#         return (request.method in permissions.SAFE_METHODS
#                 or obj.author == request.user)
