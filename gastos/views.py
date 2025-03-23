from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *

# Create your views here.

class CreateProductView(generics.CreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class UpdateExpenseView(generics.UpdateAPIView):
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "producto_id"

    def get_queryset(self):
        expense = self.kwargs['producto_id']
        return Producto.objects.filter(usuario=self.request.user, producto_id=expense)

class ListExpenseView(generics.ListAPIView):
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Producto.objects.filter(usuario=self.request.user)

class DeleteExpenseView(generics.DestroyAPIView):
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "producto_id"
    
    def get_queryset(self):
        expense = self.kwargs['producto_id']
        return Producto.objects.filter(usuario=self.request.user, producto_id=expense)


    
        