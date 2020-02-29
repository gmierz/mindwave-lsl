"""
Sets up the CLI and modules for `mindwave-lsl`.
"""
import os
from setuptools import setup

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "mindwavelsl",
    version = "1.1.0",
    author = "Gregory Mierzwinski",
    author_email = "gmierz1@live.ca",
    description = ("A package to send Mindwave EEG data over Lab Streaming "
                   "Layer (LSL)."),
    license = "GPLv3",
    keywords = "mindwave lab streaming layer lsl",
    url = "https://github.com/gmierz/mindwave-lsl",
    packages=[
        'mindwavelsl',
        'mindwavelsl.vendor'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=[
        'numpy',
        'pylsl',
        'pyserial'
    ],
    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    mindwavelsl = mindwavelsl.mindwavelsl:main
    """,
)