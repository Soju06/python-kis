import importlib.metadata as metadata
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

    try:
        requires = metadata.distribution(pykis.__package_name__).requires

        if not requires:
            print("No Dependencies")
        else:
            print()

            for package in requires:
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

    except metadata.PackageNotFoundError:
        print("Package Not Found")
        return

    print("=" * 32)

    print()


if __name__ == "__main__":
    check()
