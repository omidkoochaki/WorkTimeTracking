from rest_framework.permissions import BasePermission

from time_tracker.models import Project


class IsProjectOwner(BasePermission):
    """
    allows just POs
    """
    def has_permission(self, request, view):
        print(request.data.get('project'))
        print(Project.objects.get(id=request.data.get('project')).owner)
        return bool(request.user == Project.objects.get(id=request.data.get('project')).owner)


class IsMemberInProject(BasePermission):
    """
    Allows just project members
    """

    def has_permission(self, request, view):
        print(request.data.get('project'))
        print(Project.objects.get(id=request.data.get('project')).members)
        return bool(request.user in Project.objects.get(id=request.data.get('project')).members)
