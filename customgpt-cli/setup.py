from setuptools import setup, find_packages

setup(
    name="customgpt-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "customgpt-client>=1.1.6",
        "tabulate>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "customgpt-cli=customgpt_cli.cli:main",
        ],
    },
)
