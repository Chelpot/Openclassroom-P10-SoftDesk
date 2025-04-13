from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import User, Project, Issue, Contributor, Comment
from .permissions import IsAuthor, IsProjectContributor, IsAuthorOrCanUpdateStatus
from .serializers import UserSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    #Called before any action in ViewSet to know permissions (Update/Destroy/Get/Mine/AddContributor/...)
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'contributors', 'add_contributor', 'remove_contributor']:
            return [permissions.IsAuthenticated(), IsAuthor()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Project.objects.all()

    # get list of projects in with I am a contributor
    @action(detail=False, methods=['get'], url_path='mine')
    def my_projects(self, request):
        user = request.user
        projects = Project.objects.filter(contributors=user)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    # get list of contributors for a given project id
    @action(detail=True, methods=['get'], url_path='contributors')
    def list_contributors(self, request, pk=None):
        project = self.get_object()
        contributors = project.contributors.all()
        data = [{'id': user.id, 'username': user.username} for user in contributors]
        return Response(data)

    # add a User as a Contributor for a given project
    @action(detail=True, methods=['post'], url_path='add_contributor')
    def add_contributor(self, request, pk=None):
        project = self.get_object()
        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if Contributor.objects.filter(user=user, project=project).exists():
                return Response(
                    {"detail": "Ce contributeur existe déja"}, status=status.HTTP_400_BAD_REQUEST
                )
            Contributor.objects.create(
                user=user,
                project=project
            )
            return Response({"detail": "Contributeur ajouté"}, status=201)
        else:
            return Response(serializer.errors, status=400)

    # Remove a Contributor from the project. Use Regex to get user_id argument cause of DRF way to work
    @action(detail=True, methods=['delete'], url_path='remove_contributor/(?P<user_id>[^/.]+)')
    def remove_contributor(self, request, pk=None, user_id=None):
        project = self.get_object()
        contributor = Contributor.objects.get(project=project, user__id=user_id)
        if contributor.user == project.author:
            return Response({"detail": "Vous ne pouvez pas retirer l’auteur des contributeurs."},
                            status=status.HTTP_400_BAD_REQUEST)
        contributor.delete()
        return Response({f"detail": f"Contributeur {user_id} retiré."}, status=status.HTTP_204_NO_CONTENT)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAuthor()]
        if self.action in ['partial_update']:
            return [permissions.IsAuthenticated(), IsAuthorOrCanUpdateStatus()]
        return [permissions.IsAuthenticated(), IsProjectContributor()]

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        return Issue.objects.filter(project__id=project_id, project__contributors=self.request.user)


    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        project = get_object_or_404(self.request.user.projects, id=project_id)
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        issue_id = self.kwargs.get('issue_pk')
        issue = get_object_or_404(Issue, pk=issue_id)

        if not issue.project.contributors.filter(id=self.request.user.id).exists():
            raise PermissionDenied("Vous n’êtes pas contributeur de ce projet.")

        return Comment.objects.filter(issue=issue)

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('issue_pk')
        issue = get_object_or_404(Issue, pk=issue_id)

        if not issue.project.contributors.filter(id=self.request.user.id).exists():
            raise PermissionDenied("Vous n’êtes pas contributeur de ce projet.")

        serializer.save(author=self.request.user, issue=issue)


    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("Vous ne pouvez modifier que vos propres commentaires.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Vous ne pouvez supprimer que vos propres commentaires.")
        instance.delete()