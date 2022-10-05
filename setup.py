from setuptools import setup

setup(
    name='python-kis',
    version='1.0.0',
    description='파이썬 한국투자증권 API',
    author='soju06',
    author_email='qlskssk@gmail.com',
    url='https://github.com/soju06/python-kis',
    license='MIT',
    packages=['pykis'],
    include_package_data=True,
    install_requires=[
        'requests>=2.28.1',
        'SQLAlchemy>=1.4.39',
        'websocket-client>=1.4.1',
        'pycryptodome>=3.15.0',
        'colorlog>=6.7.0'
    ],
)