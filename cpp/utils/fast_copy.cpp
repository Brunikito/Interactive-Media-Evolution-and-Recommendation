#include "../include/aligned_alocator.h"
#include <vector>
#include <omp.h>
#include <immintrin.h>
#include <type_traits>
#include <cstdint>

namespace FastCopy {

template <typename T, std::size_t Alignment = 32>
std::vector<T, AlignedAllocator<T, Alignment>> copyAlignedVector(const std::vector<T, AlignedAllocator<T, Alignment>>& inputVector) {
    size_t size = inputVector.size();
    std::vector<T, AlignedAllocator<T, Alignment>> outputVector(size);
    if (size == 0) {
        return outputVector;
    }

    constexpr size_t simdWidth = sizeof(__m256i);               // 32 bytes
    constexpr size_t elementsPerSimd = simdWidth / sizeof(T);   // quantos T cabem em 32 bytes

    static_assert(Alignment >= alignof(T), "Alignment must be at least alignof(T)");

    omp_set_num_threads(omp_get_max_threads());
    if constexpr (std::is_same_v<T, int64_t>) {
        // Se for int64_t (que sabemos que funciona com AVX2)
        size_t simdRange = size - (size % elementsPerSimd);

        #pragma omp parallel
        {
            #pragma omp for schedule(static)
            for (int i = 0; i < simdRange; i += elementsPerSimd) {
                _mm_prefetch(reinterpret_cast<const char*>(&inputVector[i + 32]), _MM_HINT_T0);  // Prefetch
                __m256i copySubset = _mm256_load_si256(reinterpret_cast<const __m256i*>(&inputVector[i]));
                _mm256_store_si256(reinterpret_cast<__m256i*>(&outputVector[i]), copySubset);
            }
            #pragma omp for schedule(static)
            for (int i = simdRange; i < size; i++) {
                outputVector[i] = inputVector[i];
            }
        }
    } else {
        #pragma omp parallel for schedule(static)
        for (size_t i = 0; i < size; ++i) {
            outputVector[i] = inputVector[i];
        }
    }

    return outputVector;
}

}