#ifndef RECOMMENDATOR_H
#define RECOMMENDATOR_H

#include <relations.h>
#include <relation_properties.h>
#include <cstdint>

namespace Recommendations{

    Relations::id* recommendate(
        const Relations::UserArray& userInput, 
        const Relations::ContentArray& contentInput, 
        const Relations::UserSubChannelArray& subsInput, 
        const Relations::UserWatchContArray& watchInput,
        const Relations::CommentArray& commentInput,
        const Relations::UserContInteractionArray& interactionInput,
        int64_t watchMaxIndex,
        Relations::id userId, 
        uint8_t numOfRecommendtions);

    Relations::id* getNMostPopular(const Relations::UserWatchContArray& watchInput, int64_t watchMaxIndex, int8_t nMost);
}
#endif