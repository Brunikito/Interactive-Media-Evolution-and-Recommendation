#ifndef RECOMMENDATOR_H
#define RECOMMENDATOR_H

#include <relations.h>
#include <relation_properties.h>
#include <cstdint>
#include <vector>
#include <aligned_alocator.h>

namespace Recommendations{

    std::vector<Relations::id*, AlignedAllocator<Relations::id*, 32>> recommendateSelectedUsers(
        const Relations::UserArray& userInput, 
        const Relations::ContentArray& contentInput,
        const Relations::UserSubChannelArray& subsInput,
        const Relations::UserWatchContArray& watchInput,
        const Relations::CommentArray& commentInput,
        const Relations::UserContInteractionArray& interactionInput,
        std::vector<Relations::id, AlignedAllocator<Relations::id, 32>> userIds, 
        uint8_t numOfRecommendations);

}
#endif