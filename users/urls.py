from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from users import views

# urlpatterns = [
#     path('email/', ),
#     path('token/', , name=''),
#     path('token/refresh/', , name='')
#
# ]
# TODO red В итоге в этом файле ничего не происходит - может, его совсем убрать?
