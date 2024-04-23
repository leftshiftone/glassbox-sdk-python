import os
# read the contents of your README file
from pathlib import Path

import pkg_resources
from setuptools import find_packages, setup

long_description = Path(__file__).with_name("README.md").read_text()

version = "0.1.0"

setup(
    name='glassbox-sdk',
    packages=find_packages(exclude=["tests.*"]),
    version=version,
    license='Apache Software License',
    description='The sdk for the glassbox service',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='leftshiftone',
    author_email='github@leftshift.one',
    url='https://github.com/leftshiftone/glassbox-sdk-python',
    download_url=f'https://github.com/leftshiftone/glassbox-sdk-python/archive/refs/tags/v{version}.tar.gz',
    keywords=['machine-learning', 'artificial-intelligence', 'explainable-ai'],
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
