"""
JSON file-based storage for events and attendees.

This provides a very simple persistence layer without requiring a database.
It stores two top-level lists: events and attendees. Relationships are managed
via IDs.
"""
import json
import os
from typing import Dict, Any, List, Optional
from threading import RLock
from datetime import datetime

DEFAULT_DATA_PATH = os.environ.get(
    "EVENT_PLANNING_DATA_FILE",
    os.path.join(os.path.dirname(__file__), "data.json"),
)

_LOCK = RLock()


class Storage:
    """
    File-based storage abstraction.
    """

    def __init__(self, path: str = DEFAULT_DATA_PATH) -> None:
        self.path = path
        # Ensure file exists with default structure
        with _LOCK:
            if not os.path.exists(self.path):
                self._write({"events": [], "attendees": []})

    def _read(self) -> Dict[str, Any]:
        with _LOCK:
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                # Reinitialize corrupt file
                data = {"events": [], "attendees": []}
                self._write(data)
                return data

    def _write(self, data: Dict[str, Any]) -> None:
        with _LOCK:
            tmp_path = self.path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, sort_keys=True)
            os.replace(tmp_path, self.path)

    # PUBLIC_INTERFACE
    def list_events(self) -> List[Dict[str, Any]]:
        """List all events."""
        data = self._read()
        return list(data.get("events", []))

    # PUBLIC_INTERFACE
    def list_attendees(self) -> List[Dict[str, Any]]:
        """List all attendees."""
        data = self._read()
        return list(data.get("attendees", []))

    # PUBLIC_INTERFACE
    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get event by id."""
        for e in self.list_events():
            if e["id"] == event_id:
                return e
        return None

    # PUBLIC_INTERFACE
    def get_attendee(self, attendee_id: str) -> Optional[Dict[str, Any]]:
        """Get attendee by id."""
        for a in self.list_attendees():
            if a["id"] == attendee_id:
                return a
        return None

    # PUBLIC_INTERFACE
    def save_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update an event by ID."""
        data = self._read()
        events = data.get("events", [])
        replaced = False
        for idx, e in enumerate(events):
            if e["id"] == event["id"]:
                events[idx] = event
                replaced = True
                break
        if not replaced:
            events.append(event)
        data["events"] = events
        self._write(data)
        return event

    # PUBLIC_INTERFACE
    def save_attendee(self, attendee: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update an attendee by ID."""
        data = self._read()
        attendees = data.get("attendees", [])
        replaced = False
        for idx, a in enumerate(attendees):
            if a["id"] == attendee["id"]:
                attendees[idx] = attendee
                replaced = True
                break
        if not replaced:
            attendees.append(attendee)
        data["attendees"] = attendees
        self._write(data)
        return attendee

    # PUBLIC_INTERFACE
    def delete_event(self, event_id: str) -> bool:
        """Delete event by id, and remove its reference from attendees (no hard delete of attendees)."""
        data = self._read()
        before = len(data.get("events", []))
        data["events"] = [e for e in data.get("events", []) if e["id"] != event_id]
        after = len(data["events"])
        # Also remove attendee references to this event (if we stored reverse; we don't store here)
        self._write(data)
        return after < before

    # PUBLIC_INTERFACE
    def delete_attendee(self, attendee_id: str) -> bool:
        """Delete attendee by id, and remove it from any event attendee_ids."""
        data = self._read()
        before = len(data.get("attendees", []))
        data["attendees"] = [a for a in data.get("attendees", []) if a["id"] != attendee_id]
        # Remove from events' attendee_ids
        for e in data.get("events", []):
            if "attendee_ids" in e:
                e["attendee_ids"] = [aid for aid in e["attendee_ids"] if aid != attendee_id]
        after = len(data["attendees"])
        self._write(data)
        return after < before

    # PUBLIC_INTERFACE
    def set_event_attendees(self, event_id: str, attendee_ids: List[str]) -> Optional[Dict[str, Any]]:
        """Replace the attendee_ids list for an event."""
        data = self._read()
        found = None
        for e in data.get("events", []):
            if e["id"] == event_id:
                e["attendee_ids"] = attendee_ids
                e["updated_at"] = datetime.utcnow().isoformat() + "Z"
                found = e
                break
        if found is not None:
            self._write(data)
        return found
