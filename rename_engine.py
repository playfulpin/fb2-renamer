from pathlib import Path
from models import BookMetadata


def build_filename(metadata: BookMetadata, template: str) -> str:
    values = {
        'author': metadata.safe_author,
        'title': metadata.safe_title,
        'series': metadata.series or '',
        'seq': metadata.sequence or '',
        'lang': metadata.language or '',
    }
    return template.format(**values).strip()


def rename_file(source: Path, metadata: BookMetadata, template: str, force: bool = False, dry_run: bool = True) -> Path:
    target = source.with_name(build_filename(metadata, template) + source.suffix)
    if not dry_run:
        if target.exists() and not force:
            raise FileExistsError(target)
        source.rename(target)
    return target
