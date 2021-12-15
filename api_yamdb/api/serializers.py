from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = User
