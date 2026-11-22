from pathlib import Path
from zipfile import ZipFile

def unpack_archive(zip_path: Path, destination: Path) -> None:
    with ZipFile(zip_path, 'r') as zf:
        zf.extractall(destination)

def find_fb2_files(folder: Path):
    yield from folder.rglob('*.fb2')
