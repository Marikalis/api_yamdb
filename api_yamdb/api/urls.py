from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views

from .views import CreateUserViewSet, UsersViewSet, ValidationUserViewSet

router_1 = SimpleRouter()

router_1.register('auth/signup', CreateUserViewSet, basename='signup')
router_1.register('auth/token', ValidationUserViewSet, basename='activate')
router_1.register('users', UsersViewSet, basename='users')
#router_1.register(
    #r'users/(?P<username>\d+)',
    #CommentViewSet,
    #basename='users'


urlpatterns = [
    path(
        'token/',
        jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path('v1/', include(router_1.urls)),
]
