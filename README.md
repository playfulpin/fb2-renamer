# FB2 Renamer

**Version:** 0.2.0  
**Purpose:** Organize FB2 books from an input ZIP archive into a library structure based on metadata stored in each FictionBook 2 document.

## Requirements

- Python 3.10 or newer
- No third-party Python packages (standard library only)

## Project structure

```text
fb2-renamer/
├── main.py
├── zip_processor.py
├── fb2_parser.py
├── rename_engine.py
├── models.py
├── config.py
├── README.md
├── CHANGELOG.md
├── tests/
│   └── test_fb2_renamer.py
└── temp/
```

## Configuration

Edit `config.py`:

| Setting | Purpose | Default |
|---|---|---|
| `BOOK_ROOT` | Destination library root | `C:\OPDSclient\Books` |
| `TEMP_DIR` | Parent directory for temporary extraction | `<project>/temp` |
| `NAMING_MODE` | Default output mode | `regular_zip` |
| `SKIP_DUPLICATES` | Skip an existing destination rather than overwrite it | `True` |
| `NO_AUTHOR_NAME` | Folder used when author metadata is absent | `Неизвестный автор` |
| `SERIES_NUMBER_WIDTH` | Minimum series-number width | `2` |

The `--book-root` and `--mode` command-line options override the corresponding defaults for one run.

## Usage

```powershell
python main.py path\to\books.zip
python main.py books.zip --mode regular_fb2
python main.py books.zip --mode series_zip --book-root D:\Books
python main.py books.zip --dry-run --verbose
python main.py books.zip --keep-temp
```

The input archive is a required positional argument. Supported modes:

| Mode | Directory layout | Output |
|---|---|---|
| `regular_zip` | `BookRoot\Author\Series\` | `NN - Title.fb2.zip` |
| `regular_fb2` | `BookRoot\Author\Series\` | `NN - Title.fb2` |
| `series_zip` | `BookRoot\Series\` | `NN - Title.fb2.zip` |
| `series_fb2` | `BookRoot\Series\` | `NN - Title.fb2` |

The `NN - ` prefix is omitted when no numeric series position is present. Books with series metadata follow the selected directory layout. **Books without series metadata are always placed directly inside their author directory, regardless of the selected naming mode**; no series placeholder or empty series directory is created. Missing author and title values receive safe fallback names. Multiple authors are joined with `; `.

## Processing behavior

- Finds `.fb2` files recursively inside the supplied ZIP archive, including files in nested folders.
- Reads FB2 metadata as XML; Cyrillic names and titles are preserved as Unicode.
- Writes either a new ZIP containing the FB2 document or a plain FB2 file, according to the selected mode.
- Does not modify or delete the original input archive.
- Skips destination files that already exist when `SKIP_DUPLICATES` is enabled.
- Uses a unique temporary working directory and removes it after processing by default. `--keep-temp` retains extracted files in `temp/`.
- `--dry-run` prints planned destinations without creating output files.
- Rejects ZIP members whose paths attempt to escape the extraction directory.

## Tests

Run the standard-library test suite from the project directory:

```powershell
python -m unittest discover -s tests -v
```

## Exit status

- `0`: processing completed without per-book errors
- `1`: one or more FB2 files could not be processed
- `2`: invalid input or archive-level failure
