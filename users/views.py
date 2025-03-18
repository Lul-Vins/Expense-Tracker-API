from django.shortcuts import render
from .models import User
from .serializers import UserRegister
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class RegisterUserView(CreateAPIView): # Hereda de CreateAPIView, que es una vista genérica de Django REST Framework (DRF) especializada en crear objetos.
    queryset = User.objects.all() # Define el conjunto de datos sobre el cual trabaja la vista. Recupera todos los usuarios de la base de datos.
    serializer_class = UserRegister # Indica qué serializador usará la vista para manejar la validación y transformación de los datos. UserRegister es el serializador que define cómo se valida y transforma un usuario antes de guardarlo.
    permission_classes = [AllowAny] # Especifica las permisiones para acceder a la vista.

    def perform_create(self, serializer): # Sobrescribe el método perform_create() de CreateApiView.  Se ejecuta cuando serializer.save() es llamado, permitiéndonos personalizar la creación del usuario.
        serializer.save() # Llama al método create() del serializador UserRegister. Este método crea un nuevo usuario en la base de datos. También ejecuta las validaciones definidas en UserRegister.
        return Response(
            {"message": "Usuario registrado con éxito"},
            status=status.HTTP_201_CREATED
        )
        