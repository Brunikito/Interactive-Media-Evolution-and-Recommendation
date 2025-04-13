/**
 * @file relations.h
 * @brief Defines data structures representing users, channels, content, interactions, and schedules in a media platform simulation.
 */

#ifndef RELATIONS_H
#define RELATIONS_H

#include <vector>
#include <cstdint>

namespace Relations {

/**
 * @typedef id
 * @brief Integer identifier used for entities like users, channels, content, etc.
 */
using id = int;

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
enum class ContentType: uint8_t {
    VIDEO,  ///< Regular video
    SHORT,  ///< Short-form content
    LIVE    ///< Live broadcast
};

/**
 * @enum GenderType
 * @brief Binary gender type.
 */
enum class GenderType: bool {
    MALE = true,    ///< Male
    FEMALE = false  ///< Female
};

/**
 * @enum ContentStatus
 * @brief Visibility or accessibility status of content.
 */
enum class ContentStatus: uint8_t {
    PUBLIC,     ///< Publicly available
    PRIVATE,    ///< Only accessible to owner
    NONLISTED,  ///< Hidden but accessible via direct link
    DELETED     ///< Removed content
};

/**
 * @enum InteractionType
 * @brief Represents types of user interactions with content.
 */
enum class InteractionType: uint8_t {
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

/**
 * @struct User
 * @brief Stores all attributes related to a platform user.
 */
struct User {
    id userId;                                  ///< Unique user identifier
    id userChannelId;                           ///< ID of the channel owned by the user
    std::vector<unsigned char> userLanguages;   ///< Preferred or spoken languages
    Schedule userSchedule;                      ///< Daily routine schedule
    unsigned char userAge;                      ///< User's age
    GenderType userGender;                      ///< Gender type
    unsigned char userLocation[2];              ///< Encoded country/location info
    unsigned char userOccupation;               ///< Occupation code
    unsigned char userEducation;                ///< Education level code
};

/**
 * @struct Channel
 * @brief Represents a content-producing entity owned by a user.
 */
struct Channel {
    id channelOwnerId;                  ///< Owner's user ID
    id channelId;                       ///< Unique channel ID
    unsigned int channelCreationDate;   ///< Channel creation date (timestamp)
    unsigned char channelLanguage;      ///< Main language of the channel
    unsigned char channelLocation[2];   ///< Location (country/region code)
    unsigned char channelCategory;      ///< Category/type of content
};

/**
 * @struct UserSubChannel
 * @brief Represents a user subscription to a channel.
 */
struct UserSubChannel {
    id subscriberId;            ///< Subscribing user's ID
    id subscribedChannelId;     ///< Subscribed channel ID
};

/**
 * @struct Content
 * @brief Metadata for content uploaded by a channel.
 */
struct Content {
    id contentChannelId;                    ///< ID of the uploading channel
    ContentType contentType;                ///< Type of content
    id contentId;                           ///< Unique content ID
    datetime contentPubDateTime;            ///< Publication date
    ContentStatus contentStatus;            ///< Content visibility status
    unsigned char contentCategory;          ///< Content category
    unsigned char contentLanguage;          ///< Language of the content
    unsigned char contentIndRating;         ///< Content rating (e.g., PG, 18+)
    std::vector<unsigned char> contentTags; ///< List of tag identifiers
    deltatime contentDuration;              ///< Duration in seconds
    int contentViewCount;                   ///< Number of views
    int contentLikeCount;                   ///< Number of likes
    int contentDislikeCount;                ///< Number of dislikes
    int contentCommentCount;                ///< Number of comments
    bool isLiveNow;                         ///< Whether the content is currently live
    id fullvideoId;                         ///< Full video ID if part of a segment
};

/**
 * @struct UserWatchCont
 * @brief Represents a user's viewing session of a content.
 */
struct UserWatchCont {
    id userWatcherId;           ///< ID of the user watching
    id contentWatchedId;        ///< ID of the content being watched
    id watchId;                 ///< Unique ID for the watch session
    datetime watchDateTime;     ///< When the watching began
    deltatime watchDuration;    ///< Duration of the watching session
    bool isHappening;           ///< Indicates if the watching is still ongoing
};

/**
 * @struct Comment
 * @brief Represents a comment made on a piece of content.
 */
struct Comment {
    id commentAuthorId;         ///< ID of the commenting user
    id commentContentId;        ///< ID of the content being commented on
    id commentId;               ///< Unique comment ID
    datetime commentDateTime;   ///< Time when the comment was made
};

/**
 * @struct Reply
 * @brief Represents a reply to a comment.
 */
struct Reply {
    id originalCommentId;   ///< ID of the comment being replied to
    id commentReplyId;      ///< ID of the reply (comment)
};

/**
 * @struct UserContInteraction
 * @brief Represents an interaction between a user and a content item.
 */
struct UserContInteraction {
    id userInteractId;                  ///< ID of the user interacting
    id contentInteractedId;             ///< ID of the content interacted with
    id interactionId;                   ///< Unique ID for the interaction
    InteractionType interactionType;    ///< Type of interaction (like, dislike, share, etc.)
};

}

#endif