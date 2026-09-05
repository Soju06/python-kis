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
    # ruff는 target-version 기준으로 죽은 코드로 보지만, 소스에서 직접 실행하는
    # 3.9 사용자에게 명확한 메시지를 주기 위한 가드다.
    if sys.version_info < (3, 10):  # noqa: UP036
        raise RuntimeError("Python 3.10 이상이 필요합니다.")

    test_main()
