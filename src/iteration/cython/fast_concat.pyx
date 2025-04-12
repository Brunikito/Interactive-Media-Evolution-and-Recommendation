# distutils: language = c++
# cython: boundscheck=False
# cython: wraparound=False
# cython: nonecheck=False
# cython: cdivision=True

import numpy as np
cimport numpy as cnp
from cython.parallel import parallel, prange
from libc.string cimport memcpy
cimport cython
from cpython cimport PyObject
import pandas as pd

ctypedef fused float_arr_32_t:
   cnp.float32_t[:]
   cnp.float32_t[::1]

cdef concat_float32_impl(
    float_arr_32_t arr1,
    float_arr_32_t arr2
):
    cdef Py_ssize_t n1 = arr1.shape[0]
    cdef Py_ssize_t n2 = arr2.shape[0]
    cdef Py_ssize_t total = n1 + n2

    out = np.empty(total, dtype=np.float32)
    cdef cnp.float32_t[::1] out_view = out
    cdef Py_ssize_t i

    with nogil:
        for i in prange(n1, schedule='static'):
            out_view[i] = arr1[i]
        for i in prange(n2, schedule='static'):
            out_view[n1 + i] = arr2[i]

    return out

def concat_float32(arr1, arr2):
    if arr1.data.contiguous and arr2.data.contiguous:
        return concat_float32_impl[cnp.float32_t[::1]](arr1, arr2)
    else:
        return concat_float32_impl[cnp.float32_t[:]](arr1, arr2)

ctypedef fused float_arr_64_t:
    cnp.float64_t[:]
    cnp.float64_t[::1]

cdef concat_float64_impl(
        float_arr_64_t arr1,
        float_arr_64_t arr2
):
        cdef Py_ssize_t n1 = arr1.shape[0]
        cdef Py_ssize_t n2 = arr2.shape[0]
        cdef Py_ssize_t total = n1 + n2

        out = np.empty(total, dtype=np.float64)
        cdef cnp.float64_t[::1] out_view = out
        cdef Py_ssize_t i

        with nogil:
            for i in prange(n1, schedule='static'):
                out_view[i] = arr1[i]
            for i in prange(n2, schedule='static'):
                out_view[n1 + i] = arr2[i]

        return out

def concat_float64(arr1, arr2):
        if arr1.data.contiguous and arr2.data.contiguous:
            return concat_float64_impl[cnp.float64_t[::1]](arr1, arr2)
        else:
            return concat_float64_impl[cnp.float64_t[:]](arr1, arr2)

ctypedef fused int_arr_8_t:
    cnp.int8_t[:]
    cnp.int8_t[::1]

cdef concat_int8_impl(
    int_arr_8_t arr1,
    int_arr_8_t arr2
):
    cdef Py_ssize_t n1 = arr1.shape[0]
    cdef Py_ssize_t n2 = arr2.shape[0]
    cdef Py_ssize_t total = n1 + n2

    out = np.empty(total, dtype=np.int8)
    cdef cnp.int8_t[::1] out_view = out
    cdef Py_ssize_t i

    with nogil:
        for i in prange(n1, schedule='static'):
            out_view[i] = arr1[i]
        for i in prange(n2, schedule='static'):
            out_view[n1 + i] = arr2[i]

    return out

def concat_int8(arr1, arr2):
    if arr1.data.contiguous and arr2.data.contiguous:
        return concat_int8_impl[cnp.int8_t[::1]](arr1, arr2)
    else:
        return concat_int8_impl[cnp.int8_t[:]](arr1, arr2)

ctypedef fused int_arr_16_t:
    cnp.int16_t[:]
    cnp.int16_t[::1]

cdef concat_int16_impl(
    int_arr_16_t arr1,
    int_arr_16_t arr2
):
    cdef Py_ssize_t n1 = arr1.shape[0]
    cdef Py_ssize_t n2 = arr2.shape[0]
    cdef Py_ssize_t total = n1 + n2

    out = np.empty(total, dtype=np.int16)
    cdef cnp.int16_t[::1] out_view = out
    cdef Py_ssize_t i

    with nogil:
        for i in prange(n1, schedule='static'):
            out_view[i] = arr1[i]
        for i in prange(n2, schedule='static'):
            out_view[n1 + i] = arr2[i]

    return out

def concat_int16(arr1, arr2):
    if arr1.data.contiguous and arr2.data.contiguous:
        return concat_int16_impl[cnp.int16_t[::1]](arr1, arr2)
    else:
        return concat_int16_impl[cnp.int16_t[:]](arr1, arr2)

ctypedef fused int_arr_32_t:
    cnp.int32_t[:]
    cnp.int32_t[::1]

cdef concat_int32_impl(
    int_arr_32_t arr1,
    int_arr_32_t arr2
):
    cdef Py_ssize_t n1 = arr1.shape[0]
    cdef Py_ssize_t n2 = arr2.shape[0]
    cdef Py_ssize_t total = n1 + n2

    out = np.empty(total, dtype=np.int32)
    cdef cnp.int32_t[::1] out_view = out
    cdef Py_ssize_t i

    with nogil:
        for i in prange(n1, schedule='static'):
            out_view[i] = arr1[i]
        for i in prange(n2, schedule='static'):
            out_view[n1 + i] = arr2[i]

    return out

def concat_int32(arr1, arr2):
    if arr1.data.contiguous and arr2.data.contiguous:
        return concat_int32_impl[cnp.int32_t[::1]](arr1, arr2)
    else:
        return concat_int32_impl[cnp.int32_t[:]](arr1, arr2)

ctypedef fused int_arr_64_t:
    cnp.int64_t[:]
    cnp.int64_t[::1]

cdef concat_int64_impl(
    int_arr_64_t arr1,
    int_arr_64_t arr2
):
    cdef Py_ssize_t n1 = arr1.shape[0]
    cdef Py_ssize_t n2 = arr2.shape[0]
    cdef Py_ssize_t total = n1 + n2

    out = np.empty(total, dtype=np.int64)
    cdef cnp.int64_t[::1] out_view = out
    cdef Py_ssize_t i

    with nogil:
        for i in prange(n1, schedule='static'):
            out_view[i] = arr1[i]
        for i in prange(n2, schedule='static'):
            out_view[n1 + i] = arr2[i]

    return out

def concat_int64(arr1, arr2):
    if arr1.data.contiguous and arr2.data.contiguous:
        return concat_int64_impl[cnp.int64_t[::1]](arr1, arr2)
    else:
        return concat_int64_impl[cnp.int64_t[:]](arr1, arr2)

