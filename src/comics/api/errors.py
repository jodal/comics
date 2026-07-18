"""API exceptions, rendered as tastypie-style ``{"error": ...}`` responses."""


class ApiBadRequest(Exception):
    """The request is invalid; the message is returned in the 400 response."""
