from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension
import numpy

ext_modules = [
    Extension(
        "fast_concat",
        sources=["fast_concat.pyx"],
        include_dirs=[numpy.get_include()],
        extra_compile_args=["-O3", "-march=native", "-ffast-math", "/openmp"],
        extra_link_args=['/fopenmp'],
    )
]

setup(
    name='fast-concat-parallel',
    ext_modules=cythonize(ext_modules, language_level="3"),
)