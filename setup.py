# -*- coding: utf-8 -*-
"""
    Setup for PyPi
"""

from setuptools import setup

setup(
    name='code',
    version='1.2.1',
    author='zhy',
    author_email='returnzhy1996@outlook.com',
    url='https://github.com/sheepzh/hscode',
    description=u'海关编码查询库',
    packages=['hscode'],
    keywords=['hscode', 'python3', 'ciq'],
    license='MIT',
    install_requires=[
        "requests",
        "beautifulsoup4",
        "lxml"
    ],
    entry_points={
        'console_scripts': [
            'hscode=main:main'
        ]
    },
    zip_safe=True
)
