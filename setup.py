from setuptools import setup, find_packages

setup(
    name="jestlang",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
    ],
    entry_points={
        "console_scripts": [
            "jest=cli:CLI.main",
        ],
    },
)
