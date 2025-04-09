# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: nonecheck=False
# cython: initializedcheck=False

import numpy as np
cimport numpy as np
import xxhash
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy, strlen, strcpy, strcat
from cpython.bytes cimport PyBytes_FromStringAndSize
from cpython cimport PyUnicode_AsUTF8
from libc.string cimport strchr
from cython.parallel cimport prange
from cpython.unicode cimport PyUnicode_FromStringAndSize
from cpython.list cimport PyList_Append

# Cache global (em nível de módulo)
cdef dict CACHED_CATEGORY_BYTES = {}

# Tipos para arrays numpy
ctypedef np.int32_t INT32_t
ctypedef np.int64_t INT64_t

def initialize_cached_categories(np.ndarray categories):
    global CACHED_CATEGORY_BYTES
    CACHED_CATEGORY_BYTES = {str(cat): str(cat).encode('utf-8') for cat in categories}

# Função Base62 ultra-rápida
cdef char* _base62_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def to_base62_fast(long val):
    cdef char result[64]
    cdef int i = 0
    cdef int base = 62
    
    if val == 0:
        return "0"
    
    while val > 0 and i < 63:
        result[i] = _base62_chars[val % base]
        val = val // base
        i += 1
    
    result[i] = 0  # Null terminator
    
    # Inverter a string
    cdef int start = 0
    cdef int end = i - 1
    cdef char temp
    while start < end:
        temp = result[start]
        result[start] = result[end]
        result[end] = temp
        start += 1
        end -= 1
    
    return result.decode('utf-8')

# Função de hash otimizada
def fast_hash(s):
    if not isinstance(s, str):
        s = str(s)
    return xxhash.xxh64(s).hexdigest()[:12]

# Geração de linguagens otimizada
def generate_languages_nogil(
    np.ndarray[np.uint8_t, ndim=1] use_channel_lang,
    object channel_langs,       # array of bytes
    object fallback_langs       # array of bytes
):
    cdef Py_ssize_t i, n = use_channel_lang.shape[0]
    cdef np.ndarray result = np.empty(n, dtype=object)
    cdef char** chan_ptrs = <char**>malloc(n * sizeof(char*))
    cdef char** fallback_ptrs = <char**>malloc(n * sizeof(char*))

    # Prepara ponteiros em Python-safe GIL zone
    for i in range(n):
        chan_ptrs[i] = <char*> (<bytes>channel_langs[i])
        fallback_ptrs[i] = <char*> (<bytes>fallback_langs[i])

    cdef const char* raw
    cdef const char* comma
    cdef Py_ssize_t length

    # Processa paralelo, sem acesso a Python
    with nogil:
        for i in prange(n):
            if use_channel_lang[i]:
                raw = chan_ptrs[i]
                comma = strchr(raw, ord(','))
                length = comma - raw if comma != NULL else strlen(raw)

                with gil:
                    result[i] = PyUnicode_FromStringAndSize(raw, length)
            else:
                with gil:
                    result[i] = PyUnicode_FromStringAndSize(fallback_ptrs[i], strlen(fallback_ptrs[i]))

    free(chan_ptrs)
    free(fallback_ptrs)

    return result

def generate_tags_fast(np.ndarray[object] content_categories,
                       np.ndarray[object] extra_tags):
    cdef Py_ssize_t i, n = content_categories.shape[0]
    cdef object tags, c1, c2, c3
    cdef list result = []

    for i in range(n):
        c1 = content_categories[i]
        c2 = extra_tags[2*i]
        c3 = extra_tags[2*i+1]

        tags = []
        # Adiciona sem duplicatas
        if c1 != c2 and c1 != c3:
            tags.append(c1)
        if c2 != c3:
            tags.append(c2)
        tags.append(c3)  # sempre adiciona o terceiro (pelo menos 1 garantido)

        result.append(tags)  # pode ser trocado por acima, se quiser mais controle

    return result

def generate_content_tags(np.ndarray[np.int32_t] content_ids, list tag_lists):
    cdef list result = []
    cdef Py_ssize_t i, j, n = len(tag_lists)
    cdef object tag, cid
    for i in range(n):
        cid = content_ids[i]
        for tag in tag_lists[i]:
            result.append((tag, cid))
    return result