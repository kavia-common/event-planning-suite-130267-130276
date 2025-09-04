"""
Marshmallow schemas for request/response validation.
"""
from marshmallow import Schema, fields, validate


class PaginationSchema(Schema):
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    per_page = fields.Int(missing=50, validate=validate.Range(min=1, max=1000))


class AttendeeCreateSchema(Schema):
    name = fields.Str(required=True, description="Full name of the attendee")
    email = fields.Email(required=True, description="Email address of the attendee")


class AttendeeUpdateSchema(Schema):
    name = fields.Str(required=False)
    email = fields.Email(required=False)


class AttendeeSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.Str()
    updated_at = fields.Str()


class EventCreateSchema(Schema):
    title = fields.Str(required=True, description="Title of the event")
    description = fields.Str(required=False, allow_none=True)
    start_time = fields.Str(required=False, allow_none=True, description="ISO 8601")
    end_time = fields.Str(required=False, allow_none=True, description="ISO 8601")
    location = fields.Str(required=False, allow_none=True)
    attendee_ids = fields.List(fields.Str(), required=False)


class EventUpdateSchema(Schema):
    title = fields.Str(required=False)
    description = fields.Str(required=False, allow_none=True)
    start_time = fields.Str(required=False, allow_none=True)
    end_time = fields.Str(required=False, allow_none=True)
    location = fields.Str(required=False, allow_none=True)
    attendee_ids = fields.List(fields.Str(), required=False)


class EventSchema(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    start_time = fields.Str(allow_none=True)
    end_time = fields.Str(allow_none=True)
    location = fields.Str()
    attendee_ids = fields.List(fields.Str())
    created_at = fields.Str()
    updated_at = fields.Str()


class EventWithAttendeesSchema(EventSchema):
    attendees = fields.List(fields.Nested(AttendeeSchema))
