#include "../include/recommendator.h"
#include "../include/relations.h"
#include "../include/relation_properties.h"
#include <cstdint>
#include <iostream>
#include <ranges>
#include <algorithm>
#include <array>
#include <omp.h>
#include <immintrin.h>
#include <atomic>
#include <numeric>

namespace Recommendations{

    bool isIn(int64_t number, std::vector<int64_t, AlignedAllocator<int64_t, 32>> vector){
        for (size_t i = 0; i < vector.size(); i++){
            if (number = vector[i]) return true;
        }
        return false;
    }

    constexpr int8_t WATCH_VALUE = 1;
    constexpr int8_t COMMENT_VALUE = 25;
    constexpr int8_t LIKE_VALUE = 20;
    constexpr int8_t DISLIKE_VALUE = -20;
    constexpr int8_t REPORT_VALUE = -30;
    constexpr int8_t SHARE_VALUE = 15;
    constexpr int8_t SAVE_VALUE = 30;
    constexpr int8_t SUB_MULTIPLIER = 2;

    std::vector<Relations::id*, AlignedAllocator<Relations::id*, 32>> recommendateSelectedUsers(
    const Relations::UserArray& userInput, 
    const Relations::ContentArray& contentInput,
    const Relations::UserSubChannelArray& subsInput,
    const Relations::UserWatchContArray& watchInput,
    const Relations::CommentArray& commentInput,
    const Relations::UserContInteractionArray& interactionInput,
    std::vector<Relations::id, AlignedAllocator<Relations::id, 32>> userIds, 
    uint8_t numOfRecommendations){
        std::vector<Relations::id*, AlignedAllocator<Relations::id*, 32>> recommendations(userInput.size(), nullptr);

        // Alocar contentBaseScore com atomic
        std::vector<std::atomic<Relations::id>> contentBaseScore(contentInput.size());
        for (auto& v : contentBaseScore) v.store(1, std::memory_order_relaxed);

        // Alocar tagWatchCount (userInput.size() x NUMTAGS)
        std::vector<std::array<std::atomic<int8_t>, RelationProperties::NUMTAGS>> tagWatchCount(userInput.size());
        for (auto& userTags : tagWatchCount)
            for (auto& v : userTags)
                v.store(0, std::memory_order_relaxed);
        
        #pragma omp parallel for schedule(static)
        for (size_t i = 0; i < watchInput.size(); i++) {
            contentBaseScore[watchInput.contentWatchedIds[i]].fetch_add(
                WATCH_VALUE * watchInput.watchDurations[i],
                std::memory_order_relaxed);
        }

        #pragma omp parallel for schedule(static)
        for (size_t i = 0; i < commentInput.size(); i++) {
            contentBaseScore[commentInput.commentContentIds[i]].fetch_add(
                COMMENT_VALUE,
                std::memory_order_relaxed);
        }

        #pragma omp parallel for schedule(static)
        for (size_t i = 0; i < interactionInput.size(); i++) {
            int64_t contentId = interactionInput.contentInteractedIds[i];
            int64_t userId = interactionInput.userInteractIds[i];
            int8_t valueToAdd;

            switch (interactionInput.interactionTypes[i]) {
                case Relations::LIKE:    valueToAdd = LIKE_VALUE; break;
                case Relations::DISLIKE: valueToAdd = DISLIKE_VALUE; break;
                case Relations::REPORT:  valueToAdd = REPORT_VALUE; break;
                case Relations::SHARE:   valueToAdd = SHARE_VALUE; break;
                case Relations::SAVE:    valueToAdd = SAVE_VALUE; break;
            }

            contentBaseScore[contentId].fetch_add(valueToAdd, std::memory_order_relaxed);

            for (int8_t j = 0; j < contentInput.contentTags[contentId][3]; j++) {
                int8_t tagId = contentInput.contentTags[contentId][j];
                tagWatchCount[userId][tagId].fetch_add(1, std::memory_order_relaxed);
            }
        }
        

        std::vector<std::atomic<int64_t>, AlignedAllocator<std::atomic<int64_t>, 32>> TagMapBase(contentBaseScore.size());
        std::vector<int64_t, AlignedAllocator<int64_t, 32>> bestContent(50*RelationProperties::NUMTAGS, -1);
        std::atomic<int8_t> sizeBestContent;
        sizeBestContent.store(0, std::memory_order_relaxed);
        std::vector<int64_t, AlignedAllocator<int64_t, 32>> actualBest50(50);

        #pragma omp parallel for schedule(static)
        for (int8_t i = 0; i < RelationProperties::NUMTAGS; i++){
            const auto& indexes = contentInput.contentIds;
            for (auto& v : TagMapBase) v.store(-1, std::memory_order_relaxed);
            for (int64_t j = 0; j < TagMapBase.size(); j++){
                if(contentInput.contentTags[j][0] == i) TagMapBase[j].store(contentBaseScore[j].load(std::memory_order_relaxed), std::memory_order_relaxed);
                else if(contentInput.contentTags[j][3] > 1 && contentInput.contentTags[j][1] == i) TagMapBase[j].store(contentBaseScore[j].load(std::memory_order_relaxed), std::memory_order_relaxed);
                else if(contentInput.contentTags[j][3] > 2 && contentInput.contentTags[j][2] == i) TagMapBase[j].store(contentBaseScore[j].load(std::memory_order_relaxed), std::memory_order_relaxed);
            }
            std::vector<Relations::id> sortedTopIndexes(50);
            std::partial_sort_copy(
                indexes.begin(), indexes.end(),
                sortedTopIndexes.begin(), sortedTopIndexes.end(),
                [&](int a, int b) {
                    return TagMapBase[a] > TagMapBase[b]; // ordem decrescente
                }
            );
            for (int8_t j = 0; j < 50; j++){
                if (!isIn(sortedTopIndexes[j], bestContent)) {
                    bestContent[sizeBestContent++] = sortedTopIndexes[j];
                }
            }
        }


        int nThreads = omp_get_max_threads();
        std::vector<std::vector<Relations::id, AlignedAllocator<Relations::id, 32>>> threadAdjustedScores(
        nThreads, std::vector<Relations::id, AlignedAllocator<Relations::id, 32>>(contentBaseScore.size(), -1));
        
        #pragma omp parallel for schedule(static)
        for (size_t i = 0; i < userIds.size(); i++){
            Relations::id userId = userIds[i];
            auto& localAdjustedScore = threadAdjustedScores[omp_get_thread_num()];
            int multiplier;
            const auto& userTagWatch = tagWatchCount[userId];
            auto& userSubs = *subsInput.userIdSubscriptions[userId];
            const auto& indexes = contentInput.contentIds;
            
            for (size_t j = 0; j < bestContent.size(); j++){
                if (bestContent[j] == -1) continue;
                size_t contentId = bestContent[j];
                multiplier = 0;
                const auto& tags = contentInput.contentTags[contentId];
                const uint8_t tagCount = tags[3];
                multiplier += userTagWatch[tags[0]];
                if (tagCount > 1) multiplier += userTagWatch[tags[1]];
                if (tagCount > 2) multiplier += userTagWatch[tags[2]];
                localAdjustedScore[contentId] = contentBaseScore[contentId] * multiplier;
                if (userSubs.search(contentInput.contentChannelIds[contentId])) localAdjustedScore[contentId] *= SUB_MULTIPLIER;
            }
            
            std::vector<Relations::id> sortedTopIndexes(numOfRecommendations);

            std::partial_sort_copy(
                bestContent.begin(), bestContent.end(),
                sortedTopIndexes.begin(), sortedTopIndexes.end(),
                [&](int a, int b) {
                    return localAdjustedScore[a] > localAdjustedScore[b]; // ordem decrescente
                }
            );

            Relations::id* userRecommendations = new Relations::id[numOfRecommendations];
            for (int8_t j = 0; j < numOfRecommendations; j++){
                userRecommendations[j] = sortedTopIndexes[j];
            }
            recommendations[userId] = userRecommendations;
            
            for (size_t j = 0; j < bestContent.size(); j++){
                if (bestContent[j] == -1) continue;
                localAdjustedScore[bestContent[j]] = -1;
            }

        }

        return recommendations;
    }
        
}