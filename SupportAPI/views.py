from django.shortcuts import render

from rest_framework import generics, permissions
from .models import User, Project, Issue, Contributor
from .serializers import UserSerializer, ProjectSerializer

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]