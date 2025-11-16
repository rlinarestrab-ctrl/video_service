import requests

def crear_evento_google(google_token, titulo, descripcion, inicio, fin, usuario_id):
    """Crea un evento en Google Calendar y devuelve el enlace Meet."""
    event_data = {
        "summary": titulo,
        "description": descripcion,
        "start": {"dateTime": inicio.isoformat(), "timeZone": "America/Guatemala"},
        "end": {"dateTime": fin.isoformat(), "timeZone": "America/Guatemala"},
        "conferenceData": {
            "createRequest": {
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
                "requestId": f"meet-{usuario_id}",
            }
        },
    }

    headers = {
        "Authorization": f"Bearer {google_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://www.googleapis.com/calendar/v3/calendars/primary/events?conferenceDataVersion=1",
        json=event_data,
        headers=headers,
    )

    if response.status_code not in [200, 201]:
        print("⚠️ Google Calendar error:", response.text)
        return None

    data = response.json()
    enlace_meet = data.get("hangoutLink")
    print(f"✅ Evento creado: {enlace_meet}")
    return enlace_meet
