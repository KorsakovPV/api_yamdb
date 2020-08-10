from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users import views as users_views

from .views import *

router_v1 = DefaultRouter()
router_v1.register('users', users_views.UserViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

auth_patterns = [
    path('email/', send_confirmation_code, name='send_confirmation_code'),
    path('token/', get_jwt_token, name='get_jwt_token')
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
