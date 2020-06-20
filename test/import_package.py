import sys
from pathlib import Path


def import_pws():
    import pws
    return pws


sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)
pws = import_pws()
