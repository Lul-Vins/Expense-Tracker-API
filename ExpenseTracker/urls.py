
from django.contrib import admin
from django.urls import path
from users.views import RegisterUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',RegisterUserView.as_view(),name = 'Registro'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
