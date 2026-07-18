"""Serialization compatible with the API's original tastypie wire format.

The JSON output format and the ``meta``/``objects`` list envelope are
compatible with the old django-tastypie implementation, so that existing
API clients keep working.
"""

from __future__ import annotations

import datetime as dt
import json
from typing import TYPE_CHECKING, Any

from django.http import HttpResponse
from django.utils import timezone
from ninja.errors import HttpError

if TYPE_CHECKING:
    from collections.abc import Callable

    from django.db.models import QuerySet
    from django.http import HttpRequest

DEFAULT_LIMIT = 20
MAX_LIMIT = 1000


def format_value(value: Any) -> Any:
    """Convert a value to its JSON-compatible tastypie representation."""
    if isinstance(value, dt.datetime):
        if timezone.is_aware(value):
            value = timezone.make_naive(value)
        return value.isoformat()
    if isinstance(value, dt.date | dt.time):
        return value.isoformat()
    return value


def json_response(data: Any, *, status: int = 200) -> HttpResponse:
    return HttpResponse(
        json.dumps(data, sort_keys=True, ensure_ascii=False),
        content_type="application/json",
        status=status,
    )


def paginated(
    request: HttpRequest,
    queryset: QuerySet,
    serialize: Callable[[Any], dict],
) -> dict:
    """Build the tastypie list envelope: pagination ``meta`` plus ``objects``."""
    limit = _get_paging_param(request, "limit", default=DEFAULT_LIMIT)
    if not limit or limit > MAX_LIMIT:
        limit = MAX_LIMIT
    offset = _get_paging_param(request, "offset", default=0)

    total_count = queryset.count()
    objects = [serialize(obj) for obj in queryset[offset : offset + limit]]

    next_url = None
    if offset + limit < total_count:
        next_url = _page_url(request, limit, offset + limit)
    previous_url = None
    if offset - limit >= 0:
        previous_url = _page_url(request, limit, offset - limit)

    return {
        "meta": {
            "limit": limit,
            "next": next_url,
            "offset": offset,
            "previous": previous_url,
            "total_count": total_count,
        },
        "objects": objects,
    }


def _get_paging_param(request: HttpRequest, name: str, *, default: int) -> int:
    raw = request.GET.get(name, default)
    try:
        value = int(raw)
    except ValueError:
        value = -1
    if value < 0:
        raise HttpError(400, f"Invalid {name} '{raw}', expected a non-negative integer")
    return value


def _page_url(request: HttpRequest, limit: int, offset: int) -> str:
    params = request.GET.copy()
    for param in ("limit", "offset"):
        if param in params:
            del params[param]
    params["limit"] = str(limit)
    params["offset"] = str(offset)
    return f"{request.path}?{params.urlencode()}"
