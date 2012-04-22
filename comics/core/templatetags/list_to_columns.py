"""Splits query results list into multiple sublists for template display."""

from django.template import Library, Node, TemplateSyntaxError

register = Library()


class SplitListNode(Node):
    def __init__(self, results, cols, new_results):
        self.results, self.cols, self.new_results = results, cols, new_results

    def split_seq(self, results, cols=2):
        start = 0
        results = list(results)
        for i in xrange(cols):
            stop = start + len(results[i::cols])
            yield results[start:stop]
            start = stop

    def render(self, context):
        context[self.new_results] = self.split_seq(
            context[self.results], int(self.cols))
        return ''


def list_to_columns(parser, token):
    """Parse template tag: {% list_to_columns results as new_results 2 %}"""
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError("list_to_columns results as new_results 2")
    if bits[2] != 'as':
        raise TemplateSyntaxError("second argument to the list_to_columns "
            "tag must be 'as'")
    return SplitListNode(bits[1], bits[4], bits[3])


list_to_columns = register.tag(list_to_columns)
