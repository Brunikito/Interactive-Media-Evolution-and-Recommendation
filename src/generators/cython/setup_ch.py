from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name="cy_channel_generator",
    ext_modules=cythonize("cy_channel_generator.pyx", language_level=3),
    include_dirs=[numpy.get_include()]
)