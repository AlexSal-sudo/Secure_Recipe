from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

method2permit = {
    'POST': 'add',
    'PUT': 'change',
    'PATCH': 'change',
    'GET': 'view',
    'HEAD': 'view',
    'OPTION': 'view'
}
methodForbiddenModerator = ['POST', 'PUT', 'PATCH']


class IsModeratorOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in methodForbiddenModerator and request.user.groups.filter(name='recipe_moderators').exists()\
                and not request.user.is_superuser:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            if request.user.is_superuser:
                return True
            elif request.user.groups.filter(name='recipe_moderators').exists():
                return not obj.author.is_superuser
        return request.method in method2permit
