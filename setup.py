import setuptools

setuptools.setup(
    name="pyalamut",
    version="0.0.1",
    author="Sam Nalty",
    author_email="sam.nalty@nhs.net",
    description="A package for parsing Alamut mut files",
    url="https://github.com/snalty/pyalamut",
    project_urls={
        "Bug Tracker": "https://github.com/snalty/pyalamut"
    },
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">3.5",
)