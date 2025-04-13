from rest_framework.permissions import BasePermission
from .models import Contributor, Issue


class IsAuthor(BasePermission):
    message = "Vous devez être l’auteur pour effectuer cette action."
    def has_object_permission(self, request, view, object):
        return object.author == request.user
