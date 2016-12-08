import sys
from allocator import process


def main():
    process(sys.argv[1] if len(sys.argv) > 1 else 'data.yml',
            host=sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
            )


if __name__ == "__main__":
    main()
