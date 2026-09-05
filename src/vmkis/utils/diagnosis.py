import importlib.metadata as metadata
import platform

# 루트 파사드(`import vmkis`)가 아니라 `vmkis.__env__` 를 봅니다.
# `vmkis/__init__.py` 는 kis/api/client/scope 를 전부 끌고 오므로, 그것을 import
# 하면 utils 가 패키지 전체에 의존하게 됩니다(ARCHITECTURE.md 불변식 2번).
# 필요한 값 두 개는 원래 `__env__` 에 있고 루트는 그것을 재export할 뿐입니다.
from vmkis import __env__


def check():
    uname = platform.uname()

    print(f"Version: VmKis/{__env__.__version__}")
    print(f"Python: {platform.python_implementation()} {platform.python_version()}")
    print(f"System: {uname.system} {uname.version} [{uname.machine}]")
    print()
    print("Installed Packages:", end=" ")

    try:
        requires = metadata.distribution(__env__.__package_name__).requires

        if not requires:
            print("No Dependencies")
        else:
            print()

            for package in requires:
                package, version = package.rsplit("=", 1)
                package, operator = package[:-1], package[-1]
                left = (30 - len(package)) // 2
                right = 30 - len(package) - left

                print(
                    f"{'=' * left} {package} {'=' * right}\nRequired: {version}{operator}=\nInstalled: ",
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
