#include "../include/aligned_alocator.h"
#include "../include/random_utils.h"
#include <unordered_set>
#include <vector>
#include <omp.h>
#include <immintrin.h>
#include <type_traits>
#include <iostream>
#include <math.h>
#include <bitset>
#include <random>
#include "pcg_random.hpp"

namespace RandomUtils {
    inline __m256i splitmix64_avx2(__m256i idx) {
        // Constantes do splitmix64
        __m256i multiplier = _mm256_set1_epi64x(6364136223846793005ULL); // multiplicador
        __m256i increment = _mm256_set1_epi64x(1); // incremento
    
        // Calculando splitmix64 para 4 valores de 64 bits simultaneamente
        __m256i state = idx;  // Carrega o índice
    
        state = _mm256_add_epi64(state, increment);  // state += 1
        state = _mm256_mul_epu32(state, multiplier); // state = state * 6364136223846793005ULL
        state = _mm256_srli_epi64(state, 32);        // shift right (projetado para 64 bits)
        
        return state;
    }

    
    void remove_duplicates_inplace(std::vector<int64_t, AlignedAllocator<int64_t, 32>>& inputVector) {
        std::unordered_set<int64_t> seenIds;
    
        for (size_t i = 0; i < inputVector.size(); ++i) {
            // Enquanto o valor for repetido, coloca -1 (ou gere novo valor se preferir)
            if (seenIds.find(inputVector[i]) != seenIds.end()) {
                inputVector[i] = -1;
            }
            else {
            seenIds.insert(inputVector[i]);
        }
        }
    }

    std::vector<int64_t, AlignedAllocator<int64_t, 32>> shuffle_with_splitmix64(
        const std::vector<int64_t, AlignedAllocator<int64_t, 32>>& inputVector, size_t n) {
            size_t actual_range = n - (n % 4);
            std::vector<int64_t, AlignedAllocator<int64_t, 32>> outputVector(actual_range);
            
            omp_set_num_threads(omp_get_max_threads());
            #pragma omp parallel for schedule(static)
            for (size_t i = 0; i <actual_range; i += 4) {
            // Carrega os índices de forma alinhada
            _mm_prefetch(reinterpret_cast<const char*>(&inputVector[i + 32]), _MM_HINT_T0);  // Prefetch
            __m256i idx = _mm256_load_si256(reinterpret_cast<const __m256i*>(&inputVector[i]));
            // Aplica o SplitMix64 vetorizado
            __m256i result = splitmix64_avx2(idx);  // aplica o splitmix64 em 4 valores
            // Mapeia para o intervalo [0, n)
            result = _mm256_and_si256(result, _mm256_set1_epi64x(n - 1)); // % n

            // Armazena os resultados no vetor de saída de forma alinhada
            _mm256_store_si256(reinterpret_cast<__m256i*>(&outputVector[i]), result);
            }
            remove_duplicates_inplace(outputVector);

            return outputVector;
        }


    // Função de getBit para qualquer alocador
    template <typename Allocator>
    inline bool getBit(const std::vector<uint8_t, Allocator>& bits, int n) {
        return bits[n >> 3] & (1 << (n & 7));
    }

    // Função de clearBit para qualquer alocador
    template <typename Allocator>
    inline void clearBit(std::vector<uint8_t, Allocator>& bits, int n) {
        bits[n >> 3] &= ~(1 << (n & 7));
    }

    // Função de setBit para qualquer alocador
    template <typename Allocator>
    inline void setBit(std::vector<uint8_t, Allocator>& bits, int n) {
        bits[n >> 3] |= (1 << (n & 7));
    }

    std::vector<int32_t, AlignedAllocator<int32_t, 32>> fastSieve(int32_t range) {
        int32_t adjustedRange = range + (30 - range % 30);

        // Bitmap: 1 bit por número
        std::vector<uint8_t, AlignedAllocator<uint8_t, 32>> isPrime((adjustedRange + 7) / 8, 0);

        // Definir a roda de 30 (máscara de resíduos primos)
        // Índices representam os resíduos (0 a 29) mod 30
        // Os números primos menores que 30: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
        const std::vector<int> wheelPattern = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29};
        
        // Inicializa os números da roda de 30 no vetor `isPrime`
        #pragma omp parallel for schedule(static)
        for (int i = 0; i < adjustedRange; i += 30) {
            for (int j : wheelPattern) {
                setBit(isPrime, i + j);
            }
        }

        // Set bits manualmente para 2, 3, 5
        setBit(isPrime, 2);
        setBit(isPrime, 3);
        setBit(isPrime, 5);

        std::vector<int32_t, AlignedAllocator<int32_t, 32>> primes;
        primes.reserve(adjustedRange / 4);
        primes.push_back(2);
        primes.push_back(3);
        primes.push_back(5);

        int32_t limit = static_cast<int32_t>(std::sqrt(adjustedRange));

        // Crivo com múltiplos apenas nos resíduos válidos
        #pragma omp parallel for schedule(dynamic)
        for (int p = 7; p <= limit; ++p) {
            if (!getBit(isPrime, p)) continue;
            primes.push_back(p);

            // Marca múltiplos de p
            #pragma omp parallel for schedule(static)
            for (int64_t mult = int64_t(p) * p; mult < adjustedRange; mult += p * 2) {
                clearBit(isPrime, static_cast<int>(mult));
            }
        }

        // Adiciona os números restantes que são primos
        for (int i = limit + 1; i < range; ++i) {
            if (getBit(isPrime, i)) {
                primes.push_back(i);
            }
        }

        return primes;
    }

    int64_t computeCoprime(int64_t number) {
        std::vector<int32_t, AlignedAllocator<int32_t, 32>> primes = fastSieve(static_cast<int32_t>(std::sqrt(number)));
        std::vector<int64_t, AlignedAllocator<int64_t, 32>> local_products(omp_get_max_threads(), 1);

        #pragma omp parallel
        {
            int tid = omp_get_thread_num();
            int64_t& product = local_products[tid];

            #pragma omp for schedule(static)
            for (size_t i = 0; i < primes.size(); ++i) {
                if (number % primes[i] == 0) {
                    product *= primes[i];
                }
            }
        }

        // Produto final dos produtos parciais
        int64_t total_product = 1;
        for (const auto& p : local_products) {
            total_product *= p;
        }

        return total_product + 1;
    }

    void shuffleLinspace(std::vector<int64_t, AlignedAllocator<int64_t, 32>>& linspace, int64_t numberOfElements){
        size_t size = linspace.size();
        int64_t coprime = computeCoprime(size);
        std::random_device rd;
        pcg64_fast rng(rd());
        std::uniform_int_distribution<int64_t> bDist(0, size);
        int64_t b = bDist(rng);
        #pragma omp parallel for schedule(static)
        for (size_t i = 0; i < numberOfElements; ++i) {
        linspace[i] = (i * coprime + b) % size;
        }
    }

    float sampleBeta (float alpha, float beta, pcg64_fast& rng){
        std::gamma_distribution<float> dist_alpha(alpha, 1.0f);
        std::gamma_distribution<float> dist_beta(beta, 1.0f);
        float x = dist_alpha(rng);
        float y = dist_beta(rng);
        return x / (x + y);
    }

}