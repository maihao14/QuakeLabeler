import setuptools
import os.path
from os import listdir
import re
from numpy.distutils.core import setup
from pathlib import Path


def find_version(*paths):
    fname = os.path.join(os.path.dirname(__file__), *paths)
    with open(fname) as fp:
        code = fp.read()
    match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", code, re.M)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string.")


# scripts = [str(x) for x in Path('Scripts').iterdir() if x.is_file()]

setup(
    name='seiscreator',
    version=find_version('seiscreator', '__init__.py'),
    description='Seismic Phase Label Creator',
    author='Hao Mai',
    author_email='hmai090@uottawa.ca',
    maintainer='Hao Mai',
    maintainer_email='hmai090@uottawa.ca',
    url='https://github.com/maihao14/SeisLabelCreator',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'],
    install_requires=['numpy', 'obspy', 'scipy'],
    python_requires='>=3.7',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['examples/*']},
    #    scripts=scripts)
    entry_points={
        'console_scripts':
        ['SeisCreator=seiscreator.scripts.SeisCreator:main',
         'requests_isc=seiscreator.scripts.requests_isc:main']})
