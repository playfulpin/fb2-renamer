from pathlib import Path
from xml.etree import ElementTree as ET

from models import BookMetadata
from zip_processor import is_fb2_zip, extract_fb2_from_zip


def _strip(tag: str) -> str:
    return tag.split('}', 1)[-1]


def _find_first(root, name: str):
    for elem in root.iter():
        if _strip(elem.tag) == name:
            return elem
    return None


def parse_fb2(path: Path) -> BookMetadata:
    if is_fb2_zip(path):
        xml_data = extract_fb2_from_zip(path)
        root = ET.fromstring(xml_data)
    else:
        root = ET.parse(path).getroot()

    title = None
    title_elem = _find_first(root, 'book-title')
    if title_elem is not None and title_elem.text:
        title = title_elem.text.strip()

    language = None
    lang_elem = _find_first(root, 'lang')
    if lang_elem is not None and lang_elem.text:
        language = lang_elem.text.strip()

    author = None
    author_elem = _find_first(root, 'author')
    if author_elem is not None:
        parts = []
        for tag in ('first-name', 'middle-name', 'last-name', 'nickname'):
            elem = next((e for e in author_elem.iter() if _strip(e.tag) == tag and e.text), None)
            if elem is not None:
                parts.append(elem.text.strip())
        if parts:
            author = ' '.join(parts)

    series = None
    sequence = None
    seq_elem = _find_first(root, 'sequence')
    if seq_elem is not None:
        series = seq_elem.attrib.get('name')
        sequence = seq_elem.attrib.get('number')

    return BookMetadata(
        title=title,
        author=author,
        series=series,
        sequence=sequence,
        language=language,
    )
