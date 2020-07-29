from django.urls import include, path

from rest_framework.routers import DefaultRouter

from users import views

router_v1 = DefaultRouter()
router_v1.register('users', views.UserViewSet)
# router_v1.register('', views. , basename='')

urlpatterns = [
    path('v1/users/me/', views.APIUser.as_view()),
    # path('v1/auth/', include('users.urls')),
    path('v1/', include(router_v1.urls)),
]
