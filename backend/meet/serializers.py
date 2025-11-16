from rest_framework import serializers
from .models import SalaVideoconferencia, ParticipanteSala, AgendamientoCita

class SalaVideoconferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaVideoconferencia
        fields = "__all__"
        extra_kwargs = {
            "orientador_id": {"required": False},  # 👈 Ya no obligatorio
        }


class ParticipanteSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipanteSala
        fields = "__all__"


class AgendamientoCitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendamientoCita
        fields = "__all__"
