import re
from glob import glob
from pathlib import Path

from .import_package import pws

examples_dir = Path(__file__).parent.parent / "examples"


def create_tests(path: Path):
    with open(path, "r", encoding="utf_8") as f:
        script = f.read()

    doc_comment = re.search(r"/\*(.*)\*/", script, re.S).group(1)
    case_comment = re.match(r"[^i]*(input.*)", doc_comment, re.S).group(1)

    return [
        Test(
            path.name,
            script,
            m.group(1),
            m.group(2),
            m.group(3)
        )
        for m
        in re.finditer(
            r"input ([0-9]+):([^output]*)output \1:([^input]*)",
            case_comment,
            re.S
        )
    ]


class Test:
    exists_failure = False

    def __init__(self, file, script, no, input, output):
        self.file = file
        self.script = pws.sanitize_script(script)
        self.no = no
        self.input = pws.sanitize_input(input)
        self.output = pws.sanitize_input(output)

    def do(self):
        try:
            result = pws.run_script(self.script, self.input)
            assert result == self.output
        except AssertionError:
            Test.exists_failure = True
            print(f"""
[FAILED] case {self.no} in {self.file} (Assertion Error)
expected: {self.output}
actual  : {result}
            """)
        except pws.PwsSyntaxError as e:
            Test.exists_failure = True
            print(
                f"[FAILED] case {self.no} in {self.file} (Syntax Error: {e})")
        except Exception:
            Test.exists_failure = True
            print(f"[FAILED] case {self.no} in {self.file} (Unknown Error)")
        else:
            print(f"[passed] case {self.no} in {self.file}")


def test():
    Test.exists_failure = False

    for example in map(Path, glob(str(examples_dir / "*"))):
        for test in create_tests(example):
            test.do()

    return Test.exists_failure
