from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin'


# class ReadOnly(permissions.BasePermission):

#     def has_view_permission(self, request, view, obj):
#         return request.user.is_authenticated()

#     def has_object_permission(self, request, view, obj):
#         return (request.method in permissions.SAFE_METHODS
#                 or obj.author == request.user)
