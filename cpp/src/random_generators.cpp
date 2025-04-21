#include "../include/relations.h"
#include "../include/relation_properties.h"
#include "../include/random_generators.h"
#include "../utils/fast_copy.cpp"
#include "../utils/timer.cpp"
#include "../include/random_utils.h"
#include <omp.h>
#include <vector>
#include <iostream>
#include <thread>
#include <future>
#include <atomic>
#include <immintrin.h> // para SIMD
#include <random>
#include <cstdint>
#include <algorithm>
#include <cmath>
#include "pcg_random.hpp"

namespace RandomRelations {

IdBatchManager::IdBatchManager() = default;
void RandomGenerator::addRandomUser(Relations::UserArray &userInput, int numberOfUsers) {
    TimerManager timer;
    // Verifica se o número de usuários é válido (maior ou igual a 0)
    if(numberOfUsers <= 0) {
        throw std::invalid_argument("numberOfUsers must be greater than or equal to 0.");
    }

    // Definir o tamanho de pacote de SIMD
    constexpr int simdWidth = 32;

    // Garantir que o número de usuários seja múltiplo de simdWidth
    int adjustedNumberOfUsers = numberOfUsers - (numberOfUsers % simdWidth);
    int64_t initialId = ids.getAndAdvanceUserId(numberOfUsers);

    size_t requiredSize = initialId + numberOfUsers;
    if(userInput.size() < requiredSize) {
        userInput.resize(requiredSize);
    }

    const __m256i binary = _mm256_set_epi8(
                               1U, 0U, 1U, 0U, 1U, 0U, 1U, 0U,
                               1U, 0U, 1U, 0U, 1U, 0U, 1U, 0U,
                               1U, 0U, 1U, 0U, 1U, 0U, 1U, 0U,
                               1U, 0U, 1U, 0U, 1U, 0U, 1U, 0U);

    const __m256i channels = _mm256_set_epi64x(
                                 -1, -1, -1, -1);

    // Defina o valor padrão — aqui: idioma 0 com count = 1 → [0, 0, 0, 1]
    const __m256i defaultLangs = _mm256_set1_epi32(0x01000000); // big endian: [0, 0, 0, 1]

    if(debugMode)
        timer.start("Main Loop");
    // Parâmetros para o OpenMP
    #pragma omp parallel proc_bind(close)
    {
        std::random_device rd;
        pcg64_fast rng(rd() + omp_get_thread_num());

        std::uniform_int_distribution<uint8_t> ageDist(13, 100);
        std::uniform_int_distribution<uint8_t> occDist(0, 143);
        std::uniform_int_distribution<uint8_t> locDist(0, 60);
        std::binomial_distribution<uint8_t> eduDist(16, 0.75);
        std::uniform_int_distribution<uint8_t> languageDist(0, 156);

        alignas(32) uint8_t ages[simdWidth];
        alignas(32) uint8_t occs[simdWidth];
        alignas(32) uint8_t locs[simdWidth];
        alignas(32) uint8_t edus[simdWidth];
        alignas(32) uint8_t languages[8][4];

        const __m256i genders = _mm256_set_epi8(
                                    1U, 0U, 1U, 0U, 1U, 0U, 1U, 0U,
                                    1U, 0U, 1U, 0U, 1U, 0U, 1U, 0U,
                                    1U, 0U, 1U, 0U, 1U, 0U, 1U, 0U,
                                    1U, 0U, 1U, 0U, 1U, 0U, 1U, 0U);

        const __m256i channels = _mm256_set_epi64x(-1, -1, -1, -1);

        #pragma omp for schedule(static)
        for(int i = 0; i < adjustedNumberOfUsers; i += simdWidth) {
            int64_t baseId = initialId + i;

            // Gerar valores aleatórios
            for(int j = 0; j < simdWidth; j++) {
                ages[j] = ageDist(rng);
                occs[j] = occDist(rng);
                locs[j] = locDist(rng);
                edus[j] = (ages[j] < 23) ? (ages[j] - 6) : eduDist(rng);
            }

            // Carregar vetores AVX
            _mm256_store_si256((__m256i *)&userInput.userAges[baseId], _mm256_load_si256((__m256i *)ages));
            _mm256_store_si256((__m256i *)&userInput.userOccupations[baseId], _mm256_load_si256((__m256i *)occs));
            _mm256_store_si256((__m256i *)&userInput.userLocations[baseId], _mm256_load_si256((__m256i *)locs));
            _mm256_store_si256((__m256i *)&userInput.userEducations[baseId], _mm256_load_si256((__m256i *)edus));

            _mm256_store_si256((__m256i *)&userInput.userGenders[baseId], genders);
            _mm256_store_si256((__m256i *)&userInput.userSchedules[baseId], genders); // reuso do binário alternado

            for(int j = 0; j < simdWidth; j += 4) {
                int64_t baseIdInt64_t = baseId + j;
                __m256i uids = _mm256_set_epi64x(
                                   baseIdInt64_t + 3, baseIdInt64_t + 2, baseIdInt64_t + 1, baseIdInt64_t);
                _mm256_store_si256((__m256i *)&userInput.userIds[baseIdInt64_t], uids);
                _mm256_store_si256((__m256i *)&userInput.userChannelIds[baseIdInt64_t], channels);
            }

            for(int j = 0; j < simdWidth; j += 8) {
                int64_t langBase = baseId + j;
                for(int k = 0; k < 8; k++) {
                    languages[k][0] = RelationProperties::countryLanguages[locs[k]];
                    languages[k][1] = (languages[k][0] + languageDist(rng)) % 156;
                    languages[k][2] = (languages[k][0] + languageDist(rng)) % 156;
                    languages[k][3] = 1;
                    if(languages[k][0] != languages[k][1]) {
                        languages[k][3]++;
                        if((languages[k][2] != languages[k][1]) && (languages[k][2] != languages[k][0])) {
                            languages[k][3]++;
                        }
                    } 
                }
                _mm256_store_si256((__m256i *)&userInput.userLanguages[langBase], _mm256_load_si256((__m256i *)languages));
            }
        }
    }

    if(debugMode)
        timer.stop("Main Loop");

    if(debugMode)
        timer.start("Else Loop");

    #pragma omp parallel for schedule(static) proc_bind(close)
    for(int i = adjustedNumberOfUsers; i < numberOfUsers; i++) {
        int64_t uid = initialId + i;
        pcg64_fast rng(uid); // seed estável pra debug
        std::uniform_int_distribution<uint8_t> ageDist(13, 100);
        std::uniform_int_distribution<uint8_t> occDist(0, 143);
        std::uniform_int_distribution<uint8_t> locDist(0, 60);
        std::binomial_distribution<uint8_t> eduDist(16, 0.75);
        std::uniform_int_distribution<uint8_t> languageDist(0, 156);
        uint8_t languages[4];

        uint8_t age = ageDist(rng);
        userInput.userIds[uid] = uid;
        userInput.userChannelIds[uid] = -1;
        userInput.userSchedules[uid] = 0U;
        userInput.userGenders[uid] = Relations::GenderType::MALE;
        userInput.userAges[uid] = age;
        uint8_t loc = locDist(rng);
        userInput.userLocations[uid] = loc;
        userInput.userOccupations[uid] = occDist(rng);
        userInput.userEducations[uid] = (age < 23) ? (age - 6) : eduDist(rng);

        languages[0] = RelationProperties::countryLanguages[loc];
        languages[1] = (languages[0] + languageDist(rng)) % 156;
        languages[2] = (languages[1] + languageDist(rng)) % 156;
        if(languages[0] == languages[1]) {
            languages[3] = 1;
        } else if(languages[1] == languages[2] || languages[0] == languages[2]) {
            languages[3] = 2;
        } else {
            languages[3] = 3;
        }
        *reinterpret_cast<uint32_t *>(&userInput.userLanguages[uid]) = *reinterpret_cast<uint32_t *>(languages);
    }

    if(debugMode)
        timer.stop("Else Loop");
    if(debugMode)
        timer.showTimes();
    return;
}

void RandomGenerator::addRandomChannel(Relations::ChannelArray &channelInput, Relations::UserArray &userInput, float creationRatio, int creationDate) {
    TimerManager timer;
    if(debugMode)
        timer.start("Verifications");

    if(creationRatio <= 0) {
        throw std::invalid_argument("Ratio of creation must be greater than zero.");
    }
    if(creationRatio > 1) {
        throw std::invalid_argument("Ratio of creation must be less than or equal to one.");
    }
    if(channelInput.size() >= userInput.size()) {
        throw std::invalid_argument("Can't create channels: there is no user left without channel.");
    }

    if(userInput.size() == 0) {
        throw std::invalid_argument("Can't create channels: there is no user.");
    }

    size_t avaliableSize = userInput.size() - channelInput.size();
    int64_t numberOfChannels = static_cast<int64_t>(avaliableSize * creationRatio);
    if(numberOfChannels == 0) {
        return;
    }

    if(debugMode)
        timer.stop("Verifications");

    if(debugMode)
        timer.start("Auxiliar vector");
    // Fast vector of non having channel
    std::vector<int64_t, AlignedAllocator<int64_t, 32>> userWithoutChannelIds(avaliableSize);

    // primeiro: descobrir quantos cada thread vai escrever
    int nThreads = omp_get_max_threads();
    std::vector<size_t> threadCounts(nThreads, 0);

    // contar localmente
    #pragma omp parallel
    {
        int tid = omp_get_thread_num();
        size_t localCount = 0;

        #pragma omp for schedule(static)
        for(int i = 0; i < userInput.size(); i++) {
            if(userInput.userChannelIds[i] == -1) {
                localCount++;
            }
        }
        threadCounts[tid] = localCount;
    }

    // calcular prefix sum das posições de escrita
    std::vector<size_t> threadOffsets(nThreads, 0);
    for(int i = 1; i < nThreads; i++) {
        threadOffsets[i] = threadOffsets[i - 1] + threadCounts[i - 1];
    }

    // agora escreve direto nas posições corretas
    #pragma omp parallel
    {
        int tid = omp_get_thread_num();
        size_t offset = threadOffsets[tid];
        size_t localIndex = 0;

        #pragma omp for schedule(static)
        for(int i = 0; i < userInput.size(); i++) {
            if(userInput.userChannelIds[i] == -1) {
                userWithoutChannelIds[offset + localIndex] = userInput.userIds[i];
                localIndex++;
            }
        }
    }

    if(debugMode)
        timer.stop("Auxiliar vector");

    if(debugMode)
        timer.start("Shuffle vector");

    // Shuffle the vector
    RandomUtils::shuffleLinspace(userWithoutChannelIds, numberOfChannels);
    std::random_device rd;

    if(debugMode)
        timer.stop("Shuffle vector");
    if(debugMode) timer.start("Full loop");

    // Channel Modification
    int64_t initialId = ids.getAndAdvanceChannelId(numberOfChannels);

    // Definir o tamanho de pacote de SIMD
    constexpr int simdWidth = 32;
    int adjustedNumberOfChannels = numberOfChannels - (numberOfChannels % simdWidth);

    size_t requiredSize = initialId + numberOfChannels;
    if(channelInput.size() < requiredSize) {
        channelInput.resize(requiredSize);
    }

    #pragma omp parallel proc_bind(close)
    {
        pcg64_fast rng(rd() + omp_get_thread_num());

        std::uniform_int_distribution<uint8_t> langDist(0, 2);
        std::uniform_int_distribution<uint8_t> tagDist(0, 14);

        alignas(32) uint8_t langs[simdWidth];
        alignas(32) uint8_t tags[simdWidth];
        alignas(32) uint8_t locations[simdWidth];

        const __m256i creationDateMM256 = _mm256_set_epi32(
                                              creationDate, creationDate, creationDate, creationDate,
                                              creationDate, creationDate, creationDate, creationDate);

        #pragma omp for schedule(static)
        for(int i = 0; i < adjustedNumberOfChannels; i += simdWidth) {
            int64_t baseId = initialId + i;

            // Gerar valores aleatórios
            for(int j = 0; j < simdWidth; j++) {
                int userIdx = i + j;
                int userId = userWithoutChannelIds[userIdx];
                int langCount = userInput.userLanguages[userId][3];
                int randIndex = langDist(rng);
                langs[j] = userInput.userLanguages[userId][randIndex];
                tags[j] = tagDist(rng);
                locations[j] = userInput.userLocations[userId];
            }

            // Carregar vetores AVX
            _mm256_store_si256((__m256i *)&channelInput.channelLanguages[baseId], _mm256_load_si256((__m256i *)langs));
            _mm256_store_si256((__m256i *)&channelInput.channelCategories[baseId], _mm256_load_si256((__m256i *)tags));
            _mm256_store_si256((__m256i *)&channelInput.channelLocations[baseId], _mm256_load_si256((__m256i *)locations));

            for(int j = 0; j < simdWidth; j += 4) {
                int64_t baseIdIdsLoop = baseId + j;
                __m256i channelIdsM256 = _mm256_set_epi64x(
                                             baseIdIdsLoop + 3, baseIdIdsLoop + 2,
                                             baseIdIdsLoop + 1, baseIdIdsLoop);

                __m256i channelOwnerIdsM256 = _mm256_set_epi64x(
                                                  userWithoutChannelIds[i + j + 3], userWithoutChannelIds[i + j + 2],
                                                  userWithoutChannelIds[i + j + 1], userWithoutChannelIds[i + j]);

                _mm256_store_si256((__m256i *)&channelInput.channelIds[baseIdIdsLoop], channelIdsM256);
                _mm256_store_si256((__m256i *)&channelInput.channelOwnerIds[baseIdIdsLoop], channelOwnerIdsM256);
            }

            for(int j = 0; j < simdWidth; j += 8) {
                int64_t langBase = baseId + j;
                _mm256_store_si256((__m256i *)&channelInput.channelCreationDates[langBase], creationDateMM256);
            }

            for(int j = 0; j < simdWidth; j++) {
                int64_t userBase = i + j;
                userInput.userChannelIds[userWithoutChannelIds[userBase]] = userBase;
            }

        }

        #pragma omp parallel for schedule(static) proc_bind(close)
        for(int i = adjustedNumberOfChannels; i < numberOfChannels; i++) {
            int64_t channelId = initialId + i;
            pcg64_fast rng(channelId); // seed estável pra debug
            std::uniform_int_distribution<uint8_t> langDist(0, 2);
            std::uniform_int_distribution<uint8_t> tagDist(0, 14);
            unsigned char channelLanguage = langDist(rng);
            if(channelLanguage >= userInput.userLanguages[userWithoutChannelIds[i]][3]) {
                channelLanguage = userInput.userLanguages[userWithoutChannelIds[i]][userInput.userLanguages[userWithoutChannelIds[i]][3] - 1];
            }
            else channelLanguage = userInput.userLanguages[userWithoutChannelIds[i]][channelLanguage];
            channelInput.channelCategories[i] = tagDist(rng);
            channelInput.channelCreationDates[i] = creationDate;
            channelInput.channelIds[i] = channelId;
            channelInput.channelLanguages[i] = channelLanguage;
            channelInput.channelLocations[i] = userInput.userLocations[userWithoutChannelIds[i]];
            channelInput.channelOwnerIds[i] = userWithoutChannelIds[i];
            userInput.userChannelIds[userWithoutChannelIds[i]] = channelId;
        }
    }
    
    if(debugMode)
        timer.showTimes();
    return;
}

void RandomGenerator::addRandomSubs(Relations::UserSubChannelArray& subsInput, const Relations::ChannelArray& channelInput, const Relations::UserArray& userInput, float maxUserRatio){
    TimerManager timer;
    if(debugMode) timer.start("Verifications");

    if(maxUserRatio <= 0) {
        throw std::invalid_argument("Ratio of subscriptions must be greater than zero.");
    }
    if(maxUserRatio > 1) {
        throw std::invalid_argument("Ratio of subscriptions must be less than or equal to one.");
    }
    if(channelInput.size() == 0) {
        throw std::invalid_argument("Can't create subscriptions: there is no channel.");
    }
    if(userInput.size() == 0) {
        throw std::invalid_argument("Can't create subscriptions: there is no user.");
    }

    subsInput.resizeUsers(userInput.size());
    subsInput.resizeChannels(channelInput.size());

    size_t maxPossibleSubscriptions;
    if (userInput.size() < channelInput.size()) maxPossibleSubscriptions = userInput.size();
    else maxPossibleSubscriptions = channelInput.size();
    size_t numberOfSubscriptions = static_cast<size_t>(maxPossibleSubscriptions * maxUserRatio);

    if(numberOfSubscriptions == 0) {
        return;
    }

    if(debugMode) timer.stop("Verifications");

    if(debugMode) timer.start("Auxiliar vectors creation and shuffle");
    std::vector<int64_t, AlignedAllocator<int64_t, 32>> randomUserIds = FastCopy::copyAlignedVector(userInput.userIds);
    RandomUtils::shuffleLinspace(randomUserIds, numberOfSubscriptions);
    std::vector<int64_t, AlignedAllocator<int64_t, 32>> randomchannelIds = FastCopy::copyAlignedVector(channelInput.channelIds);
    RandomUtils::shuffleLinspace(randomchannelIds, numberOfSubscriptions);
    if(debugMode) timer.stop("Auxiliar vectors creation and shuffle");
    
    if(debugMode) timer.start("Main loop");
    #pragma omp parallel for schedule(static)
    for (size_t i = 0; i < numberOfSubscriptions; i++) {

        int64_t userId = randomUserIds[i];
        int64_t channelId = randomchannelIds[i];

        UnorderedLinkedList::UnorderedLinkedList* userList = subsInput.userIdSubscriptions[userId];
        UnorderedLinkedList::UnorderedLinkedList* channelList = subsInput.channelIdSubscribers[channelId];

        if (!userList) {userList = new UnorderedLinkedList::UnorderedLinkedList(); subsInput.userIdSubscriptions[userId] = userList;} 
        if (!channelList) {channelList = new UnorderedLinkedList::UnorderedLinkedList(); subsInput.channelIdSubscribers[channelId] = channelList;}

        bool alreadySubscribed = false;
        if (userList->getSize() <= channelList->getSize()) {
            alreadySubscribed = userList->search(channelId);
        } else {
            alreadySubscribed = channelList->search(userId);
        }

        if (!alreadySubscribed) {
            auto node1 = new UnorderedLinkedList::Node(channelId);
            node1->nextNode = userList->head;
            userList->head = node1;
            userList->size++;

            auto node2 = new UnorderedLinkedList::Node(userId);
            node2->nextNode = channelList->head;
            channelList->head = node2;
            channelList->size++;
        }
    }
    if(debugMode) timer.stop("Main loop");
    if(debugMode) timer.showTimes();
    return;
}

void RandomGenerator::addRandomContent(Relations::ContentArray& contentInput, const Relations::ChannelArray& channelInput, float creationRatio, int creationDate){
    TimerManager timer;
    if(debugMode) timer.start("Verifications");

    if(creationRatio <= 0 || creationRatio > 1) 
        throw std::invalid_argument("Ratio of creation must be in (0,1].");
    if(channelInput.size() == 0) 
        throw std::invalid_argument("Can't create content: there is no channel.");

    int64_t numberOfContent = static_cast<int64_t>(channelInput.size() * creationRatio);
    if(numberOfContent == 0) return;

    int64_t initialId = ids.getAndAdvanceContentId(numberOfContent);
    contentInput.resize(contentInput.size() + numberOfContent);

    if(debugMode) timer.stop("Verifications");
    if(debugMode) timer.start("Auxiliar vectors creation and shuffle");

    std::vector<int64_t, AlignedAllocator<int64_t, 32>> randomchannelIds = FastCopy::copyAlignedVector(channelInput.channelIds);
    RandomUtils::shuffleLinspace(randomchannelIds, numberOfContent);

    if(debugMode) timer.stop("Auxiliar vectors creation and shuffle");
    if(debugMode) timer.start("Main loop");

    constexpr int simdWidth = 32;
    int64_t adjustedNumberOfContent = numberOfContent - (numberOfContent % simdWidth);

    #pragma omp parallel
    {
        pcg64_fast rng(std::random_device{}() + omp_get_thread_num());
        std::uniform_int_distribution<uint8_t> tagDist(0, 14);
        std::uniform_int_distribution<uint8_t> languageDist(0, 156);
        std::uniform_int_distribution<uint8_t> percentDist(0, 100);

        alignas(32) uint8_t types[simdWidth];
        alignas(32) uint8_t statuses[simdWidth];
        alignas(32) uint8_t ratings[simdWidth];
        alignas(32) uint8_t categories[simdWidth];
        alignas(32) uint8_t languages[simdWidth];
        alignas(32) uint8_t zeros[simdWidth] = {};

        __m256i creationDateMM256 = _mm256_set1_epi32(creationDate);

        #pragma omp for schedule(static)
        for(int64_t i = 0; i < adjustedNumberOfContent; i += simdWidth){
            int64_t baseId = initialId + i;

            for(int j = 0; j < simdWidth; j++){
                int64_t channelId = randomchannelIds[i + j];
                contentInput.contentIds[baseId + j] = baseId + j;
                contentInput.contentChannelIds[baseId + j] = channelId;

                uint8_t type = percentDist(rng);
                if (type <= 45) types[j] = Relations::ContentType::VIDEO;
                else if (type <= 85) types[j] = Relations::ContentType::SHORT;
                else types[j] = Relations::ContentType::LIVE;

                uint8_t status = percentDist(rng);
                if (status <= 80) statuses[j] = Relations::ContentStatus::PUBLIC;
                else if (status <= 90) statuses[j] = Relations::ContentStatus::PRIVATE;
                else statuses[j] = Relations::ContentStatus::NONLISTED;

                ratings[j] = (percentDist(rng) <= 35) ? 0 :
                             (percentDist(rng) <= 55) ? 1 :
                             (percentDist(rng) <= 90) ? 2 : 3;

                categories[j] = (percentDist(rng) <= 80) ? 
                                channelInput.channelCategories[channelId] : 
                                tagDist(rng);

                languages[j] = (percentDist(rng) <= 80) ? 
                               channelInput.channelLanguages[channelId] : 
                               languageDist(rng);
            }

            _mm256_store_si256((__m256i*)&contentInput.contentTypes[baseId], _mm256_load_si256((__m256i*)types));
            _mm256_store_si256((__m256i*)&contentInput.contentStatuses[baseId], _mm256_load_si256((__m256i*)statuses));
            _mm256_store_si256((__m256i*)&contentInput.contentIndRatings[baseId], _mm256_load_si256((__m256i*)ratings));
            _mm256_store_si256((__m256i*)&contentInput.contentCategories[baseId], _mm256_load_si256((__m256i*)categories));
            _mm256_store_si256((__m256i*)&contentInput.contentLanguages[baseId], _mm256_load_si256((__m256i*)languages));

            // fixed values
            _mm256_store_si256((__m256i*)&contentInput.contentLikeCounts[baseId], _mm256_load_si256((__m256i*)zeros));
            _mm256_store_si256((__m256i*)&contentInput.contentDislikeCounts[baseId], _mm256_load_si256((__m256i*)zeros));
            _mm256_store_si256((__m256i*)&contentInput.contentViewCounts[baseId], _mm256_load_si256((__m256i*)zeros));
            _mm256_store_si256((__m256i*)&contentInput.contentCommentCounts[baseId], _mm256_load_si256((__m256i*)zeros));

            for(int j = 0; j < simdWidth; j++){
                int64_t cid = baseId + j;
                int64_t channelId = randomchannelIds[i + j];

                // Tags (pode vetorizar mais no futuro)
                contentInput.contentTags[cid][0] = categories[j];
                contentInput.contentTags[cid][1] = (categories[j] + languageDist(rng)) % 156;
                contentInput.contentTags[cid][2] = (categories[j] + languageDist(rng)) % 156;
                contentInput.contentTags[cid][3] = 1;
                if(contentInput.contentTags[cid][0] != contentInput.contentTags[cid][1]){
                    contentInput.contentTags[cid][3]++;
                    if((contentInput.contentTags[cid][2] != contentInput.contentTags[cid][1]) &&
                       (contentInput.contentTags[cid][2] != contentInput.contentTags[cid][0])){
                        contentInput.contentTags[cid][3]++;
                    }
                }

                // Duração
                if(types[j] == Relations::ContentType::VIDEO){
                    contentInput.contentDurations[cid] = static_cast<unsigned int>(RandomUtils::sampleBeta(2, 4, rng) * 3600);
                } else if(types[j] == Relations::ContentType::SHORT){
                    contentInput.contentDurations[cid] = static_cast<unsigned int>(RandomUtils::sampleBeta(4, 2, rng) * 60);
                } else {
                    contentInput.contentDurations[cid] = static_cast<unsigned int>(RandomUtils::sampleBeta(2, 3, rng) * 18000);
                }
                
                //std::cout << "#";
                // Is live
                contentInput.isLiveNows[cid] = (types[j] == Relations::ContentType::LIVE);
                contentInput.fullvideoIds[cid] = -1;
                contentInput.contentPubDateTimes[cid] = creationDate;
                //std::cout << "#";
            } 
        }

        // Parte restante sem SIMD
        #pragma omp for schedule(static)
        for (int64_t i = adjustedNumberOfContent; i < numberOfContent; i++){
            int64_t cid = initialId + i;
            int64_t channelId = randomchannelIds[i];

            contentInput.contentIds[cid] = cid;
            contentInput.contentChannelIds[cid] = channelId;
            contentInput.contentPubDateTimes[cid] = creationDate;

            uint8_t type = percentDist(rng);
            contentInput.contentTypes[cid] = (type <= 45) ? Relations::ContentType::VIDEO : (type <= 85 ? Relations::ContentType::SHORT : Relations::ContentType::LIVE);
            contentInput.isLiveNows[cid] = (contentInput.contentTypes[cid] == Relations::ContentType::LIVE);

            uint8_t status = percentDist(rng);
            contentInput.contentStatuses[cid] = (status <= 80) ? Relations::ContentStatus::PUBLIC : (status <= 90 ? Relations::ContentStatus::PRIVATE : Relations::ContentStatus::NONLISTED);

            uint8_t rating = percentDist(rng);
            contentInput.contentIndRatings[cid] = (rating <= 35) ? 0 : (rating <= 55 ? 1 : (rating <= 90 ? 2 : 3));

            contentInput.contentLikeCounts[cid] = 0;
            contentInput.contentDislikeCounts[cid] = 0;
            contentInput.contentViewCounts[cid] = 0;
            contentInput.contentCommentCounts[cid] = 0;

            uint8_t category = (percentDist(rng) <= 80) ? channelInput.channelCategories[channelId] : tagDist(rng);
            contentInput.contentCategories[cid] = category;

            uint8_t language = (percentDist(rng) <= 80) ? channelInput.channelLanguages[channelId] : languageDist(rng);
            contentInput.contentLanguages[cid] = language;

            contentInput.contentTags[cid][0] = category;
            contentInput.contentTags[cid][1] = (category + languageDist(rng)) % 156;
            contentInput.contentTags[cid][2] = (category + languageDist(rng)) % 156;
            contentInput.contentTags[cid][3] = 1;
            if(contentInput.contentTags[cid][0] != contentInput.contentTags[cid][1]){
                contentInput.contentTags[cid][3]++;
                if((contentInput.contentTags[cid][2] != contentInput.contentTags[cid][1]) &&
                   (contentInput.contentTags[cid][2] != contentInput.contentTags[cid][0])){
                    contentInput.contentTags[cid][3]++;
                }
            }

            if(contentInput.contentTypes[cid] == Relations::ContentType::VIDEO){
                contentInput.contentDurations[cid] = static_cast<unsigned int>(RandomUtils::sampleBeta(2, 4, rng) * 3600);
            } else if(contentInput.contentTypes[cid] == Relations::ContentType::SHORT){
                contentInput.contentDurations[cid] = static_cast<unsigned int>(RandomUtils::sampleBeta(4, 2, rng) * 60);
            } else {
                contentInput.contentDurations[cid] = static_cast<unsigned int>(RandomUtils::sampleBeta(2, 3, rng) * 18000);
            }

            contentInput.fullvideoIds[cid] = -1;
        }
    }

    if(debugMode) timer.stop("Main loop");
    if(debugMode) timer.showTimes();
    return;
}
}
