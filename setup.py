# -*- coding:utf-8 -*-
import distutils.core
from distutils.core import setup
from Cython.Build import cythonize


setup(ext_modules=cythonize("dzmainui.py"))
distutils.core.setup(
    name='dz',
    version='2.26',
    author='dz'
)
