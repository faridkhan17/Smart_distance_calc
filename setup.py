from distutils.core import setup
from glob import glob

from setuptools import find_packages

setup(name='algorithm',
      version='1.0',
      description='Python Distribution Utilities',
      author='farid khan',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
     )