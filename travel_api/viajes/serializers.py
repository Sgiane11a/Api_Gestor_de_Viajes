from rest_framework import serializers
from .models import Viaje, Destino, Itinerario, Actividad

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'

class ItinerarioSerializer(serializers.ModelSerializer):
    actividades = ActividadSerializer(many=True, read_only=True)

    class Meta:
        model = Itinerario
        fields = '__all__'

class DestinoSerializer(serializers.ModelSerializer):
    itinerarios = ItinerarioSerializer(many=True, read_only=True)

    class Meta:
        model = Destino
        fields = '__all__'

class ViajeSerializer(serializers.ModelSerializer):
    destinos = DestinoSerializer(many=True, read_only=True)

    class Meta:
        model = Viaje
        fields = '__all__'
