from rest_framework import permissions

method2permit = {
    'POST': 'add'
}

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # if request.method == 'DELETE':
        #     return request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class IsModeratorOrSuperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return request.user.groups.filter(name='recipe_moderators').exists()
        return False
