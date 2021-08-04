"""A package to monitor science job feeds and tweet new limnology jobs"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="limnojobs",
    version="0.0.1",
    author="Jemma Stachelek",
    author_email="stachel2@msu.edu",
    description="A package to monitor science job feeds and tweet new \
                limnology jobs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jsta/limnojobs",
    scripts=["bin/limnojobs"],
    include_package_data=True,
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
