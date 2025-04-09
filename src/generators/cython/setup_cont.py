from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np
import sys

# Configurações específicas para Windows/MSVC
extra_compile_args = []
if sys.platform == 'win32':
    extra_compile_args = ['/O2', '/GL', '/MD']  # Otimizações para MSVC
else:
    extra_compile_args = ['-O3', '-march=native', '-ffast-math']

extensions = [
    Extension(
        "cy_content_generator",
        ["cy_content_generator.pyx"],
        extra_compile_args=extra_compile_args,
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    )
]

setup(
    ext_modules=cythonize(extensions),
    include_dirs=[np.get_include()],
)