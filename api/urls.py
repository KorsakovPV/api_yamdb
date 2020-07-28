from django.urls import path, include
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
# router_v1.register('', views. , basename='')

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/', include(router_v1.urls))
    ]



