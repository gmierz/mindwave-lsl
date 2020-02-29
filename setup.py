"""
Sets up the CLI and modules for `mindwave-lsl`.
"""
from setuptools import setup

setup(
    name = "mindwavelsl",
    version = "1.0",
    author = "Gregory Mierzwinski",
    author_email = "gmierz1@live.ca",
    description = ("A package to send Mindwave Mobile 2 data over Lab Streaming "
                   "Layer (LSL)."),
    license = "GPLv3",
    keywords = "mindwave lab streaming layer lsl",
    url = "https://github.com/gmierz/mindwave-lsl",
    packages=[
        'mindwavelsl',
    ],
    long_description="See this page: https://github.com/gmierz/mindwave-lsl \n"
                     "After installation, run with `mindwavelsl`.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=[
        'pylsl',
        'numpy'
    ],
    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    mindwavelsl = mindwavelsl.mindwavelsl:main
    """,
)