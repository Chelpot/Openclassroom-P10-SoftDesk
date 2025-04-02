from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, permissions, viewsets, status
from .models import User, Project, Issue, Contributor
from .serializers import UserSerializer, ProjectSerializer, ContributorSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.all()

    def perform_update(self, serializer):
        project = self.get_object()
        if project.author != self.request.user:
            raise PermissionDenied("Vous devez êtres l'auteur du projet pour le modifier.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Vous devez êtres l'auteur du projet pour le supprimer.")
        instance.delete()

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
        if project.author != request.user:
            raise PermissionDenied("Vous devez êtres l'auteur pour ajouter un contributeur à ce projet")

        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if Contributor.objects.filter(user=user, project=project).exists():
                return Response(
                    {"detail": "Ce contributeur existe déja"},
                    status=status.HTTP_400_BAD_REQUEST
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
        if project.author != request.user:
            raise PermissionDenied("Vous devez êtres l'auteur pour ajouter un contributeur à ce projet")
        try:
            contributor = Contributor.objects.get(project=project, user__id=user_id)
        except Contributor.DoesNotExist:
            raise NotFound("Contributeur introuvable.")
        if contributor.user == project.author:
            return Response({"detail": "Vous ne pouvez pas retirer l’auteur des contributeurs."},
                            status=status.HTTP_400_BAD_REQUEST)
        contributor.delete()
        return Response({f"detail": f"Contributeur {user_id} retiré."}, status=status.HTTP_204_NO_CONTENT)
