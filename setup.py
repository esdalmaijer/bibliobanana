import bibliobanana
import setuptools

example_image = \
"""Example:

![Graph illustrating the yearly number of papers referencing "banana" and "farts" on PubMed](farts_1964-2020.png)

*Occurence of the word "fart" versus the word "banana" in PubMed-indexed 
articles between 1964 and 2020*
"""

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
    # Remove the example image.
    long_description = long_description.replace(example_image, "")

# Stupid bug in twine ignores long_description_content_type, so just refer
# people to GitHub.
long_description = "A bug in twine prevents reading Markdown files, so please read the README at https://github.com/esdalmaijer/bibliobanana"

setuptools.setup(
    name="bibliobanana",
    version=bibliobanana.__version__,
    author="Edwin Dalmaijer",
    author_email="edwin.dalmaijer@mrc-cbu.cam.ac.uk",
    description="Python package to quantify and normalise yearly publication rates for specific keywords on PubMed and Google Scholar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/esdalmaijer/bibliobanana",
    packages=["bibliobanana"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
    ],
)
