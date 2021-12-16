from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import User


# class UserSerializer(serializers.ModelSerializer):
#     # user = SlugRelatedField(slug_field='username', read_only=True)

#     class Meta:
#         fields = ('username', 'email')
#         model = User

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()


class ConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    # class Meta:
    #     model = User
