import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def read_requirements():
    with open("WHL_requirements.txt") as f:
        return [line.replace("\n", "") for line in f.readlines()]


setuptools.setup(
    name="MordinezNLP",
    version=os.environ['PACKAGEVERSION'],
    install_requires=read_requirements(),
    author='Marcin Borzymowski',
    description='Powerfull python tool for modern NLP processing',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BMarcin/MordinezNLP",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    keywords="NLP text preprocessing cleaning tool",
    license='MIT',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.6'
)
