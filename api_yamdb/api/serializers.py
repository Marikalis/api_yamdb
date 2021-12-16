from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User


# class UserSerializer(serializers.ModelSerializer):
#     # user = SlugRelatedField(slug_field='username', read_only=True)

#     class Meta:
#         fields = ('username', 'email')
#         model = User

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])


class ConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
