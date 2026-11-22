import xml.etree.ElementTree as ET
from models import BookInfo

def _text(node):
    return node.text.strip() if node is not None and node.text else ''

def parse_fb2(fb2_file) -> BookInfo:
    tree = ET.parse(fb2_file)
    root = tree.getroot()
    ns = {'fb':'http://www.gribuser.ru/xml/fictionbook/2.0'}
    title = _text(root.find('.//fb:book-title', ns))
    author_node = root.find('.//fb:author', ns)
    first_name = last_name = ''
    if author_node is not None:
        first_name = _text(author_node.find('fb:first-name', ns))
        last_name = _text(author_node.find('fb:last-name', ns))
    author = f'{last_name} {first_name}'.strip()
    sequence = root.find('.//fb:sequence', ns)
    series = None
    number = None
    if sequence is not None:
        series = sequence.attrib.get('name')
        try:
            number = int(sequence.attrib.get('number'))
        except Exception:
            pass
    return BookInfo(title=title, author=author, series=series, series_number=number)
