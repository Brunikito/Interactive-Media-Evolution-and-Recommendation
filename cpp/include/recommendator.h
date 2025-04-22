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
        const Relations::ContentArray& contentInput, //*%ofTags
        const Relations::UserSubChannelArray& subsInput, // *2
        const Relations::UserWatchContArray& watchInput, // 1
        const Relations::CommentArray& commentInput, // 10
        const Relations::UserContInteractionArray& interactionInput, // 20 15 -20
        std::vector<Relations::id, AlignedAllocator<Relations::id, 32>> userIds, 
        uint8_t numOfRecommendations);

}
#endif