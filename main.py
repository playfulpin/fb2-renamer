import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='fb2-renamer')

    sub = parser.add_subparsers(dest='command', required=True)

    info = sub.add_parser('info')
    info.add_argument('file')

    scan = sub.add_parser('scan')
    scan.add_argument('path')
    scan.add_argument('-r', '--recursive', action='store_true')
    scan.add_argument('-v', '--verbose', action='store_true')
    scan.add_argument('--template')

    rename = sub.add_parser('rename')
    rename.add_argument('path')
    rename.add_argument('-r', '--recursive', action='store_true')
    rename.add_argument('-v', '--verbose', action='store_true')
    rename.add_argument('--template')
    rename.add_argument('--force', action='store_true')

    return parser


if __name__ == '__main__':
    args = build_parser().parse_args()
    print(args)
