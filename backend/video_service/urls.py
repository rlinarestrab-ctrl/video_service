from django.urls import path, include
from django.http import JsonResponse

def health(_):
    return JsonResponse({"status": "ok", "service": "video_service"})

urlpatterns = [
    path("api/health/", health),
    path("api/meet/", include("meet.urls")),  # lo creamos vacío ahora y lo completamos en el Paso 2
]
