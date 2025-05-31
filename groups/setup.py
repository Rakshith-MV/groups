# data_processor/setup.py
from setuptools import setup, find_packages

setup(
    name="groups",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "networkx>=2.5",
        "flask>=2.0.0",
        "flask-cors>=3.0.10"
    ],
    author="Rakshith V",
    author_email="werakshith@gmail.com",
    description="A package for algebraic groups",
    keywords="math, algebra",
)