import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='pyformlang',
    version='0.1.9',
    #scripts=['pyformlang'] ,
    author="Julien Romero",
    author_email="romerojulien34@gmail.com",
    description="A python framework for formal grammars",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aunsiels/pyformlang",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
