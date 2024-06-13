from setuptools import setup

from pykis import __author__, __author_email__, __license__, __url__, __version__

setup(
    name="python-kis",
    version=__version__,
    description="파이썬 한국투자증권 API",
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    packages=["pykis"],
    include_package_data=True,
    install_requires=[
        "requests>=2.28.1",
        "websocket-client>=1.4.1",
        "pycryptodome>=3.15.0",
        "colorlog>=6.7.0",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/Soju06/python-kis/issues",
        "Documentation": "https://github.com/Soju06/python-kis/wiki/Tutorial",
        "Source Code": "https://github.com/Soju06/python-kis",
    },
)
