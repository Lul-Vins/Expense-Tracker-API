
from django.contrib import admin
from django.urls import path, include 
from users.views import RegisterUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import *
from gastos.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',RegisterUserView.as_view(),name = 'registro'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('crear_producto/', CreateProductView.as_view(), name='creacion_producto'),
    path('listar_gastos/', ListExpenseView.as_view(), name='listar_gastos'),
    path('actualizar_gastos/<int:producto_id>', UpdateExpenseView.as_view(), name='actualizar_gastos'),
    path('borrar_gasto/<int:producto_id>', DeleteExpenseView.as_view(), name='borrar_gastos'),


]
