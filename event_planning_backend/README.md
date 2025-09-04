# Event Planning Backend

A simple Flask backend with RESTful APIs to manage Events and Attendees. Uses file-based JSON persistence (no external database).

- Framework: Flask + flask-smorest (OpenAPI docs)
- Persistence: `app/data.json` file (auto-created)
- Docs: Swagger UI available at `/docs`

## Getting Started

1. Install dependencies:
   pip install -r requirements.txt

2. Run the server:
   python run.py

3. Open API docs in your browser:
   http://localhost:5000/docs

## API Overview

- GET `/` Health check
- Events
  - GET `/events/` List events (query `include_attendees=true` to expand attendees)
  - POST `/events/` Create event
  - GET `/events/{id}` Get event (includes attendees)
  - PATCH `/events/{id}` Update event
  - DELETE `/events/{id}` Delete event
  - PUT `/events/{id}/attendees` Replace attendee_ids list for event
- Attendees
  - GET `/attendees/` List attendees
  - POST `/attendees/` Create attendee
  - GET `/attendees/{id}` Get attendee
  - PATCH `/attendees/{id}` Update attendee
  - DELETE `/attendees/{id}` Delete attendee

## Notes

- Relationships are maintained by storing `attendee_ids` on each event.
- Deleting an attendee removes their ID from all events.
- Creating/updating events validates that provided `attendee_ids` exist.

## Development

- Code organization:
  - `app/models.py` Dataclasses for Event/Attendee
  - `app/schemas.py` Marshmallow schemas
  - `app/storage.py` JSON file storage engine
  - `app/services.py` Business logic for events/attendees
  - `app/routes/*` Flask Blueprints for endpoints
  - `app/__init__.py` App and blueprint registration
  - `run.py` App entrypoint

- Testing manually:
  Create attendee:
    curl -X POST http://localhost:5000/attendees/ -H "Content-Type: application/json" -d '{"name":"Alice","email":"alice@example.com"}'

  Create event:
    curl -X POST http://localhost:5000/events/ -H "Content-Type: application/json" -d '{"title":"Kickoff","description":"Project kickoff"}'

  List events:
    curl http://localhost:5000/events/

## Configuration

- No environment variables required. Optionally set `EVENT_PLANNING_DATA_FILE` to change the data path.
