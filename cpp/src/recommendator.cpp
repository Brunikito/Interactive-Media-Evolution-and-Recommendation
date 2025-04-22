#include "../include/recommendator.h"
#include "../include/relations.h"
#include "../include/relation_properties.h"
#include <cstdint>
#include <iostream>
#include <ranges>
#include <algorithm>
#include <array>

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
    const Relations::ContentArray& contentInput, //*%ofTags
    const Relations::UserSubChannelArray& subsInput, // *2
    const Relations::UserWatchContArray& watchInput, // 1
    const Relations::CommentArray& commentInput, // 10
    const Relations::UserContInteractionArray& interactionInput, // 20 15 -20
    std::vector<Relations::id, AlignedAllocator<Relations::id, 32>> userIds, 
    uint8_t numOfRecommendations){
        std::vector<Relations::id*, AlignedAllocator<Relations::id*, 32>> recommendations(userInput.size(), nullptr);
        std::array<int8_t, RelationProperties::NUMTAGS> zeroedTags = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
        std::vector<std::array<int8_t, RelationProperties::NUMTAGS>, AlignedAllocator<std::array<int8_t, RelationProperties::NUMTAGS>, 32>> tagWatchCount(userInput.size(), zeroedTags);
        std::vector<Relations::id, AlignedAllocator<Relations::id, 32>> contentBaseScore(contentInput.size(), 1);

        //Iterate over watch
        for (size_t i = 0; i < watchInput.size(); i++){
            int64_t watchId = i;
            contentBaseScore[watchInput.contentWatchedIds[watchId]] += WATCH_VALUE*watchInput.watchDurations[watchId];
        }

        //Iterate over comment
        for (size_t i = 0; i < commentInput.size(); i++){
            int64_t commentId = i;
            contentBaseScore[commentInput.commentContentIds[commentId]] += COMMENT_VALUE;
        }
        
        //Iterate over interactions
        for (size_t i = 0; i < interactionInput.size(); i++){
            int64_t interactionId = i;
            int8_t valueToAdd;
            Relations::InteractionType interactionType = interactionInput.interactionTypes[interactionId];
            if (interactionType == Relations::LIKE) valueToAdd = LIKE_VALUE;
            else if (interactionType == Relations::DISLIKE) valueToAdd = DISLIKE_VALUE;
            else if (interactionType == Relations::REPORT) valueToAdd = REPORT_VALUE;
            else if (interactionType == Relations::SHARE) valueToAdd = SHARE_VALUE;
            else if (interactionType == Relations::SAVE) valueToAdd = SAVE_VALUE;
            contentBaseScore[interactionInput.contentInteractedIds[interactionId]] += valueToAdd;
        
            //Get ocurrencesOfTags
            for (int8_t j = 0; j < contentInput.contentTags[interactionInput.contentInteractedIds[interactionId]][3]; j++){
                tagWatchCount[interactionInput.userInteractIds[interactionId]][contentInput.contentTags[interactionInput.contentInteractedIds[interactionId]][j]] += 1;
            }
        }
        
        // Get the adjusted values, and the best for the user
        // Basicaly, get the adjusted value by the tags for the user
        std::vector<Relations::id, AlignedAllocator<Relations::id, 32>> contentAdjustedScore(contentInput.size());
        for (size_t i = 0; i < userIds.size(); i++){
            Relations::id userId = userIds[i];
            for (size_t j = 0; j < contentAdjustedScore.size(); j++){
                int8_t multiplier = 1;
                for (int8_t k = 0; k < contentInput.contentTags[j][3]; k++){
                    multiplier += tagWatchCount[userId][contentInput.contentTags[j][k]];
                }
                contentAdjustedScore[j] = contentBaseScore[j] * multiplier;
                if (subsInput.channelIdSubscribers[contentInput.contentChannelIds[j]]->search(userId)) contentAdjustedScore[j] *= SUB_MULTIPLIER;
            }

            std::ranges::partial_sort(contentAdjustedScore.begin(), contentAdjustedScore.begin() + numOfRecommendations, contentAdjustedScore.end(), std::greater{});
            Relations::id* userRecommendations = new Relations::id[numOfRecommendations];
            for (int8_t j = 0; j < numOfRecommendations; j++){
                userRecommendations[j] = contentAdjustedScore[j];
            }
            recommendations[userId] = userRecommendations;
        }

        return recommendations;
    }
        
}