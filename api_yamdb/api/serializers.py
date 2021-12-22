from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=[UniqueValidator(
            queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all())]
    )

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('Cannot signup as me')
        return data


class ConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all())]
    )

    def validate_role(self, role):
        user = self.context['request'].user
        if user.role == 'admin' or user.is_superuser:
            return role
        return user.role

    class Meta:
        fields = 'username', 'email', 'role', 'first_name', 'last_name', 'bio'
        model = User
