from rest_framework import serializers
from .models import User, Project, Contributor,Issue

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, validators=[])

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'age', 'can_be_contacted', 'can_data_be_shared')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Cet utilisateur existe déjà.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type']

    def create(self, validated_data):
        user = self.context['request'].user
        project = Project.objects.create(author=user, **validated_data)
        Contributor.objects.create(
            user=user,
            project=project,
        )
        return project

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user']