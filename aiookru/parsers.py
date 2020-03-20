import html.parser
from collections import defaultdict


class AuthDialogParser(html.parser.HTMLParser):
    """Authorization dialog parser."""

    @property
    def form(self):
        return self.url, self.inputs

    __slots__ = ('url', 'inputs')

    def __init__(self):
        super().__init__()
        self.inputs = {}
        self.url = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            attrs = defaultdict(str, attrs)
            if attrs['type'].lower() != 'submit':
                self.inputs[attrs['name']] = attrs['value']
        elif tag == 'form':
            attrs = defaultdict(str, attrs)
            if attrs['method'].lower() == 'post':
                self.url = attrs['action']


class AccessDialogParser(html.parser.HTMLParser):
    """Access dialog parser."""

    @property
    def form(self):
        return self.url, self.inputs

    __slots__ = ('url', 'inputs')

    def __init__(self):
        super().__init__()
        self.inputs = {}
        self.url = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            attrs = defaultdict(str, attrs)
            if attrs['type'].lower() != 'submit':
                self.inputs[attrs['name']] = attrs['value']
        elif tag == 'form':
            attrs = defaultdict(str, attrs)
            if attrs['method'].lower() == 'post':
                self.url = attrs['action']
