from setuptools import setup

VERSION = "0.0.1"

setup(
    name="xword_converter",
    description="A crossword utility written in Python that converts between the different formats available to distribute them.",
    author="obrhubr",
    url="https://github.com/obrhubr/xword-converter",
    license="MIT",
    version=VERSION,
    install_requires=[
        "argparse"
    ],
    python_requires=">=3.8"
)