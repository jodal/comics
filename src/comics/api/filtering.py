"""Query-parameter filtering compatible with the original tastypie behavior.

Unknown parameters are silently ignored, known fields must be whitelisted
for filtering, and lookups are validated against the Django model field's
registered lookups.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from ninja.errors import HttpError

if TYPE_CHECKING:
    from collections.abc import Mapping

    from django.db.models import Model, QuerySet
    from django.http import QueryDict

    # The value a query parameter is turned into before being passed to
    # QuerySet.filter().
    FilterValue = str | bool | list[str]

# Sentinel allowing all lookup types on a field, like tastypie's ALL.
# Relations are allowed by using a FilterSpec as the filtering value,
# like tastypie's ALL_WITH_RELATIONS.
ALL = "__all__"

# What filtering a field allows: the ALL sentinel, a set of allowed
# lookups, or a FilterSpec for filtering across a relation.
type FilterRule = str | frozenset[str] | FilterSpec


def _no_filtering() -> dict[str, FilterRule]:
    return {}


@dataclass(frozen=True)
class FilterSpec:
    """What filtering a resource allows."""

    model: type[Model]
    field_names: frozenset[str]
    filtering: Mapping[str, FilterRule] = field(default_factory=_no_filtering)


def apply_filters[M: Model](
    request_params: QueryDict,
    queryset: QuerySet[M],
    spec: FilterSpec,
) -> QuerySet[M]:
    filters = _build_filters(request_params, spec)
    if filters:
        queryset = queryset.filter(**filters)
    return queryset


def _build_filters(params: QueryDict, spec: FilterSpec) -> dict[str, FilterValue]:
    qs_filters: dict[str, FilterValue] = {}

    for filter_expr in params:
        filter_bits = filter_expr.split(LOOKUP_SEP)
        field_name = filter_bits.pop(0)

        if field_name not in spec.field_names:
            # Not a field we know about, e.g. "format" or "subscribed"
            continue

        try:
            model_field = spec.model._meta.get_field(field_name)
        except FieldDoesNotExist:
            raise HttpError(400, f"Invalid filter '{filter_expr}'") from None

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
        raise HttpError(400, f"Filtering on '{field_name}' is not allowed")

    allowed = spec.filtering[field_name]

    if (
        allowed != ALL
        and not isinstance(allowed, FilterSpec)
        and filter_type not in allowed
    ):
        raise HttpError(
            400, f"Filtering on '{field_name}' with '{filter_type}' is not allowed"
        )

    if relation_bits:
        if not isinstance(allowed, FilterSpec):
            raise HttpError(
                400, f"Filtering on '{field_name}' across relations is not allowed"
            )
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
) -> FilterValue:
    raw = params[filter_expr]
    value: FilterValue = raw if isinstance(raw, str) else [str(part) for part in raw]

    if filter_type == "isnull" or is_boolean:
        if value in ("true", "True"):
            value = True
        elif value in ("false", "False"):
            value = False

    if filter_type in ("in", "range") and isinstance(value, str) and value:
        parts: list[str] = []
        for part in params.getlist(filter_expr):
            parts.extend(part.split(","))
        value = parts

    return value
