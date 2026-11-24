from dataclasses import dataclass


@dataclass(slots=True)
class BookMetadata:
    title: str | None = None
    author: str | None = None
    series: str | None = None
    sequence: str | None = None
    language: str | None = None

    @property
    def safe_author(self) -> str:
        return self.author or "UNKNOWN_AUTHOR"

    @property
    def safe_title(self) -> str:
        return self.title or "UNKNOWN_TITLE"
