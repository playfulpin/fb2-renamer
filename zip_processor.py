from pathlib import Path
from zipfile import ZipFile


def is_fb2_zip(path: Path) -> bool:
    return path.name.lower().endswith('.fb2.zip')


def extract_fb2_from_zip(path: Path) -> bytes:
    with ZipFile(path) as zf:
        fb2_files = [n for n in zf.namelist() if n.lower().endswith('.fb2')]
        if not fb2_files:
            raise FileNotFoundError('No .fb2 file found inside archive')
        return zf.read(fb2_files[0])
