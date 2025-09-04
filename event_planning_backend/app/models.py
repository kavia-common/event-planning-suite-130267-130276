"""
Domain models for Event Planning Backend.
Includes dataclasses for Event and Attendee and helper functions for ID handling.

These models do not directly manage persistence; see storage layer for that.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict
from datetime import datetime
import uuid


def _new_id() -> str:
    """Generate a new unique identifier."""
    return str(uuid.uuid4())


@dataclass
class Attendee:
    """
    Represents an attendee of an event.
    """
    id: str
    name: str
    email: str
    # event_id is optional here; relationship maintained in Event
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    # PUBLIC_INTERFACE
    def to_dict(self) -> Dict:
        """Serialize Attendee to a dictionary."""
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict) -> "Attendee":
        """Create Attendee from dict."""
        return Attendee(
            id=data.get("id") or _new_id(),
            name=data["name"],
            email=data["email"],
            created_at=data.get("created_at") or datetime.utcnow().isoformat() + "Z",
            updated_at=data.get("updated_at") or datetime.utcnow().isoformat() + "Z",
        )


@dataclass
class Event:
    """
    Represents an event with multiple attendees.
    """
    id: str
    title: str
    description: Optional[str] = ""
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = ""
    attendee_ids: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    # PUBLIC_INTERFACE
    def to_dict(self) -> Dict:
        """Serialize Event to a dictionary."""
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict) -> "Event":
        """Create Event from dict."""
        return Event(
            id=data.get("id") or _new_id(),
            title=data["title"],
            description=data.get("description") or "",
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            location=data.get("location") or "",
            attendee_ids=list(data.get("attendee_ids") or []),
            created_at=data.get("created_at") or datetime.utcnow().isoformat() + "Z",
            updated_at=data.get("updated_at") or datetime.utcnow().isoformat() + "Z",
        )
