from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from datetime import datetime, timedelta
from django.utils import timezone
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
        
        filtro = self.request.query_params.get('filtro')  
        if not filtro:
            return Producto.objects.filter(usuario=self.request.user)
        
        elif filtro == 'ultima_semana':
            hoy = datetime.now()
            hoy_conv = timezone.make_aware(hoy, timezone=timezone.get_current_timezone())
            ultima_semana= hoy - timedelta(days=7)
            ultima_semana_conv = timezone.make_aware(ultima_semana, timezone=timezone.get_current_timezone())

            return Producto.objects.filter(usuario=self.request.user, fecha_actualizacion__range=[ultima_semana_conv,hoy_conv])
        
        elif filtro == 'ultimo_mes':
            hoy = datetime.now()
            hoy_conv = timezone.make_aware(hoy, timezone=timezone.get_current_timezone())
            ultimo_mes = hoy - timedelta(days=30)
            ultimo_mes_conv = timezone.make_aware(ultimo_mes, timezone=timezone.get_current_timezone())

            return Producto.objects.filter(usuario=self.request.user, fecha_actualizacion__range=[ultimo_mes_conv, hoy_conv])

        elif filtro == 'ultimos_3_meses':
            hoy = datetime.now()
            hoy_conv = timezone.make_aware(hoy, timezone=timezone.get_current_timezone())
            tres_meses = hoy - timedelta(days=90)
            tres_meses_conv = timezone.make_aware(tres_meses, timezone=timezone.get_current_timezone())

            return Producto.objects.filter(usuario=self.request.user, fecha_actualizacion__range=[tres_meses_conv, hoy_conv])
        
        else:
            fecha_inicio = self.request.query_params.get('fecha_inicio')
            fecha_final = self.request.query_params.get('fecha_final')

            if not fecha_inicio or not fecha_final:
                return Producto.objects.none()  # O devuelve un error HTTP 400

            try:
                fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
                fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d").date()


            except ValueError:
                return Producto.objects.none()  # O devuelve un error HTTP 400

            if fecha_inicio > fecha_final:
                return Producto.objects.none()  # O devuelve un error HTTP 400

            return Producto.objects.filter(usuario=self.request.user,fecha_actualizacion__range=[fecha_inicio, fecha_final])
            


            

class DeleteExpenseView(generics.DestroyAPIView):
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "producto_id"
    
    def get_queryset(self):
        expense = self.kwargs['producto_id']
        return Producto.objects.filter(usuario=self.request.user, producto_id=expense)
    

