import platform
from pathlib import Path

import pykis


def check():
    uname = platform.uname()

    print(f"Version: PyKis/{pykis.__version__}")
    print(f"Python: {platform.python_implementation()} {platform.python_version()}")
    print(f"System: {uname.system} {uname.version} [{uname.machine}]")
    print()
    print("Installed Packages:", end=" ")

    requirements = Path(__file__).parents[2].joinpath("requirements.txt")

    if requirements.exists():
        try:
            import importlib.metadata as metadata

            print()

            for package in requirements.read_text().splitlines():
                package, version = package.rsplit("=", 1)
                package, operator = package[:-1], package[-1]
                l = (30 - len(package)) // 2
                r = 30 - len(package) - l

                print(
                    f"{'=' * l} {package} {'=' * r}\nRequired: {version}{operator}=\nInstalled: ",
                    end="",
                )

                try:
                    print(metadata.version(package))
                except metadata.PackageNotFoundError:
                    print("Not Found")

            print("=" * 32)
        except ImportError:
            print("importlib-metadata not found")
            return
    else:
        print("requirements.txt not found")

    print()


if __name__ == "__main__":
    check()
