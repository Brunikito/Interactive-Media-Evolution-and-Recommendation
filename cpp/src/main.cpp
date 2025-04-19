#include <iostream>
#include <chrono>
#include "../include/relations.h"
#include "../include/random_generators.h"
#include "../include/random_utils.h"
#include <unordered_set>
#include <numeric>

int main() {
    Relations::UserArray userArray;
    Relations::ChannelArray channelArray;
    Relations::UserSubChannelArray subArray;
    Relations::ContentArray contentArray;
    RandomRelations::IdBatchManager idManager;
    RandomRelations::RandomGenerator generator(idManager, true);
    constexpr int userCount = 10'000'000;

    auto start = std::chrono::high_resolution_clock::now();
    std::cout << std::endl << "Initiated User Generation";
    generator.addRandomUser(userArray, userCount);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;
    std::cout << "Time to add " << userCount << " users: "
              << duration.count() << " seconds." << std::endl;

    start = std::chrono::high_resolution_clock::now();
    constexpr int date = 0;
    constexpr float channelCreationRatio = 1;
    std::cout << std::endl << "Initiated Channel Generation";
    generator.addRandomChannel(channelArray, userArray, channelCreationRatio, date);
    end = std::chrono::high_resolution_clock::now();
    duration = end - start;
    std::cout << "Time to add " << channelCreationRatio*100 << "'%' channels: "
              << duration.count() << " seconds." << std::endl;

    start = std::chrono::high_resolution_clock::now();
    std::cout << std::endl << "Initiated Subs Generation";
    constexpr float maxUserRatio = 1;
    generator.addRandomSubs(subArray, channelArray, userArray, maxUserRatio);
    end = std::chrono::high_resolution_clock::now();
    duration = end - start;
    std::cout << "Time to sub " << maxUserRatio*100 << "'%' users: "
            << duration.count() << " seconds." << std::endl;

    start = std::chrono::high_resolution_clock::now();
    constexpr float contentCreationRatio = 1;
    std::cout << std::endl << "Initiated Content Generation";
    generator.addRandomContent(contentArray, channelArray, contentCreationRatio, date);
    end = std::chrono::high_resolution_clock::now();
    duration = end - start;
    std::cout << "Time to add " << contentCreationRatio*100 << "'%' Content: "
                << duration.count() << " seconds." << std::endl;
    
    return 0;

}




/*
bool hasAllUniqueElements(const std::vector<int64_t, AlignedAllocator<int64_t, 32>>& linspace) {
    std::unordered_set<int64_t> seen;
    for (auto val : linspace) {
        if (!seen.insert(val).second) {
            std::cerr << "Duplicate found: " << val << "\n";
            return false;
        }
    }
    return true;
}

int main(){
    int32_t size = 100'000'001;
    auto start = std::chrono::high_resolution_clock::now();
    std::cout << "Initiated User Generation" << std::endl;
    std::vector<int32_t, AlignedAllocator<int32_t, 32>> vector = RandomUtils::fastSieve(size);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;
    std::cout << "Time to get " << size << " in sieve: "
              << duration.count() << " seconds." << std::endl;

    start = std::chrono::high_resolution_clock::now();
    std::cout << "Initiated Coprime Generation" << std::endl;
    int64_t coprime = RandomUtils::computeCoprime(size);
    end = std::chrono::high_resolution_clock::now();
    duration = end - start;
    std::cout << "Time to get coprime: "
    << duration.count() << " seconds." << std::endl;
    if (std::gcd(coprime, size) != 1) {
        std::cerr << "Coprime " << coprime << " is NOT coprime with size " << size << "!" << std::endl;
    } else {
        std::cout << "Verified coprime: " << coprime << std::endl;
    }

    std::vector<int64_t, AlignedAllocator<int64_t, 32>> linspace(size);

    // Preencher de 0 até size - 1
    #pragma omp parallel for
    for (int64_t i = 0; i < size; ++i) {
        linspace[i] = i;
    }

    std::cout << "Running shuffleLinspace on " << size << " elements...\n";
    start = std::chrono::high_resolution_clock::now();
    RandomUtils::shuffleLinspace(linspace, 100'000'000);
    end = std::chrono::high_resolution_clock::now();
    duration = end - start;
    std::cout << "Shuffle done in " << duration.count() << " seconds.\n";

    if (hasAllUniqueElements(linspace)) {
        std::cout << "All elements are unique.\n";
    } else {
        std::cerr << "Duplicate elements detected!\n";
    }
    

    return 0;
}
*/