# Changelog

All notable changes to this project are documented here.

## [0.2.1] - 2026-11-23

### Changed
- Books without series metadata no longer use a placeholder directory; the series directory is omitted entirely.
- Removed the obsolete `NO_SERIES_NAME` configuration setting.

## [0.2.0] - 2026-11-23

### Added
- Command-line options for naming mode, output root, dry-run, temporary-file retention, and verbose logging.
- Safe ZIP extraction with protection against path traversal.
- Recursive, case-insensitive FB2 discovery.
- FB2 metadata parsing for multiple authors, title, series, and series number.
- Windows-safe filename sanitization and fallback names for missing metadata.
- Four output modes: regular/series directory layouts, each as zipped or unzipped FB2.
- Standard-library unit tests.

### Changed
- Temporary extraction now uses a unique per-run directory.
- Source archive is retained; extracted FB2 files are copied into the destination rather than moved.
- Documentation now describes configuration, command-line usage, naming modes, and processing behavior.

### Fixed
- ZIP path traversal vulnerability in archive extraction.
- Handling of invalid XML, missing metadata, and non-numeric series positions.
- Existing destination files are not overwritten by default.

## [0.1.0] - Initial prototype

- Initial ZIP extraction, FB2 metadata parsing, and metadata-based output organization.
