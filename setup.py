"""
Setup configuration for SCEE project.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="scee",
    version="0.1.0",
    author="SCEE Team",
    author_email="dev@scee.com.br",
    description="Sistema de Comércio Eletrônico - E-commerce completo em Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daniele-senko/SCEE",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "black>=23.12.1",
            "pylint>=3.0.3",
            "mypy>=1.7.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "scee=main:main",
        ],
    },
)
