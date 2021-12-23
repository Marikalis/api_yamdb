from django.db.models import Avg
from rest_framework import filters, mixins, permissions, viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.settings import api_settings

from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrModerOrReadOnly
from reviews.models import User, Category, Genre, Title
from .serializers import (
    SignupSerializer,
    ConfirmationSerializer,
    UserSerializer)
from .tokens import account_activation_token
from .filters import TitlesFilter


CORRECT_CODE = 'Код регистрации аккаунта'
WRONG_CODE = 'Неверный код активации'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def users_profile(self, request):
        user = get_object_or_404(
            User,
            username=request.user.username)

        if request.method == 'PATCH':
            serializer = UserSerializer(
                user,
                context={'request': request},
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(user)

        return Response(serializer.data)


class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user, created = User.objects.get_or_create(
                username=serializer.data.get('username'),
                email=serializer.data.get('email')
            )
            user.is_active = False
            user.save()
            msg = account_activation_token.make_token(user)
            email = EmailMessage(
                CORRECT_CODE,
                msg,
                to=[serializer.data.get('email')]
            )
            email.send()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class ValidationUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=serializer.data.get('username'))
            confirmation_code = serializer.data.get('confirmation_code')
            if (user is not None
                    and user.is_active is not True
                    and account_activation_token.check_token(
                        user,
                        confirmation_code
                    )):
                user.is_active = True
                user.save()
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                payload = jwt_payload_handler(request.user)
                token = jwt_encode_handler(payload)
                return Response(
                    {
                        'token': token
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    WRONG_CODE,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class CreateListDeleteViewSet(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    http_method_names = ['get', 'post', 'head', 'delete']

    def retrieve(self, request, slug):
        raise MethodNotAllowed('Не разрешенный метод')


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    pagination_class = PageNumberPagination

    permission_classes = (
        IsAdminOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitlePostSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthorOrModerOrReadOnly,
        IsAuthenticatedOrReadOnly
    )

    def _get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        title = self._get_title()
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = self._get_title()
        return title.reviews.all()
