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

namespace Recommendations{

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
        
        int nThreads = omp_get_max_threads();
        std::vector<std::vector<Relations::id, AlignedAllocator<Relations::id, 32>>> threadAdjustedScores(
        nThreads, std::vector<Relations::id, AlignedAllocator<Relations::id, 32>>(contentInput.size()));
        
        #pragma omp parallel for schedule(static)
        for (size_t i = 0; i < userIds.size(); i++){
            Relations::id userId = userIds[i];
            auto& localAdjustedScore = threadAdjustedScores[omp_get_thread_num()];
            int8_t multiplier;
            auto& userTagWatch = tagWatchCount[userId];
            auto& userSubs = *subsInput.userIdSubscriptions[userId];
            
            for (size_t j = 0; j < localAdjustedScore.size(); j++){
                multiplier = 0;
                auto& tags = contentInput.contentTags[j];
                uint8_t tagCount = tags[3];
                if (tagCount > 0) multiplier += userTagWatch[tags[0]];
                if (tagCount > 1) multiplier += userTagWatch[tags[1]];
                if (tagCount > 2) multiplier += userTagWatch[tags[2]];
                localAdjustedScore[j] = contentBaseScore[j] * multiplier;
                if (userSubs.search(contentInput.contentChannelIds[j])) localAdjustedScore[j] *= SUB_MULTIPLIER;
            }

            std::ranges::partial_sort(localAdjustedScore.begin(), localAdjustedScore.begin() + numOfRecommendations, localAdjustedScore.end(), std::greater{});
            
            Relations::id* userRecommendations = new Relations::id[numOfRecommendations];
            
            for (int8_t j = 0; j < numOfRecommendations; j++){
                userRecommendations[j] = localAdjustedScore[j];
            }
            recommendations[userId] = userRecommendations;
        }

        return recommendations;
    }
        
}