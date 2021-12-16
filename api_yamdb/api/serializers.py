from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("Cannot signup as me")
        return data



class ConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
