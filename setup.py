import codecs
import re
from setuptools import setup
from setuptools import find_packages
from pip._internal.req import parse_requirements

__version__ = re.findall('__version__ = "(.*)"',
                         open('cd_drive/__init__.py').read())[0]

INSTALL_REQS = parse_requirements('requirements.txt', session='hack')
REQUIREMENTS = [str(ir.req) for ir in INSTALL_REQS]

print(REQUIREMENTS)

setup(
    name='cd_drive',
    version=__version__,
    description='Wrapper to easily manipulate Google Drive files',
    url='https://github.com/matheusbsilva/cd_drive',
    long_description=codecs.open('README.md', 'rb', 'utf8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=REQUIREMENTS
)
