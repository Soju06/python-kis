from setuptools import setup

from pykis import __author__, __author_email__, __license__, __url__, __version__


def main():
    with open("README.md", "r") as f:
        long_description = f.read()

    with open("requirements.txt", "r") as f:
        requirements = [line for line in f.read().splitlines() if line]

    setup(
        name="python-kis",
        version=__version__,
        description="파이썬 한국투자증권 REST 기반 Trading API 라이브러리",
        long_description=long_description,
        author=__author__,
        author_email=__author_email__,
        url=__url__,
        license=__license__,
        packages=["pykis"],
        include_package_data=True,
        install_requires=requirements,
        project_urls={
            "Bug Tracker": "https://github.com/Soju06/python-kis/issues",
            "Documentation": "https://github.com/Soju06/python-kis/wiki/Tutorial",
            "Source Code": "https://github.com/Soju06/python-kis",
        },
    )


if __name__ == "__main__":
    main()
