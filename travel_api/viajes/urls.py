from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ViajeViewSet, DestinoViewSet, ItinerarioViewSet, ActividadViewSet

router = DefaultRouter()
router.register(r'viajes', ViajeViewSet)
router.register(r'destinos', DestinoViewSet)
router.register(r'itinerarios', ItinerarioViewSet)
router.register(r'actividades', ActividadViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
