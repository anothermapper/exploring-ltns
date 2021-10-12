import sys
from pathlib import Path

if "src" not in sys.path[1][-3:]:
    _src = str(Path(sys.path[0]).joinpath("src"))
    sys.path.insert(1, _src)
