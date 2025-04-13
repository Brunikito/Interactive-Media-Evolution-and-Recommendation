#pragma once
#include <malloc.h>     // para _aligned_malloc e _aligned_free no Windows
#include <new>
#include <cstddef>
#include <stdexcept>

template <typename T, std::size_t Alignment = 32>
struct AlignedAllocator {
    using value_type = T;

    AlignedAllocator() noexcept = default;

    template <typename U>
    AlignedAllocator(const AlignedAllocator<U, Alignment>&) noexcept {}

    T* allocate(std::size_t n) {
        if (n == 0) return nullptr;
        void* ptr = _aligned_malloc(n * sizeof(T), Alignment);
        if (!ptr) throw std::bad_alloc();
        return static_cast<T*>(ptr);
    }

    void deallocate(T* p, std::size_t) noexcept {
        _aligned_free(p);
    }

    template <typename U>
    struct rebind {
        using other = AlignedAllocator<U, Alignment>;
    };
};

template <typename T1, std::size_t A1, typename T2, std::size_t A2>
bool operator==(const AlignedAllocator<T1, A1>&, const AlignedAllocator<T2, A2>&) noexcept {
    return A1 == A2;
}

template <typename T1, std::size_t A1, typename T2, std::size_t A2>
bool operator!=(const AlignedAllocator<T1, A1>&, const AlignedAllocator<T2, A2>&) noexcept {
    return A1 != A2;
}
