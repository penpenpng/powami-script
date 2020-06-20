from .engine import Env
from .yacc import parse

import sys
import re


def sanitize_input(arg):
    arg = re.sub(r"〜", "～", arg)
    return re.sub(r"[^ぽわ！？～ー]", "", arg)


def sanitize_script(script):
    script = re.sub(r"〜", "～", script)
    script = re.sub(r"/\*[^/]*\*/", "", script, re.S)
    return re.sub(r"[^ぽわ！？～ーっ]", "", script)


def run_script(
    script: str,
    arg: str = "",
    max_step: int = 100000,
    var_capacity: int = 1024
):
    arg = sanitize_input(arg)
    script = sanitize_script(script)
    code = parse(script)

    return Env.run(code, arg, max_step, var_capacity)


def run_script_file(
    path,
    arg: str = "",
    max_step: int = 100000,
    var_capacity: int = 1024
):
    with open(path, "r", encoding="utf_8") as f:
        return run_script(f.read(), arg, max_step, var_capacity)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(run_script_file(sys.argv[1]))
    if len(sys.argv) >= 3:
        print(run_script_file(sys.argv[1], sys.argv[2]))
