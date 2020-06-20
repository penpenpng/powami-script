from .test_examples import test as test_examples
from .test_wrong_scripts import test as wrong_scripts

if __name__ == "__main__":
    failed = any([
        test_examples(),
        wrong_scripts(),
    ])

    if failed:
        exit(1)
    else:
        exit(0)
