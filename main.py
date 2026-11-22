import argparse
import shutil
from pathlib import Path
from config import TEMP_DIR
from zip_processor import unpack_archive, find_fb2_files
from fb2_parser import parse_fb2
from rename_engine import store_book

def prepare_temp():
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('archive')
    args=parser.parse_args()
    archive=Path(args.archive)
    prepare_temp()
    unpack_archive(archive, TEMP_DIR)
    count=0
    for fb2 in find_fb2_files(TEMP_DIR):
        try:
            store_book(fb2, parse_fb2(fb2))
            count+=1
        except Exception as ex:
            print(f'ERROR: {fb2}
{ex}')
    print(f'Processed: {count}')
    shutil.rmtree(TEMP_DIR, ignore_errors=True)

if __name__ == '__main__':
    main()
