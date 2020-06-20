import re
from glob import glob
from pathlib import Path

from .import_package import pws

runtime_error_dir = Path(__file__).parent / "runtime_error_case"
syntax_error_dir = Path(__file__).parent / "syntax_error_case"


def create_tests(path: Path, expect):
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
            expect
        )
        for m
        in re.finditer(
            r"input ([0-9]+):([^input]*)",
            case_comment,
            re.S
        )
    ]


class Result:
    SYNTAX_ERROR = "Syntax Error"
    RUNTIME_ERROR = "Runtime Error"
    UNKNOWN_ERROR = "Unknown Error"
    SUCCESS = "Success"


class Test:
    exists_failure = False

    def __init__(self, file, script, no, input, expect):
        self.file = file
        self.script = pws.sanitize_script(script)
        self.no = no
        self.input = pws.sanitize_input(input)
        self.expect = expect

    def do(self):
        try:
            result = pws.run_script(self.script, self.input)
        except pws.PwsSyntaxError:
            actual = Result.SYNTAX_ERROR
        except Exception:
            actual = Result.UNKNOWN_ERROR
        else:
            if result == pws.ERROR_MESSAGE:
                actual = Result.RUNTIME_ERROR
            else:
                actual = Result.SUCCESS

        if actual != Result.SUCCESS:
            result = ""
        else:
            result = f"({result})"

        if actual == self.expect:
            print(f"[passed] case {self.no} in {self.file}")
        else:
            Test.exists_failure = True
            print(f"""
[FAILED] case {self.no} in {self.file}
expected: {self.expect}
actual  : {actual} {result}
            """)


def test():
    Test.exists_failure = False

    for file in map(Path, glob(str(syntax_error_dir / "*"))):
        for test in create_tests(file, Result.SYNTAX_ERROR):
            test.do()

    for file in map(Path, glob(str(runtime_error_dir / "*"))):
        for test in create_tests(file, Result.RUNTIME_ERROR):
            test.do()

    return Test.exists_failure
