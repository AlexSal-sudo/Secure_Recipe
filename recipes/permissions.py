from rest_framework import permissions

method2permit = {
    'POST': 'add',
    'PUT': 'change',
    'PATCH': 'change',
    'GET': 'view',
    'HEAD': 'view',
    'OPTION': 'view'
}


class IsDeleter(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.groups.filter(name='recipe_moderators').exists() or request.user.is_superuser
        return request.method in method2permit
