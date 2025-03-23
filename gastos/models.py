from django.db import models
from  users.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    producto_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="productos")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL,null=True, blank=True )
    def __str__(self):
        return self.nombre



