#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pymecab',
    version='2.0.0',
    description='mecab wrapper by using natto-py',
    author='JX PRESS Corp.',
    author_email='info@jxpress.net',
    url='https://github.com/jxpress/pymecab',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(), 
    include_package_data=True,
    keywords=['natural language processing', 'morphological analyzer', 'mecab'],
    license='MIT License',
    install_requires=[
        'natto-py'
    ],
    extras_require={
        'test': ['pytest']
    },
    entry_points={
        'console_scripts': [
            'pymecab.console=pymecab.console:main'
        ]
    }
)
