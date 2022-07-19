#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pyshp>=2.3',
    'wordcloud>=1.7',
    'numpy>=1.23',
    'matplotlib>=3.5',
    'descartes>=1.1',
    'pandas>=1.0'
]

test_requirements = ['pytest>=3', ]

setup(
    author="Gabriel da Silva Zech",
    author_email='g.inbox@posteo.net',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    description="A package for creating wordcloud maps in Python.",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='wordcloud_mapper',
    name='wordcloud_mapper',
    packages=find_packages(include=['wordcloud_mapper', 'wordcloud_mapper.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/GabZech/wordcloud_mapper',
    version='0.1.0',
    zip_safe=False,
)
