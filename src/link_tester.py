import argparse
import re
import sys

from helpers import retrieve_url


def parse_args():
    parser = argparse.ArgumentParser(
        description="Test URL retrieval with different output modes."
    )
    parser.add_argument("url", help="Input URL to test")
    return parser.parse_args()


def main():
    args = parse_args()
    url = args.url

    try:
        print(re.sub(r"\s+", " ", retrieve_url(url)).strip())
    except Exception as exc:
        print(f"Error while processing URL: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
