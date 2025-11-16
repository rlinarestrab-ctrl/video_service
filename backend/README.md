# Meet Service Backend (Django + DRF)

Microservicio para crear eventos de Google Calendar con enlace de Google Meet.

## Requisitos
- Python 3.11+
- PostgreSQL 15+
- Variables de entorno (o Docker) para credenciales de Google y DB.

## Variables de entorno (ejemplo .env)
```env
DJANGO_SECRET_KEY=dev-secret
DJANGO_DEBUG=1
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=http://localhost:5173

POSTGRES_DB=meet_service_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

GOOGLE_CLIENT_ID=TU_CLIENT_ID
GOOGLE_CLIENT_SECRET=TU_CLIENT_SECRET
GOOGLE_REDIRECT_URI=http://localhost:8003/api/meet/oauth/callback/
```

## Endpoints
- `GET /api/meet/oauth/start/` → URL de autorización Google
- `GET /api/meet/oauth/callback/` → Callback OAuth
- `POST /api/meet/events/` → Crea evento con Meet
- `GET /api/meet/events/list/` → Lista próximos eventos
- `POST /api/meet/watch/start/` → Inicia webhook (opcional)
- `POST /api/meet/webhook/calendar/` → Recibe notificaciones (opcional)

**Header requerido**: `X-User-Id: <uuid del usuario>`

## Ejecutar local (sin Docker)
```bash
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## Docker
```bash
docker compose up -d --build
```
