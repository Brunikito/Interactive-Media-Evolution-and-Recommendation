#pragma once
#include "../include/aligned_alocator.h"
#include <immintrin.h>
#include <type_traits>

namespace RandomUtils {
    inline __m256i splitmix64_avx2(__m256i idx);
    void remove_duplicates_inplace(std::vector<int64_t, AlignedAllocator<int64_t, 32>>& inputVector);
    std::vector<int64_t, AlignedAllocator<int64_t, 32>> shuffle_with_splitmix64(
        const std::vector<int64_t, AlignedAllocator<int64_t, 32>>& inputVector, size_t n);
    // Função de getBit para qualquer alocador
    template <typename Allocator>
    inline bool getBit(const std::vector<uint8_t, Allocator>& bits, int n);
    // Função de clearBit para qualquer alocador
    template <typename Allocator>
    inline void clearBit(std::vector<uint8_t, Allocator>& bits, int n);
    // Função de setBit para qualquer alocador
    template <typename Allocator>
    inline void setBit(std::vector<uint8_t, Allocator>& bits, int n);

    std::vector<int32_t, AlignedAllocator<int32_t, 32>> fastSieve(int32_t range);
    int64_t computeCoprime(int64_t number);
    void shuffleLinspace(std::vector<int64_t, AlignedAllocator<int64_t, 32>>& linspace, int64_t numberOfElements);

}