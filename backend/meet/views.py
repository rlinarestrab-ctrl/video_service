import requests
from django.conf import settings
from rest_framework import viewsets, permissions, renderers
from rest_framework.exceptions import PermissionDenied
from .models import SalaVideoconferencia, ParticipanteSala, AgendamientoCita
from .serializers import (
    SalaVideoconferenciaSerializer,
    ParticipanteSalaSerializer,
    AgendamientoCitaSerializer,
)

# ------------------------------------------
# 🔐 Permisos personalizados
# ------------------------------------------
class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        rol = getattr(request.user, "rol", None)
        if view.action in ["list", "retrieve"]:
            return True
        if view.action in ["create", "update", "partial_update", "destroy"]:
            return rol in ["admin", "orientador"]
        return False

# ------------------------------------------
# 🎥 Vista: Salas de Videoconferencia
# ------------------------------------------
from datetime import datetime, timedelta
from .services_google import crear_evento_google

class SalaVideoconferenciaViewSet(viewsets.ModelViewSet):
    queryset = SalaVideoconferencia.objects.all().order_by("-fecha_programada")
    serializer_class = SalaVideoconferenciaSerializer
    permission_classes = [CustomPermission]
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]

    def perform_create(self, serializer):
        """Crea la sala en la BD y en Google Calendar (si hay token)."""
        user = self.request.user
        rol = getattr(user, "rol", None)

        if rol not in ["admin", "orientador"]:
            raise PermissionDenied("Solo orientadores o administradores pueden crear reuniones.")

        google_token = self.request.headers.get("Google-Access-Token")
        enlace_meet = None

        if google_token:
            try:
                titulo = self.request.data.get("titulo", "Reunión Orientación Vocacional")
                descripcion = self.request.data.get("descripcion", "")
                fecha_inicio = self.request.data.get("fecha_programada")

                # 🔹 Convertir a objeto datetime y agregar 1 hora de duración
                inicio = datetime.fromisoformat(fecha_inicio)
                fin = inicio + timedelta(hours=1)

                enlace_meet = crear_evento_google(
                    google_token=google_token,
                    titulo=titulo,
                    descripcion=descripcion,
                    inicio=inicio,
                    fin=fin,
                    usuario_id=str(user.id)
                )

            except Exception as e:
                print("❌ Error al crear evento en Google Calendar:", str(e))
        else:
            print("⚠️ No se proporcionó Google-Access-Token; solo se crea en BD local.")

        # Guardar en base de datos local
        serializer.save(
            orientador_id=user.id,
            enlace_acceso=enlace_meet,
        )


# ------------------------------------------
# 👥 Vista: Participantes
# ------------------------------------------
class ParticipanteSalaViewSet(viewsets.ModelViewSet):
    queryset = ParticipanteSala.objects.all()
    serializer_class = ParticipanteSalaSerializer
    permission_classes = [CustomPermission]
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]


# ------------------------------------------
# 📅 Vista: Agendamiento de Citas
# ------------------------------------------
class AgendamientoCitaViewSet(viewsets.ModelViewSet):
    queryset = AgendamientoCita.objects.all().order_by("-fecha_cita")
    serializer_class = AgendamientoCitaSerializer
    permission_classes = [CustomPermission]
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]
