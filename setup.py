#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pymecab',
    version='1.0.1',
    description='mecab wrapper by using natto-py',
    author='JX PRESS Corp.',
    author_email='info@jxpress.net',
    url='https://github.com/jxpress/pymecab',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(), 
    include_package_data=True,
    keywords=['natural language processing', 'morphological analyzer', 'mecab'],
    license='MIT License',
    install_requires=[
        'natto-py'
    ]
)
