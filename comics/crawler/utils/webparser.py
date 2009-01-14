from sgmllib import SGMLParser
import urllib

class WebParser(SGMLParser):
    _allowed_tags = ('div', 'p')

    def reset(self):
        """Resets parser"""

        SGMLParser.reset(self)
        self.response = None
        self.charset = None
        self._tagstack = []
        self.tags = []
        self.imgs = []

    def _contenttype_to_charset(self, contenttype):
        """Extracts charset from content-types"""

        for part in contenttype.split(';'):
            if part.strip().lower().startswith('charset='):
                return part.split('=')[-1].strip()
        return None

    def unknown_starttag(self, tag, attrs):
        """Handles unknown starttags"""

        if not tag in self._allowed_tags:
            return
        D = {}
        D['tag'] = tag
        for key, value in attrs:
            D[key] = value
        self._tagstack.append(D)

    def unknown_endtag(self, tag):
        """Handles unknown endtags"""

        if not tag in self._allowed_tags:
            return
        if not len(self._tagstack):
            return
        D = self._tagstack.pop()
        # Strip whitespace from data field, and delete it if empty
        if D.has_key('data'):
            if len(D['data']):
                D['data'] = [i.strip() for i in D['data']]
                D['data'] = ' '.join(D['data'])
                D['data'] = D['data'].strip()
            if not len(D['data']):
                del D['data']
        self.tags.append(D)

    def handle_data(self, text):
        """Handles data outside tags"""

        if len(self._tagstack):
            if not self._tagstack[-1].has_key('data'):
                self._tagstack[-1]['data'] = []
            self._tagstack[-1]['data'].append(text)

    def start_img(self, attrs):
        """Handles img tags"""

        img = {}
        for key, value in attrs:
            img[key] = value
        self.imgs.append(img)

    def start_meta(self, attrs):
        """Extract content-type from meta tags"""

        meta = {}
        for key, value in attrs:
            meta[key] = value
        if (meta.has_key('http-equiv')
            and meta['http-equiv'].lower() == 'content-type'
            and meta.has_key('content')):
            charset = self._contenttype_to_charset(meta['content'])
            if charset:
                # Charset in meta tags override charset in HTTP headers
                self.charset = charset

    def parse_url(self, url):
        """Parses content at URL"""

        self.reset()
        usock = urllib.urlopen(url)
        self.response = usock.info()

        # Get charset from HTTP headers
        self.charset = self._contenttype_to_charset(self.response.typeheader)
        if not self.charset and self.response.maintype == 'text':
            # Use HTTP default charset for text/*
            self.charset = 'iso-8859-1'

        self.feed(usock.read())
        usock.close()
        self.close()
