"""
Service layer encapsulating business logic for events and attendees.
"""
from typing import Dict, List, Optional
from datetime import datetime

from .models import Event, Attendee
from .storage import Storage


class EventService:
    """
    Provides operations for managing events and their attendee relationships.
    """
    def __init__(self, storage: Storage):
        self.storage = storage

    # PUBLIC_INTERFACE
    def list_events(self, include_attendees: bool = False) -> List[Dict]:
        """Return list of events; optionally expand attendees."""
        events = [Event.from_dict(e) for e in self.storage.list_events()]
        if not include_attendees:
            return [e.to_dict() for e in events]
        # include attendees
        attendees_map = {a["id"]: a for a in self.storage.list_attendees()}
        result = []
        for e in events:
            obj = e.to_dict()
            obj["attendees"] = [attendees_map[aid] for aid in e.attendee_ids if aid in attendees_map]
            result.append(obj)
        return result

    # PUBLIC_INTERFACE
    def get_event(self, event_id: str, include_attendees: bool = False) -> Optional[Dict]:
        """Get single event; optionally include attendees."""
        e = self.storage.get_event(event_id)
        if not e:
            return None
        event = Event.from_dict(e)
        obj = event.to_dict()
        if include_attendees:
            attendees_map = {a["id"]: a for a in self.storage.list_attendees()}
            obj["attendees"] = [attendees_map[aid] for aid in event.attendee_ids if aid in attendees_map]
        return obj

    # PUBLIC_INTERFACE
    def create_event(self, payload: Dict) -> Dict:
        """Create a new event, validating attendee_ids existence."""
        now = datetime.utcnow().isoformat() + "Z"
        attendee_ids = list(payload.get("attendee_ids") or [])
        # validate attendees
        valid_ids = {a["id"] for a in self.storage.list_attendees()}
        for aid in attendee_ids:
            if aid not in valid_ids:
                raise ValueError(f"Attendee id not found: {aid}")

        event = Event.from_dict({
            "title": payload["title"],
            "description": payload.get("description"),
            "start_time": payload.get("start_time"),
            "end_time": payload.get("end_time"),
            "location": payload.get("location"),
            "attendee_ids": attendee_ids,
            "created_at": now,
            "updated_at": now,
        })
        return self.storage.save_event(event.to_dict())

    # PUBLIC_INTERFACE
    def update_event(self, event_id: str, payload: Dict) -> Optional[Dict]:
        """Update an event's fields, validating attendee_ids when provided."""
        current = self.storage.get_event(event_id)
        if not current:
            return None
        event = Event.from_dict(current)

        if "title" in payload and payload["title"] is not None:
            event.title = payload["title"]
        if "description" in payload:
            event.description = payload["description"]
        if "start_time" in payload:
            event.start_time = payload["start_time"]
        if "end_time" in payload:
            event.end_time = payload["end_time"]
        if "location" in payload:
            event.location = payload["location"]
        if "attendee_ids" in payload and payload["attendee_ids"] is not None:
            provided = list(payload["attendee_ids"])
            valid_ids = {a["id"] for a in self.storage.list_attendees()}
            for aid in provided:
                if aid not in valid_ids:
                    raise ValueError(f"Attendee id not found: {aid}")
            event.attendee_ids = provided

        event.updated_at = datetime.utcnow().isoformat() + "Z"
        return self.storage.save_event(event.to_dict())

    # PUBLIC_INTERFACE
    def delete_event(self, event_id: str) -> bool:
        """Delete an event by id."""
        return self.storage.delete_event(event_id)

    # PUBLIC_INTERFACE
    def replace_event_attendees(self, event_id: str, attendee_ids: List[str]) -> Optional[Dict]:
        """Replace the attendee list for an event."""
        valid_ids = {a["id"] for a in self.storage.list_attendees()}
        for aid in attendee_ids:
            if aid not in valid_ids:
                raise ValueError(f"Attendee id not found: {aid}")
        updated = self.storage.set_event_attendees(event_id, attendee_ids)
        return updated


class AttendeeService:
    """
    Provides operations for managing attendees.
    """
    def __init__(self, storage: Storage):
        self.storage = storage

    # PUBLIC_INTERFACE
    def list_attendees(self) -> List[Dict]:
        """List all attendees."""
        return self.storage.list_attendees()

    # PUBLIC_INTERFACE
    def get_attendee(self, attendee_id: str) -> Optional[Dict]:
        """Get a single attendee by id."""
        return self.storage.get_attendee(attendee_id)

    # PUBLIC_INTERFACE
    def create_attendee(self, payload: Dict) -> Dict:
        """Create a new attendee."""
        now = datetime.utcnow().isoformat() + "Z"
        attendee = Attendee.from_dict({
            "name": payload["name"],
            "email": payload["email"],
            "created_at": now,
            "updated_at": now,
        })
        return self.storage.save_attendee(attendee.to_dict())

    # PUBLIC_INTERFACE
    def update_attendee(self, attendee_id: str, payload: Dict) -> Optional[Dict]:
        """Update attendee fields."""
        current = self.storage.get_attendee(attendee_id)
        if not current:
            return None
        attendee = Attendee.from_dict(current)
        if "name" in payload and payload["name"] is not None:
            attendee.name = payload["name"]
        if "email" in payload and payload["email"] is not None:
            attendee.email = payload["email"]
        attendee.updated_at = datetime.utcnow().isoformat() + "Z"
        return self.storage.save_attendee(attendee.to_dict())

    # PUBLIC_INTERFACE
    def delete_attendee(self, attendee_id: str) -> bool:
        """Delete attendee and remove them from any events."""
        return self.storage.delete_attendee(attendee_id)
