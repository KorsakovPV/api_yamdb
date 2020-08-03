from django.urls import include, path
from rest_framework.routers import DefaultRouter

from content import views as content_views
from users import views as users_views
from .views import send_confirmation_code, get_jwt_token

router_v1 = DefaultRouter()
router_v1.register('users', users_views.UserViewSet)
router_v1.register('categories', content_views.CategoryViewSet)
router_v1.register('genres', content_views.GenreViewSet)
router_v1.register('titles', content_views.TitleViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   content_views.ReviewViewSet,
                   basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    content_views.CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/users/me/', users_views.APIUser.as_view()),
    path('v1/auth/email/', send_confirmation_code,
         name='send_confirmation_code'),
    path('v1/auth/token/', get_jwt_token, name='get_jwt_token'),
    path('v1/', include(router_v1.urls)),
]
