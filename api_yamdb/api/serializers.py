from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Comment, User, Review


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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)
    class Meta:
        model = Comment
        exclude = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Review
        exclude = ['title']
    
    def validate (self, data):
        request = self.context.get('request')
        if request.method != ' POST':
            return data
        user = request. user
        title = get_object_or_404(
            Title,
            pk=request.parser_context.get('kwargs').get('title_id'))
        if Review.objects.filter(author=user, title=title).exists():
            raise serializers. ValidationError('Вы уже оставили отзыв на это произведение!')
        return data
