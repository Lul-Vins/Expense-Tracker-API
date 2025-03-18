from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
import re

class UserRegister(serializers.ModelSerializer): # Hereda de serializers.Serializer, pero con menos código repetitivo. Se usa para transformar datos de entrada/salida a partir del modelo User.
    class Meta: # Define la configuración del serializador. DRF) usa esta clase para saber qué modelo y qué campos debe manejar.
        model = User # Asigna el modelo User que defini en la app.
        fields = ['email', 'password'] # Especifica los campos que manejará el serializador.
        extra_kwargs = {
            'password' : {'write_only' : True, 'min_length' : 8} # Define configuraciones adicionales para ciertos campos. write_only: True → El campo password solo se usará para escritura, no se enviará en respuestas.
        }
    
    def validate_password(self, value): # Valida la contraseña antes de guardarla. value es la contraseña ingresada por el usuario.
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("La contraseña debe contener una letra mayúscula")
        if len(value) < 8:
            print("Ejecutando validación de contraseña") 
            raise serializers.ValidationError("La contraseña debe ser de 8 caractereces como minimo")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("La contraseña debe contener un caracter especial")
        return value 
    
    def validate_email(self, value): # Valida el email antes de guardarlo. value es el email enviado por el usuario
        if User.objects.filter(email=value).exists(): # Consulta la base de datos: si el email ya existe, lanza un error de validación.
            raise serializers.ValidationError("No se pudo completar el registro")
        return value
    
    def create(self, validated_data): # Crea y guarda un usuario con los datos validados. validated_data es un diccionario con los datos ya validados del usuario.
        password = validated_data.pop('password', None) # Extrae la contraseña del diccionario de datos y la elimina de ahí. Se usa pop() para sacar password, evitando que se almacene en texto plano.
        if not password:
            raise serializers.ValidationError({'password': "Este campo es obligatorio" })
        
        user = User(**validated_data) # Crea una instancia del modelo User con los datos restantes. No incluye la contraseña todavía.

        if password: # Encripta la contraseña antes de guardarla. set_password(password) usa el sistema de hash de Django para almacenarla de forma segura.
            user.set_password(password)
        user.save() # Guarda el usuario en la base de datos
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Credenciales incorrectas")
        return user