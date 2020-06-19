import sys
from setuptools import setup, find_packages
import djbver


VERSION = djbver.__version__
CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================

Python {}.{} version is not supported, and it requires Python {}.{}.
""".format(*(CURRENT_PYTHON, REQUIRED_PYTHON)))
    sys.exit(1)


def read(f):
    return open(f, 'r', encoding='utf-8').read()


def file(path: str) -> str:
    with open('README.md', encoding='utf-8') as f:
        description = f.read()
    return description


setup(
    name='djbver',
    version=VERSION,
    long_description=file('README.md'),
    long_description_content_type='text/markdown',
    description='djbver',
    license='MIT',
    author='Kwon Jaewon',
    author_email='springkjw@gmail.com',
    url='https://github.com/springkjw/djbver',
    download_url='https://github.com/springkjw/djbver/archive/{version}.tar.gz'.format(version=VERSION),
    install_requires=[
        'django>=3.0',
        'djangorestframework'
    ],
    packages=find_packages(exclude = []),
    keywords=['django', 'djbver', 'rest framework'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Natural Language :: Korean',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)