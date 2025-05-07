from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Viaje, Destino, Itinerario, Actividad
from .serializers import ViajeSerializer, DestinoSerializer, ItinerarioSerializer, ActividadSerializer

class ViajeViewSet(viewsets.ModelViewSet):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer

    @action(detail=True, methods=['get'])
    def presupuesto(self, request, pk=None):
        viaje = self.get_object()
        actividades = Actividad.objects.filter(itinerario__destino__viaje=viaje)
        total_gasto = sum([a.costo for a in actividades])
        restante = viaje.presupuesto - total_gasto
        return Response({
            "presupuesto": viaje.presupuesto,
            "gastado": total_gasto,
            "restante": restante
        })

class DestinoViewSet(viewsets.ModelViewSet):
    queryset = Destino.objects.all()
    serializer_class = DestinoSerializer

class ItinerarioViewSet(viewsets.ModelViewSet):
    queryset = Itinerario.objects.all()
    serializer_class = ItinerarioSerializer

    @action(detail=True, methods=['post'])
    def planificar(self, request, pk=None):
        itinerario = self.get_object()
        actividades_data = request.data.get('actividades', [])
        creadas = []

        for data in actividades_data:
            data['itinerario'] = itinerario.id
            serializer = ActividadSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                creadas.append(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        return Response({"actividades_creadas": creadas})

    @action(detail=True, methods=['post'])
    def compartir(self, request, pk=None):
        itinerario = self.get_object()
        username = request.data.get('username')
        try:
            usuario = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)
        
        # Crear una copia del itinerario
        nuevo = Itinerario.objects.create(
            destino=itinerario.destino,
            fecha=itinerario.fecha,
            descripcion=f"(Compartido) {itinerario.descripcion}"
        )
        for actividad in itinerario.actividades.all():
            Actividad.objects.create(
                itinerario=nuevo,
                nombre=actividad.nombre,
                hora=actividad.hora,
                costo=actividad.costo
            )
        return Response({"mensaje": f"Itinerario compartido con {usuario.username}."})

class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
