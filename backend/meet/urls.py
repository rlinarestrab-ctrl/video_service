from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    SalaVideoconferenciaViewSet,
    ParticipanteSalaViewSet,
    AgendamientoCitaViewSet,
)

router = DefaultRouter()
router.register(r"salas", SalaVideoconferenciaViewSet)
router.register(r"participantes", ParticipanteSalaViewSet)
router.register(r"citas", AgendamientoCitaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
