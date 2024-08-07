from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

AUTHOR_NAME = 'SAMBHAV GUPTA'
SRC_REPO = 'src'
LIST_OF_REQUIREMENTS = ['streamlit']

setup(
    name = SRC_REPO,
    version = '0.0.1',
    author = AUTHOR_NAME,
    author_email = 'guptasambhav1207@gmail.com',
    description = 'A Movie Recommendation System',
    long_description = long_description,
    package = [SRC_REPO],
    python_requires = '>=3.7',
    install_requires = LIST_OF_REQUIREMENTS
)