from flask_smorest import Blueprint, abort
from flask.views import MethodView

from ..schemas import (
    EventSchema,
    EventCreateSchema,
    EventUpdateSchema,
    EventWithAttendeesSchema,
)
from ..services import EventService
from ..storage import Storage

blp = Blueprint(
    "Events",
    "events",
    url_prefix="/events",
    description="Operations on events and their attendees",
)

_storage = Storage()
_service = EventService(_storage)


@blp.route("/")
class EventsCollection(MethodView):
    """List and create events."""

    @blp.response(200, EventSchema(many=True), description="List events")
    def get(self):
        """
        List events.

        Query params:
        - include_attendees: if 'true', include attendees array in each event.
        """
        from flask import request

        include_attendees = str(request.args.get("include_attendees", "false")).lower() == "true"
        return _service.list_events(include_attendees=include_attendees)

    @blp.arguments(EventCreateSchema, location="json")
    @blp.response(201, EventSchema, description="Created event")
    def post(self, json_data):
        """
        Create a new event.

        Body: EventCreate schema
        """
        try:
            created = _service.create_event(json_data)
            return created
        except ValueError as e:
            abort(400, message=str(e))


@blp.route("/<string:event_id>")
class EventItem(MethodView):
    """Retrieve, update, and delete a single event."""

    @blp.response(200, EventWithAttendeesSchema, description="Event details")
    def get(self, event_id: str):
        """
        Get a single event by ID with attendees list.
        """
        obj = _service.get_event(event_id, include_attendees=True)
        if not obj:
            abort(404, message="Event not found")
        return obj

    @blp.arguments(EventUpdateSchema, location="json")
    @blp.response(200, EventSchema, description="Updated event")
    def patch(self, json_data, event_id: str):
        """
        Update an event partially.
        """
        try:
            updated = _service.update_event(event_id, json_data)
            if not updated:
                abort(404, message="Event not found")
            return updated
        except ValueError as e:
            abort(400, message=str(e))

    @blp.response(204)
    def delete(self, event_id: str):
        """
        Delete an event.
        """
        ok = _service.delete_event(event_id)
        if not ok:
            abort(404, message="Event not found")
        return ""


@blp.route("/<string:event_id>/attendees")
class EventAttendeesReplace(MethodView):
    """Replace attendee list on an event."""
    @blp.arguments(
        EventUpdateSchema(only=("attendee_ids",)),
        location="json",
    )
    @blp.response(200, EventSchema, description="Event with updated attendee_ids")
    def put(self, json_data, event_id: str):
        """
        Replace attendees for the event by providing attendee_ids list in body.
        """
        ids = json_data.get("attendee_ids") or []
        try:
            updated = _service.replace_event_attendees(event_id, ids)
            if not updated:
                abort(404, message="Event not found")
            return updated
        except ValueError as e:
            abort(400, message=str(e))
