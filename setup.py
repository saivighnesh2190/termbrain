from setuptools import setup, find_packages

setup(
    name="termbrain",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "rich",
        "ollama",
    ],
    entry_points={
        "console_scripts": [
            "termbrain=termbrain.main:app",
        ],
    },
)
