"""
Setup.py file.
Install:  "pip install ."
"""

import setuptools

setuptools.setup(
    name="tekkieworden",
    version="0.1",
    description="Workflows and supporting code for Tekkieworden.",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[  # dependencies
        "python-dotenv~=0.13.0",
        "black~=19.3b0",
        "flake8~=3.7.9"
    ],
    python_requires="==3.6.*",
)