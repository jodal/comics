"""Splits query results list into multiple sublists for template display."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.template import Library, Node, TemplateSyntaxError

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from django.template import Context
    from django.template.base import Parser, Token

register = Library()


class SplitListNode(Node):
    def __init__(self, results: str, cols: str, new_results: str) -> None:
        self.results, self.cols, self.new_results = results, cols, new_results

    def split_seq(
        self,
        results: Iterable[object],
        cols: int = 2,
    ) -> Iterator[list[object]]:
        start = 0
        items = list(results)
        for i in range(cols):
            stop = start + len(items[i::cols])
            yield items[start:stop]
            start = stop

    def render(self, context: Context) -> str:
        context[self.new_results] = self.split_seq(
            context[self.results], int(self.cols)
        )
        return ""


@register.tag
def list_to_columns(parser: Parser, token: Token) -> SplitListNode:
    """Parse template tag: {% list_to_columns results as new_results 2 %}"""
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError("list_to_columns results as new_results 2")
    if bits[2] != "as":
        raise TemplateSyntaxError(
            "second argument to the list_to_columns tag must be 'as'"
        )
    return SplitListNode(bits[1], bits[4], bits[3])
