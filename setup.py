import codecs
import re
from setuptools import setup
from setuptools import find_packages

__version__ = re.findall('__version__ = "(.*)"',
                         open('cd_drive/__init__.py').read())[0]

REQUIREMENTS = codecs.open('requirements.txt', 'r', 'utf8').read().split('\n')[:-1]

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
