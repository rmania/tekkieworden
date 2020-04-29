"""
Setup.py file.
Install:  "pip install ."
"""
import os
import io
from pathlib import Path
from setuptools import find_packages, setup

# Package meta-data.
NAME = 'tekkieworden'
DESCRIPTION = 'Project to analyse the gap in tech talent in the Netherlands'
URL = 'https://github.com/rmania/tekkieworden'
EMAIL = 'd.meijerink@braxwell.com'
AUTHOR = 'Diederik Meijerink'
REQUIRES_PYTHON = '>=3.6.0'

# Packages that are required for this module to be executed
def list_reqs(fname='requirements.txt'):
    with open(fname) as fd:
        return fd.read().splitlines()


here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
ROOT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = ROOT_DIR / 'src/tekkieworden'
about = {}
with open(PACKAGE_DIR / 'VERSION') as f:
    _version = f.read().strip()
    about['__version__'] = _version

setup(
    name=NAME,
    version="about['__version__']",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    packages=find_packages(),
    package_data={'tekkieworden': ['VERSION']},
    package_dir={"": "src"},
    install_requires=list_reqs(),
    extras_require={},
    include_package_data=True,
    license='BSD 3',
    python_requires="==3.6.*",
)