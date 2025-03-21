from rest_framework import serializers
from .models import User

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
