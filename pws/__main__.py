from .engine import Env
from .yacc import parse

import sys
import re


def run_script(script: str, arg: str = ""):
    script = re.sub(r"[^ぽわ！？～ーっ]", "", script)
    arg = re.sub(r"[^ぽわ！？～ー]", "", arg)

    code = parse(script)

    return Env.run(code, arg)


def run_script_file(path, arg=""):
    with open(path, "r", encoding="utf_8") as f:
        return run_script(f.read(), arg)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(run_script_file(sys.argv[1]))
    if len(sys.argv) >= 3:
        print(run_script_file(sys.argv[1], sys.argv[2]))
