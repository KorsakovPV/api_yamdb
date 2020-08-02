from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api import views
from users.views import APIUser, UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/users/me/', APIUser.as_view()),
    path('v1/auth/email/', views.send_confirmation_code,
         name='send_confirmation_code'),
    path('v1/auth/token/', views.get_jwt_token, name='get_jwt_token'),
    path('v1/', include(router_v1.urls)),
]
