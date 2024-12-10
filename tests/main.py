import sys
import unittest
from pathlib import Path


def test_main() -> None:
    sys.path.append(str(Path(__file__).parent.parent))

    loader = unittest.TestLoader()
    suite = loader.discover("tests/unit")

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        raise RuntimeError("Python 3.10 이상이 필요합니다.")

    test_main()
