from rest_framework.permissions import BasePermission
from .models import Contributor, Issue
from django.shortcuts import get_object_or_404



class IsAuthor(BasePermission):
    message = "Vous devez être l’auteur pour effectuer cette action."
    def has_object_permission(self, request, view, object):
        return object.author == request.user


class IsProjectContributor(BasePermission):
    message = "Vous n’êtes pas contributeur de ce projet."
    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_pk") or request.data.get("project")
        if not project_id:
            return False
        return Contributor.objects.filter(project_id=project_id, user=request.user).exists()

    def has_object_permission(self, request, view, object):
        return Contributor.objects.filter(project=object.project, user=request.user).exists()


class IsAuthorOrCanUpdateStatus(BasePermission):
    def has_object_permission(self, request, view, object):
        if object.author == request.user:
            return True

        is_contrib = Contributor.objects.filter(project=object.project, user=request.user).exists()
        if is_contrib and request.method in ["PUT", "PATCH"]:
            #Check if body only contain status field
            if set(request.data.keys()) == {"status"}:
                return True
            self.message = "En tant que contributeur  vous ne pouvez modifier que le statut."
            return False

        self.message = "Vous devez être  contributeur de ce projet."
        return False


class IsProjectContributorForComment(BasePermission):
    message = "Vous devez être contributeur du projet pour accéder aux commentaires."

    def has_permission(self, request, view):
        issue_id = view.kwargs.get("issue_pk")
        if not issue_id:
            return False

        issue = get_object_or_404(Issue, id=issue_id)
        return Contributor.objects.filter(user=request.user, project=issue.project).exists()