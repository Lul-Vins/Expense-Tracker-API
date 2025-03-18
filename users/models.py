from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings

class CustomUserManager(BaseUserManager): 
    def _create_user(self, email, password=None, **extra_fields): # create_user() es un método de instancia que define cómo se debe crear un usuario en la BD. 
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email) # normalize_email(email) es un método de BaseUserManager que convierte el email a minúsculas y lo formatea correctamente.
        user = self.model(email=email, **extra_fields) # self.model se refiere al modelo de usuario que usa este Manager. jango asigna automáticamente self.model cuando defines el objects = CustomUserManager() en tu modelo de usuario 
        user.set_password(password) # set_password(password) es un método heredado de AbstractBaseUser. Encripta la contraseña antes de guadarla en la BD con un hash
        user.save(using=self._db) # Esto guarda el usuario en la base de datos, self._db es una referencia a la base de datos que django esta usando, en la mayoria de casos es default pero si hay muchas bases de datos conectadas, se usa para guardarla en la bd especifica
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email,password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True) # Indica si el usuario está activo o no. Django lo usa para deshabilitar cuentas sin eliminarlas.
    is_staff = models.BooleanField(default=False) # Indica si el usuario tiene permisos de staff (puede acceder al panel de administración).
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager() # objects se vincula con CustomUserManager, el cual define cómo se crean los usuarios y superusuarios. Es el gestor de consultas de este modelo (User.objects llamará a los métodos de CustomUserManager).

    class Meta: # Define el nombre que tendrá el modelo en el Django Admin
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email.split("@")[0]
    
    USERNAME_FIELD = "email" #  Define qué campo se usará para autenticación en Django.

    REQUIRED_FIELDS = [] # Son los campos adicionales obligatorios cuando se crea un superusuario
    
    def __str__(self):
        return self.email 