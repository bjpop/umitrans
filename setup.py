#!/usr/bin/env python

from distutils.core import setup

LONG_DESCRIPTION = \
'''Transfer UMI sequences from a separate FASTQ file to the read IDs
in another FASTQ file.'''


setup(
    name='umitrans',
    version='0.1.0.0',
    author='Bernie Pope',
    author_email='bjpope@unimelb.edu.au',
    packages=['umitrans'],
    package_dir={'umitrans': 'umitrans'},
    entry_points={
        'console_scripts': ['umitrans = umitrans.umitrans:main']
    },
    url='https://github.com/bjpop/umitrans',
    license='LICENSE',
    description=('Transfer UMI sequences between FASTQ files'),
    long_description=(LONG_DESCRIPTION),
    install_requires=['pyfastx'],
)
