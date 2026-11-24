"""
Title:        FB2 metadata parser
Script Name:  fb2_parser.py
Description:  Read book metadata from FictionBook 2 XML documents.
Project:      fb2-renamer
Author:       mp
Date:         2026-11-23
Version:      0.2.0
"""

import xml.etree.ElementTree as ET
from pathlib import Path

from models import BookInfo

FB2_NAMESPACE = "http://www.gribuser.ru/xml/fictionbook/2.0"
NS = {"fb": FB2_NAMESPACE}


def _text(node: ET.Element | None) -> str:
    """Return normalized text for an optional XML element."""
    if node is None:
        return ""
    return " ".join("".join(node.itertext()).split())


def parse_fb2(fb2_file: Path) -> BookInfo:
    """Parse title, all author names, and the first sequence declaration."""
    try:
        root = ET.parse(fb2_file).getroot()
    except ET.ParseError as exc:
        raise ValueError(f"Invalid FB2 XML: {exc}") from exc

    title = _text(root.find(".//fb:description/fb:title-info/fb:book-title", NS))
    author_names = []
    for author_node in root.findall(".//fb:description/fb:title-info/fb:author", NS):
        first = _text(author_node.find("fb:first-name", NS))
        middle = _text(author_node.find("fb:middle-name", NS))
        last = _text(author_node.find("fb:last-name", NS))
        nickname = _text(author_node.find("fb:nickname", NS))
        name = " ".join(part for part in (last, first, middle) if part).strip() or nickname
        if name and name not in author_names:
            author_names.append(name)

    sequence = root.find(".//fb:description/fb:title-info/fb:sequence", NS)
    series = sequence.attrib.get("name", "").strip() if sequence is not None else ""
    number = None
    if sequence is not None:
        raw_number = sequence.attrib.get("number", "").strip()
        try:
            number = int(raw_number) if raw_number else None
        except ValueError:
            number = None

    return BookInfo(
        title=title,
        author="; ".join(author_names),
        series=series or None,
        series_number=number,
    )
