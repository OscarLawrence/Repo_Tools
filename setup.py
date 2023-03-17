from setuptools import setup, find_packages

from Tools.setup_utils import get_readme

setup(
    name="Tools",
    version="0.0.1",
    description='Tools and Utilities for Python',
    long_description=get_readme(),
    author='Vincent Schmitt',
    author_email='vindao@outlook.com',
    url=None,
    download_url='',
    keywords=[],
    packages=find_packages(),
    install_requires=[],
)
