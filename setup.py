#!/usr/bin/env python
"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.readlines()


setup(
    name="yemeksepeti_api",
    version="0.0.1",
    description="Yemeksepeti unofficial API.",
    python_requires=">=3.6",
    author="Mahir Tüzel",
    author_email="e4c6@dataso.me",
    license="GNU General Public License v3.0",
    url="https://github.com/e4c6/yemeksepeti_api",
    install_requires=[requirements],
    long_description=readme,
    packages=find_packages(
        include=[
            "yemeksepeti_api",
        ]
    ),
    zip_safe=False,
)
