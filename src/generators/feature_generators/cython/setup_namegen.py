# setup.py
from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name="channel_name_generator",
    ext_modules=cythonize("namegen.pyx", language_level=3),
    include_dirs=[numpy.get_include()],
)