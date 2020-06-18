import sys

from yacc import run


def from_file(path, arg=""):
    with open(path, "r", encoding="utf_8") as f:
        return run(f.read(), arg)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(from_file(sys.argv[1]))
    if len(sys.argv) >= 3:
        print(from_file(sys.argv[1], sys.argv[2]))
