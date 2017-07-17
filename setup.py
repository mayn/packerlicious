from distutils.core import setup
from setuptools import find_packages

setup(
    name='packerlicious',
    version='0.1.0dev',
    author='Matthew Aynalem',
    author_email='maynalem@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/mayn/packerlicious',
    license='Apache License 2.0',
    description='',
    long_description=open('README.md').read(),
    install_requires=[
    ],
)
