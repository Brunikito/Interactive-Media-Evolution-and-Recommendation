/**
 * @file relations.h
 * @brief Defines data structures representing users, channels, content, interactions, and schedules in a media platform simulation.
 */

#ifndef RELATIONS_H
#define RELATIONS_H

#include <vector>
#include <array>
#include <cstdint>
#include <memory>
#include <cstddef>
#include <cstdlib>
#include <stdexcept>
#include "aligned_alocator.h"
#include "unordered_linked_list.h"

#define ALIGN_VEC(type) std::vector<type, AlignedAllocator<type, 32>>
using ULL = UnorderedLinkedList::UnorderedLinkedList;
using AlignedULLVec = std::vector<ULL*, AlignedAllocator<ULL*, 32>>;

namespace Relations {

/**
 * @typedef id
 * @brief Integer identifier used for entities like users, channels, content, etc.
 */
using id = int64_t;

/**
 * @typedef datetime
 * @brief Represents a timestamp (e.g., creation or interaction time).
 */
using datetime = unsigned int;

/**
 * @typedef deltatime
 * @brief Represents duration of events like watching or content length.
 */
using deltatime = unsigned int;

/**
 * @enum ContentType
 * @brief Represents the type of content.
 */
enum ContentType: uint8_t {
    VIDEO,  ///< Regular video
    SHORT,  ///< Short-form content
    LIVE    ///< Live broadcast
};

/**
 * @enum GenderType
 * @brief Binary gender type.
 */
enum GenderType: unsigned char {
    MALE = 0,    ///< Male
    FEMALE = 1  ///< Female
};

/**
 * @enum ContentStatus
 * @brief Visibility or accessibility status of content.
 */
enum ContentStatus: uint8_t {
    PUBLIC,     ///< Publicly available
    PRIVATE,    ///< Only accessible to owner
    NONLISTED,  ///< Hidden but accessible via direct link
    DELETED     ///< Removed content
};

/**
 * @enum InteractionType
 * @brief Represents types of user interactions with content.
 */
enum InteractionType: uint8_t {
    LIKE,    ///< User liked the content
    DISLIKE, ///< User disliked the content
    REPORT,  ///< User reported the content
    SHARE,   ///< User shared the content
    SAVE     ///< User saved the content
};

/**
 * @struct Schedule
 * @brief Represents a user's daily routine and work pattern.
 */
struct Schedule {
    datetime bedTime;           ///< Time the user goes to bed
    datetime wakeTime;          ///< Time the user wakes up
    datetime lunchTime;         ///< Lunchtime
    datetime dinnerTime;        ///< Dinnertime
    datetime workTime;          ///< Time work starts
    datetime freeFromWorkTime;  ///< Time work ends
    unsigned char workDays;     ///< Bitmask for active workdays
};

using UnsignedChar4_t = std::array<unsigned char, 4>;

using ScheduleId_t = unsigned char;

struct UserArray {
    ALIGN_VEC(id) userIds;
    ALIGN_VEC(id) userChannelIds;
    ALIGN_VEC(UnsignedChar4_t) userLanguages;
    ALIGN_VEC(ScheduleId_t) userSchedules;
    ALIGN_VEC(GenderType) userGenders;
    ALIGN_VEC(unsigned char) userAges;
    ALIGN_VEC(unsigned char) userLocations;
    ALIGN_VEC(unsigned char) userOccupations;
    ALIGN_VEC(unsigned char) userEducations;

    void resize(size_t new_size) {
        userIds.resize(new_size);
        userChannelIds.resize(new_size);
        userLanguages.resize(new_size);
        userSchedules.resize(new_size);
        userAges.resize(new_size);
        userGenders.resize(new_size);
        userLocations.resize(new_size);
        userOccupations.resize(new_size);
        userEducations.resize(new_size);
    }

    size_t size() const {
        return userIds.size(); // ou qualquer um dos vetores
    }
};

struct ChannelArray {
    ALIGN_VEC(id) channelOwnerIds;
    ALIGN_VEC(id) channelIds;
    ALIGN_VEC(unsigned int) channelCreationDates;
    ALIGN_VEC(unsigned char) channelLanguages;
    ALIGN_VEC(unsigned char) channelLocations;
    ALIGN_VEC(unsigned char) channelCategories;

    void resize(size_t new_size) {
        channelOwnerIds.resize(new_size);
        channelIds.resize(new_size);
        channelCreationDates.resize(new_size);
        channelLanguages.resize(new_size);
        channelLocations.resize(new_size);
        channelCategories.resize(new_size);
    }

    size_t size() const { return channelIds.size(); }
};

struct UserSubChannelArray {
    AlignedULLVec userIdSubscriptions;
    AlignedULLVec channelIdSubscribers;

    void resizeUsers(size_t new_size) {
        userIdSubscriptions.resize(new_size);
    }

    void resizeChannels(size_t new_size) {
        channelIdSubscribers.resize(new_size);
    }

    size_t sizeUsers() const { return userIdSubscriptions.size(); }
    size_t sizeChannels() const { return channelIdSubscribers.size(); }
};

struct ContentArray {
    ALIGN_VEC(id) contentChannelIds;
    ALIGN_VEC(ContentType) contentTypes;
    ALIGN_VEC(id) contentIds;
    ALIGN_VEC(datetime) contentPubDateTimes;
    ALIGN_VEC(ContentStatus) contentStatuses;
    ALIGN_VEC(unsigned char) contentCategories;
    ALIGN_VEC(unsigned char) contentLanguages;
    ALIGN_VEC(unsigned char) contentIndRatings;
    ALIGN_VEC(UnsignedChar4_t) contentTags;
    ALIGN_VEC(deltatime) contentDurations;
    ALIGN_VEC(int) contentViewCounts;
    ALIGN_VEC(int) contentLikeCounts;
    ALIGN_VEC(int) contentDislikeCounts;
    ALIGN_VEC(int) contentCommentCounts;
    ALIGN_VEC(bool) isLiveNows;
    ALIGN_VEC(id) fullvideoIds;

    void resize(size_t new_size) {
        contentChannelIds.resize(new_size);
        contentTypes.resize(new_size);
        contentIds.resize(new_size);
        contentPubDateTimes.resize(new_size);
        contentStatuses.resize(new_size);
        contentCategories.resize(new_size);
        contentLanguages.resize(new_size);
        contentIndRatings.resize(new_size);
        contentTags.resize(new_size);
        contentDurations.resize(new_size);
        contentViewCounts.resize(new_size);
        contentLikeCounts.resize(new_size);
        contentDislikeCounts.resize(new_size);
        contentCommentCounts.resize(new_size);
        isLiveNows.resize(new_size);
        fullvideoIds.resize(new_size);
    }

    size_t size() const { return contentIds.size(); }
};

struct UserWatchContArray {
    ALIGN_VEC(id) userWatcherIds;
    ALIGN_VEC(id) contentWatchedIds;
    ALIGN_VEC(id) watchIds;
    ALIGN_VEC(datetime) watchDateTimes;
    ALIGN_VEC(deltatime) watchDurations;
    ALIGN_VEC(bool) isHappenings;

    void resize(size_t new_size) {
        userWatcherIds.resize(new_size);
        contentWatchedIds.resize(new_size);
        watchIds.resize(new_size);
        watchDateTimes.resize(new_size);
        watchDurations.resize(new_size);
        isHappenings.resize(new_size);
    }

    size_t size() const { return watchIds.size(); }
};

struct CommentArray {
    ALIGN_VEC(id) commentAuthorIds;
    ALIGN_VEC(id) commentContentIds;
    ALIGN_VEC(id) commentIds;
    ALIGN_VEC(datetime) commentDateTimes;

    void resize(size_t new_size) {
        commentAuthorIds.resize(new_size);
        commentContentIds.resize(new_size);
        commentIds.resize(new_size);
        commentDateTimes.resize(new_size);
    }

    size_t size() const { return commentIds.size(); }
};

struct ReplyArray {
    ALIGN_VEC(id) originalCommentIds;
    ALIGN_VEC(id) commentReplyIds;

    void resize(size_t new_size) {
        originalCommentIds.resize(new_size);
        commentReplyIds.resize(new_size);
    }

    size_t size() const { return commentReplyIds.size(); }
};

struct UserContInteractionArray {
    ALIGN_VEC(id) userInteractIds;
    ALIGN_VEC(id) contentInteractedIds;
    ALIGN_VEC(id) interactionIds;
    ALIGN_VEC(InteractionType) interactionTypes;

    void resize(size_t new_size) {
        userInteractIds.resize(new_size);
        contentInteractedIds.resize(new_size);
        interactionIds.resize(new_size);
        interactionTypes.resize(new_size);
    }

    size_t size() const { return interactionIds.size(); }
};

}

#endif