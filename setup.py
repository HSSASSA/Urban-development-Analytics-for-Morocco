"""
Setup script for package distribution
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="urban-development-analytics",
    version="1.0.0",
    author="Urban Analytics Team",
    description="End-to-end data engineering and analysis for urban development policy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0",
        "numpy>=1.24",
        "scipy>=1.11",
        "scikit-learn>=1.3",
        "plotly>=5.17",
        "dash>=2.14",
        "sqlalchemy>=2.0",
        "pytest>=7.4",
        "pyyaml>=6.0",
    ],
)
