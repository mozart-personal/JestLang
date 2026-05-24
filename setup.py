from setuptools import setup

setup(
    name="jestlang",
    version="0.0.1",
    py_modules=["main"],
    install_requires=[
        "flask"
    ],
    entry_points={
        "console_scripts": [
            "jest=main:main"
        ]
    }
)
