from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views

from .views import CreateUserViewSet, UserViewSet, ValidationUserViewSet

router_v1 = SimpleRouter()

router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitlesViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewsViewSet, basename='reviews')
router_v1.register('auth/signup', CreateUserViewSet, basename='signup')
router_v1.register('auth/token', ValidationUserViewSet, basename='activate')
router_v1.register('users', UsersViewSet, basename='users')
#router_v1.register(
    #r'users/(?P<username>\d+)',
    #CommentViewSet,
    #basename='users'


urlpatterns = [
    path(
        'token/',
        jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path('v1/', include(router_v1.urls)),


