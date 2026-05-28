# UC05 Backend Prototype

Runnable backend for the predictive quality demo. It uses only the Python
standard library, so it does not require package installation.

```bash
python3 backend/server.py
```

Base URL:

```text
http://127.0.0.1:8025
```

## Endpoints

- `GET /api/health`
- `GET /api/variants`
- `GET /api/events?limit=25`
- `POST /api/events/generate`
- `GET /api/incidents`
- `GET /api/model-versions`
- `POST /api/model-versions/retrain`
- `GET /api/events/stream?variant_id=ioniq5&line_speed=54&drift=1`

## Example Event Generate Request

```json
{
  "variant_id": "ioniq5",
  "line_speed": 58,
  "drift": 1.4
}
```

The backend persists generated events, quality holds, incidents, and model
versions into `quality_demo.sqlite3`.
