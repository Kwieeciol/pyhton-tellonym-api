import setuptools

with open("README.md", "r") as fh:
    desc = fh.read()

setuptools.setup(
    name="tellonym", # Replace with your own username
    version="1.0.0",
    author="PatchByte",
    author_email="sorrynoemail@email.com",
    description="A Python tellonym api",
    long_description=desc,
    long_description_content_type="text/markdown",
    url="https://github.com/PatchByte/pyhton-tellonym-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
