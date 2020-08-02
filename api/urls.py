from django.urls import include, path

from rest_framework.routers import DefaultRouter

from users import views
from content import views as content_views

router_v1 = DefaultRouter()
router_v1.register('users', views.UserViewSet)
router_v1.register('categories', content_views.CategoryViewSet)
router_v1.register('genres', content_views.GenreViewSet)
router_v1.register('titles', content_views.TitleViewSet)

# router_v1.register('', views. , basename='')

urlpatterns = [
    path('v1/users/me/', APIUser.as_view()),
    path('v1/auth/email/', views.send_confirmation_code,
         name='send_confirmation_code'),
    path('v1/auth/token/', views.get_jwt_token, name='get_jwt_token'),
    path('v1/', include(router_v1.urls)),
]
