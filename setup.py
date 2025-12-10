"""Setup configuration for fycus"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fycus",
    version="0.1.0",
    author="Joshua Melander",
    description="Easy scientific figure generation with matplotlib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jbmelander/fycus",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.7",
    install_requires=[
        "matplotlib>=3.0.0",
        "pyyaml>=5.1",
    ],
    entry_points={
        'console_scripts': [
            'fycus=fycus.cli:main',
        ],
    },
)
