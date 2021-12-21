from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    # def has_permission(self, request, view):
    #     return request.method in permissions.SAFE_METHODS

    #def has_object_permission(self, request, view, obj):
        # if request.user.is_authenticated:
        #     print(f'request.user.role = {request.user.role}')
        #     return request.user.role == 'admin'
        #return True

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == 'admin' or request.user.is_superuser
        


#class IsSuperUser(permissions.BasePermission):

    #def has_permission(self, request, view):
        #return request.user and request.user.is_superuser


# class ReadOnly(permissions.BasePermission):

#     def has_view_permission(self, request, view, obj):
#         return request.user.is_authenticated()

#     def has_object_permission(self, request, view, obj):
#         return (request.method in permissions.SAFE_METHODS
#                 or obj.author == request.user)
