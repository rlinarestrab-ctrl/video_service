import os
import jwt
from types import SimpleNamespace
from rest_framework import authentication, exceptions

# 🔹 Carga la clave y el algoritmo desde variables de entorno
JWT_SECRET = os.getenv("JWT_SECRET", os.getenv("DJANGO_SECRET_KEY", "dev-secret"))
JWT_ALG = os.getenv("JWT_ALG", "HS256")


class JWTUserAuthentication(authentication.BaseAuthentication):
    """
    Autenticación basada en JWT emitido por auth_service.
    Lee Authorization: Bearer <token> y crea un objeto 'user' con los datos del payload.
    """

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).decode("utf-8")

        if not auth_header or not auth_header.lower().startswith("bearer "):
            return None  # sin token → usuario anónimo (permite vistas públicas)

        token = auth_header.split(" ", 1)[1].strip()

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expirado")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Token inválido")

        # 🔹 Crear un usuario temporal con los datos del payload
        user = SimpleNamespace(
            id=payload.get("id") or payload.get("user_id"),
            email=payload.get("email"),
            rol=payload.get("rol"),
            nombre=payload.get("nombre", ""),
            is_authenticated=True,
        )

        if not user.id:
            raise exceptions.AuthenticationFailed("Token sin ID de usuario válido")

        return (user, None)
