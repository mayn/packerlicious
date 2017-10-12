"""
Copyright 2017 Matthew Aynalem

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from distutils.core import setup
from setuptools import find_packages

# opening and reading the file version.py
vop = open("src/packerlicious/version.py","r")


setup(
    name='packerlicious',
    version=vop,
    author='Matthew Aynalem',
    author_email='maynalem@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/mayn/packerlicious',
    license='Apache License 2.0',
    description='packerlicious - a python wrapper for packer templates.',
    long_description=open('README.rst').read(),
    install_requires=[
        "future",
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License'
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
