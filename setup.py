from distutils.core import setup
from setuptools import find_packages

setup(
    name='packerlicious',
    version='0.2.0',
    author='Matthew Aynalem',
    author_email='maynalem@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/mayn/packerlicious',
    license='Apache License 2.0',
    description='',
    install_requires=[
        "future",
    ],
)
