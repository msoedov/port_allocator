import sys
from allocator import process


def main():
    process(sys.argv[1] if len(sys.argv) > 1 else 'data.yml')


if __name__ == "__main__":
    main()
