from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

root = Path('site').resolve()
void = set('area base br col embed hr img input link meta param source track wbr'.split())

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.stack, self.links, self.ids = path, [], [], set()

    def handle_starttag(self, tag, attrs):
        assert len(dict(attrs)) == len(attrs), f'{self.path}: duplicate attribute'
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'{self.path}: duplicate id'
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])
        if tag not in void:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        assert self.stack and self.stack.pop() == tag, f'{self.path}: unbalanced {tag}'

for path in sorted(root.rglob('*.html')):
    page = Page(path)
    page.feed(path.read_text())
    assert not page.stack, f'{path}: unclosed tags'
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            assert url.scheme in ('https', 'mailto'), f'{path}: unsafe link'
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        assert target.is_relative_to(root), f'{path}: link leaves site'
        if target.is_dir():
            target /= 'index.html'
        assert target.is_file(), f'{path}: broken local link {link}'
        if url.fragment and target == path:
            assert url.fragment in page.ids, f'{path}: missing anchor'
    print(f'Valid HTML and local links: {path.relative_to(root)}')
