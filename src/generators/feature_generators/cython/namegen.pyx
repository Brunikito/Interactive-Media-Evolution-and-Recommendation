# namegen.pyx
import numpy as np
cimport numpy as np
from libc.stdlib cimport rand, srand, RAND_MAX
from cython cimport boundscheck, wraparound

@boundscheck(False)
@wraparound(False)
def generate_indices(int n, int n_adjectives, int n_nouns,
                     np.ndarray[np.int32_t, ndim=1] suffixes_lengths,
                     np.ndarray[np.int32_t, ndim=1] category_indices):
    cdef np.ndarray[np.int32_t, ndim=1] adjective_ids = np.random.randint(0, n_adjectives, size=n)
    cdef np.ndarray[np.int32_t, ndim=1] noun_ids = np.random.randint(0, n_nouns, size=n)
    cdef np.ndarray[np.int32_t, ndim=1] suffix_ids = np.empty(n, dtype=np.int32)

    cdef int i, suffix_len
    for i in range(n):
        suffix_len = suffixes_lengths[category_indices[i]]
        suffix_ids[i] = rand() % suffix_len

    return adjective_ids, noun_ids, suffix_ids