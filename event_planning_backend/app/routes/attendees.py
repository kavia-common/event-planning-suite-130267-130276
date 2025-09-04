from flask_smorest import Blueprint, abort
from flask.views import MethodView

from ..schemas import (
    AttendeeSchema,
    AttendeeCreateSchema,
    AttendeeUpdateSchema,
)
from ..services import AttendeeService
from ..storage import Storage

blp = Blueprint(
    "Attendees",
    "attendees",
    url_prefix="/attendees",
    description="Operations on attendees",
)

_storage = Storage()
_service = AttendeeService(_storage)


@blp.route("/")
class AttendeesCollection(MethodView):
    """List and create attendees."""

    @blp.response(200, AttendeeSchema(many=True), description="List attendees")
    def get(self):
        """
        List all attendees.
        """
        return _service.list_attendees()

    @blp.arguments(AttendeeCreateSchema, location="json")
    @blp.response(201, AttendeeSchema, description="Created attendee")
    def post(self, json_data):
        """
        Create a new attendee.
        """
        created = _service.create_attendee(json_data)
        return created


@blp.route("/<string:attendee_id>")
class AttendeeItem(MethodView):
    """Get, update, delete attendee."""

    @blp.response(200, AttendeeSchema, description="Attendee details")
    def get(self, attendee_id: str):
        """
        Get attendee by id.
        """
        obj = _service.get_attendee(attendee_id)
        if not obj:
            abort(404, message="Attendee not found")
        return obj

    @blp.arguments(AttendeeUpdateSchema, location="json")
    @blp.response(200, AttendeeSchema, description="Updated attendee")
    def patch(self, json_data, attendee_id: str):
        """
        Update attendee fields.
        """
        updated = _service.update_attendee(attendee_id, json_data)
        if not updated:
            abort(404, message="Attendee not found")
        return updated

    @blp.response(204)
    def delete(self, attendee_id: str):
        """
        Delete an attendee, removing from all events.
        """
        ok = _service.delete_attendee(attendee_id)
        if not ok:
            abort(404, message="Attendee not found")
        return ""
