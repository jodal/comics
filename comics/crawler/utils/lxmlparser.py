#encoding: utf-8

from lxml.html import parse, fromstring

class LxmlParser(object):
    def __init__(self, url=None, string=None):
        if url:
            self.root = parse(url).getroot()
            self.root.make_links_absolute(url)
        elif string:
            self.root = fromstring(string)

    def text(self, selector):
        return self.select(selector).text_content()

    def src(self, selector):
        return self.select(selector).get('src')

    def alt(self, selector):
        return self.select(selector).get('alt')

    def title(self, selector):
        return self.select(selector).get('title')

    def remove(self, selector):
        for element in self.root.cssselect(selector):
            element.drop_tree()

    def select(self, selector):
        elements = self.root.cssselect(selector)

        if len(elements) == 0:
            raise DoesNotExist('Noting matched the selector: %s' % selector)
        elif len(elements) > 1:
            raise MultipleElementsReturned('Selector matched %d elements: %s' %
                (len(elements), selector))

        return elements[0]

class DoesNotExist(Exception):
    pass

class MultipleElementsReturned(Exception):
    pass
