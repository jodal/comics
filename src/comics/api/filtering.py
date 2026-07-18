"""Query-parameter filtering compatible with the original tastypie behavior.

Unknown parameters are silently ignored, known fields must be whitelisted
for filtering, and lookups are validated against the Django model field's
registered lookups. Error messages match tastypie's exactly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models.constants import LOOKUP_SEP

from comics.api.errors import ApiBadRequest

if TYPE_CHECKING:
    from collections.abc import Mapping

    from django.db.models import Model, QuerySet
    from django.http import QueryDict

# Sentinel allowing all lookup types on a field, like tastypie's ALL.
# Relations are allowed by using a FilterSpec as the filtering value,
# like tastypie's ALL_WITH_RELATIONS.
ALL = "__all__"


@dataclass(frozen=True)
class FilterSpec:
    """What filtering a resource allows."""

    model: type[Model]
    field_names: frozenset[str]
    filtering: Mapping[str, Any] = field(default_factory=dict)


def apply_filters(request_params: QueryDict, queryset: QuerySet, spec: FilterSpec):
    filters = _build_filters(request_params, spec)
    if filters:
        queryset = queryset.filter(**filters)
    return queryset


def _build_filters(params: QueryDict, spec: FilterSpec) -> dict[str, Any]:
    qs_filters = {}

    for filter_expr in params:
        filter_bits = filter_expr.split(LOOKUP_SEP)
        field_name = filter_bits.pop(0)

        if field_name not in spec.field_names:
            # Not a field we know about, e.g. "format" or "subscribed"
            continue

        try:
            model_field = spec.model._meta.get_field(field_name)
        except FieldDoesNotExist:
            msg = f"The '{field_name}' field is not a valid field name"
            raise ApiBadRequest(msg) from None

        filter_type = "exact"
        if filter_bits and filter_bits[-1] in model_field.get_lookups():
            filter_type = filter_bits.pop()

        _check_filtering(spec, field_name, filter_type, filter_bits)

        value = _filter_value_to_python(
            params,
            filter_expr,
            filter_type,
            is_boolean=_is_boolean_field(spec.model, [field_name, *filter_bits]),
        )

        qs_filter = LOOKUP_SEP.join([field_name, *filter_bits, filter_type])
        qs_filters[qs_filter] = value

    return qs_filters


def _check_filtering(
    spec: FilterSpec,
    field_name: str,
    filter_type: str,
    relation_bits: list[str],
) -> None:
    if field_name not in spec.filtering:
        msg = f"The '{field_name}' field does not allow filtering."
        raise ApiBadRequest(msg)

    allowed = spec.filtering[field_name]

    if (
        allowed != ALL
        and not isinstance(allowed, FilterSpec)
        and filter_type not in allowed
    ):
        msg = f"'{filter_type}' is not an allowed filter on the '{field_name}' field."
        raise ApiBadRequest(msg)

    if relation_bits:
        if not isinstance(allowed, FilterSpec):
            if spec.model._meta.get_field(field_name).is_relation:
                msg = (
                    "Lookups are not allowed more than one level deep "
                    f"on the '{field_name}' field."
                )
                raise ApiBadRequest(msg)
            msg = f"The '{field_name}' field does not support relations."
            raise ApiBadRequest(msg)
        _check_filtering(allowed, relation_bits[0], filter_type, relation_bits[1:])


def _is_boolean_field(model: type[Model], field_path: list[str]) -> bool:
    field = None
    for part in field_path:
        field = model._meta.get_field(part)
        if field.is_relation and field.related_model is not None:
            model = field.related_model
    return isinstance(field, models.BooleanField)


def _filter_value_to_python(
    params: QueryDict,
    filter_expr: str,
    filter_type: str,
    *,
    is_boolean: bool,
) -> Any:
    value: Any = params[filter_expr]

    if filter_type == "isnull" or is_boolean:
        if value in ("true", "True"):
            value = True
        elif value in ("false", "False"):
            value = False

    if filter_type in ("in", "range") and isinstance(value, str) and value:
        parts = []
        for part in params.getlist(filter_expr):
            parts.extend(part.split(","))
        value = parts

    return value
