#!/usr/bin/env python

"""
setup.py  to build conjecture code with cython
To build, run in cmd: python setup.py build_ext --inplace
Or simply call: cython conjecture.py
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'conjecture',
  ext_modules = cythonize("conjecture.py"),
)