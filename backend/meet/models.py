from django.db import models
import uuid

class SalaVideoconferencia(models.Model):
    ESTADOS = [
        ("programada", "Programada"),
        ("en_curso", "En curso"),
        ("finalizada", "Finalizada"),
        ("cancelada", "Cancelada"),
    ]
    TIPOS_ORGANIZADOR = [
        ("orientador", "Orientador"),
        ("institucion", "Institución"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    orientador_id = models.UUIDField(blank=True, null=True)
    institucion_id = models.UUIDField(blank=True, null=True)
    fecha_programada = models.DateTimeField()
    duracion_estimada = models.PositiveIntegerField(help_text="Duración en minutos", blank=True, null=True)
    max_participantes = models.PositiveIntegerField(default=50)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="programada")
    sala_id = models.CharField(max_length=100, blank=True, null=True)
    enlace_acceso = models.URLField(blank=True, null=True)
    tipo_organizador = models.CharField(max_length=20, choices=TIPOS_ORGANIZADOR, blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} ({self.estado})"


class ParticipanteSala(models.Model):
    ROLES = [
        ("presentador", "Presentador"),
        ("participante", "Participante"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sala = models.ForeignKey(SalaVideoconferencia, on_delete=models.CASCADE, related_name="participantes")
    usuario_id = models.UUIDField()
    rol = models.CharField(max_length=20, choices=ROLES, default="participante")
    fecha_union = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario_id} en {self.sala.titulo}"


class AgendamientoCita(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
        ("completada", "Completada"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estudiante_id = models.UUIDField()
    orientador_id = models.UUIDField(blank=True, null=True)
    institucion_id = models.UUIDField(blank=True, null=True)
    sala = models.ForeignKey(SalaVideoconferencia, on_delete=models.SET_NULL, blank=True, null=True, related_name="citas")
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_cita = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    motivo = models.TextField(blank=True, null=True)
    duracion = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"Cita {self.id} - {self.estado}"
