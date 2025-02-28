import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="expiring-dict",
    version="1.1.2",
    author="David Parker",
    description="Python dict with TTL support for auto-expiring caches",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dparker2/py-expiring-dict",
    packages=setuptools.find_packages(),
    install_requires=["sortedcontainers"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
