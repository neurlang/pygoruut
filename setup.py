from setuptools import setup, find_packages

setup(
    name="pygoruut",
    version="0.7.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Neurlang Project",
    author_email="77860779+neurlang@users.noreply.github.com",
    description="Text-to-IPA converter and phonetic translator for Python, powered by the Goruut phonemization engine",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/neurlang/pygoruut",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

