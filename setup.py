import os
import version
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='qbuild-jupyter',
    version=version.__version__,
    description='A convert system for our jupyter challenges',
    long_description=README,
    author='Peyman Najafi',
    author_email="peynajber@gmail.com",
    url='https://github.com/peynaj/qbuild-jupyter.git',
    packages=find_packages(),
    include_package_data=True,
    scripts=[],
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
)