# cython: boundscheck=False, wraparound=False, nonecheck=False, language_level=3
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION

import numpy as np
cimport numpy as np
import xxhash
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy, strlen, strcpy, strcat
from cpython.bytes cimport PyBytes_FromStringAndSize
from cpython cimport PyUnicode_AsUTF8
from libc.string cimport strchr

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

# Limpeza de strings acelerada
def clean_string(s):
    cdef str str_s
    if not isinstance(s, str):
        str_s = str(s)
    else:
        str_s = s

    cdef list result = []
    cdef Py_UCS4 c
    for c in str_s:
        if c.isalnum():
            result.append(c.lower())
    return ''.join(result)

def generate_tags(np.ndarray channel_categories, np.ndarray extra_tags_counts, object random_state):
    cdef Py_ssize_t i, j, n
    cdef bytes cat_bytes
    cdef bytearray buffer
    cdef list content_tags = [None] * len(extra_tags_counts)
    cdef object extra_tags
    cdef str category_str

    for i in range(len(extra_tags_counts)):
        n = extra_tags_counts[i]
        category_str = str(channel_categories[i])
        cat_bytes = CACHED_CATEGORY_BYTES[category_str]

        if n == 0:
            content_tags[i] = category_str
            continue

        extra_tags = random_state.choice(list(CACHED_CATEGORY_BYTES.keys()), size=n, replace=False)
        buffer = bytearray()
        buffer.extend(cat_bytes)

        for j in range(n):
            buffer.append(ord(','))
            buffer.extend(CACHED_CATEGORY_BYTES[extra_tags[j]])

        content_tags[i] = buffer.decode('utf-8')

    return content_tags


# Geração de linguagens otimizada
def generate_languages(np.ndarray channel_langs, np.ndarray use_channel_lang, np.ndarray languages, object random_state):
    cdef Py_ssize_t i, n = use_channel_lang.shape[0]
    cdef np.ndarray result = np.empty(n, dtype=object)
    cdef str lang_entry, first_lang
    cdef bytes lang_bytes
    cdef const char* raw_str
    cdef const char* comma_pos

    for i in range(n):
        if use_channel_lang[i]:
            # Converte para string Python pura
            lang_entry = str(channel_langs[i])

            # Armazena o resultado de .encode em variável Python
            lang_bytes = lang_entry.encode('utf-8')
            raw_str = lang_bytes
            comma_pos = strchr(raw_str, ord(','))

            if comma_pos != NULL:
                first_lang = lang_bytes[:comma_pos - raw_str].decode('utf-8')
            else:
                first_lang = lang_entry

            result[i] = first_lang
        else:
            result[i] = random_state.choice(languages)

    return result.astype(str)