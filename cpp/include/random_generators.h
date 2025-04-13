/**
 * @file random_generators.h
 * @brief Provides functions to generate randomized user, channel, content, and interaction data for simulation purposes.
 */

#ifndef RANDOM_GENERATORS_H
#define RANDOM_GENERATORS_H

#include <relations.h>
#include <unordered_map>

/**
 * @namespace RandomRelations
 * @brief Contains utilities for generating random entities and interactions related to users, channels, content, and activity.
 */
namespace RandomRelations {

/**
 * @class IdBatchManager
 * @brief Manages unique identifiers for different entities in the system.
 *
 * This class provides methods to generate and advance unique identifiers
 * for users, channels, content, views, comments, and interactions.
 */
class IdBatchManager {
    public:
        /// Next available user ID.
        int nextUserId = 0;
        /// Next available channel ID.
        int nextChannelId = 0;
        /// Next available content ID.
        int nextContentId = 0;
        /// Next available view ID.
        int nextWatchId = 0;
        /// Next available comment ID.
        int nextCommentId = 0;
        /// Next available interaction ID.
        int nextInteractionId = 0;

        /**
         * @brief Returns the next available user ID and advances.
         * @param amount Number of IDs to reserve (default = 1).
         * @return The first ID of the reserved sequence.
         */
        int getAndAdvanceUserId(int amount = 1) {
            if (amount < 0) {
                throw std::invalid_argument("Amount must be non-negative");
            }
            int start = nextUserId;
            nextUserId += amount;
            return start;
        }

        /**
         * @brief Returns the next available channel ID and advances.
         * @param amount Number of IDs to reserve (default = 1).
         * @return The first ID of the reserved sequence.
         */
        int getAndAdvanceChannelId(int amount = 1) {
            if (amount < 0) {
                throw std::invalid_argument("Amount must be non-negative");
            }
            int start = nextChannelId;
            nextChannelId += amount;
            return start;
        }

        /**
         * @brief Returns the next available content ID and advances.
         * @param amount Number of IDs to reserve (default = 1).
         * @return The first ID of the reserved sequence.
         */
        int getAndAdvanceContentId(int amount = 1) {
            if (amount < 0) {
                throw std::invalid_argument("Amount must be non-negative");
            }
            int start = nextContentId;
            nextContentId += amount;
            return start;
        }

        /**
         * @brief Returns the next available view ID and advances.
         * @param amount Number of IDs to reserve (default = 1).
         * @return The first ID of the reserved sequence.
         */
        int getAndAdvanceWatchId(int amount = 1) {
            if (amount < 0) {
                throw std::invalid_argument("Amount must be non-negative");
            }
            int start = nextWatchId;
            nextWatchId += amount;
            return start;
        }

        /**
         * @brief Returns the next available comment ID and advances.
         * @param amount Number of IDs to reserve (default = 1).
         * @return The first ID of the reserved sequence.
         */
        int getAndAdvanceCommentId(int amount = 1) {
            if (amount < 0) {
                throw std::invalid_argument("Amount must be non-negative");
            }
            int start = nextCommentId;
            nextCommentId += amount;
            return start;
        }

        /**
         * @brief Returns the next available interaction ID and advances.
         * @param amount Number of IDs to reserve (default = 1).
         * @return The first ID of the reserved sequence.
         */
        int getAndAdvanceInteractionId(int amount = 1) {
            if (amount < 0) {
                throw std::invalid_argument("Amount must be non-negative");
            }
            int start = nextInteractionId;
            nextInteractionId += amount;
            return start;
        }
};

/**
 * @brief A constant representing an invalid ID (-1).
 */
constexpr int invalidId = -1;

/**
 * @brief Adds randomly generated users to the provided user map.
 * 
 * @param userInput The map to populate with new users.
 * @param numberOfUsers Number of users to generate.
 */
void addRandomUser(std::unordered_map<int, Relations::User>& userInput, int numberOfUsers, IdBatchManager& ids);

/**
 * @brief Adds randomly generated channels based on a ratio of the number of users.
 * 
 * @param channelInput The map to populate with new channels.
 * @param userInput The existing map of users for channel ownership.
 * @param creationRatio Ratio of channels to users.
 */
void addRandomChannel(std::unordered_map<int, Relations::Channel>& channelInput, std::unordered_map<int, Relations::User>& userInput, float creationRatio, IdBatchManager& ids);

/**
 * @brief Adds random user subscriptions to channels.
 * 
 * @param subsInput The map to populate with user-channel subscriptions.
 * @param channelInput The existing channels available for subscription.
 * @param userInput The existing users subscribing to channels.
 */
void addRandomSubs(std::unordered_map<int, Relations::UserSubChannel>& subsInput, const std::unordered_map<int, Relations::Channel>& channelInput, const std::unordered_map<int, Relations::User>& userInput, IdBatchManager& ids);

/**
 * @brief Adds random content entries to the content map.
 * 
 * @param contentInput The map to populate with content.
 * @param creationRatio Ratio of content per user/channel.
 */
void addRandomContent(std::unordered_map<int, Relations::Content>& contentInput, float creationRatio, IdBatchManager& ids);

/**
 * @brief Adds random user-content watch interactions.
 * 
 * @param watchInput The map to populate with watch events.
 * @param userInput The users watching content.
 * @param contentInput The content being watched.
 * @param maxWatchSameTime Maximum concurrent watch interactions allowed.
 * @param userWatchRatio Ratio of how much users engage in watching content.
 */
void addRandomWatch(std::unordered_map<int, Relations::UserWatchCont>& watchInput, const std::unordered_map<int, Relations::User>& userInput, const std::unordered_map<int, Relations::Content>& contentInput, int maxWatchSameTime, float userWatchRatio, IdBatchManager& ids);

/**
 * @brief Adds random comments from users on watched content.
 * 
 * @param commentsInput The map to populate with comments.
 * @param watchInput The user watch history to determine comment context.
 * @param commentRatio Ratio of watch events that result in a comment.
 */
void addRandomComment(std::unordered_map<int, Relations::Comment>& commentsInput, const std::unordered_map<int, Relations::UserWatchCont>& watchInput, float commentRatio, IdBatchManager& ids);

/**
 * @brief Adds random replies to existing comments.
 * 
 * @param repliesInput The map to populate with replies.
 * @param commentsInput Existing comments to reply to.
 * @param watchInput User watch data to guide reply authorship.
 * @param replyRatio Ratio of comments that receive replies.
 */
void addRandomReplies(std::unordered_map<int, Relations::Reply>& repliesInput, std::unordered_map<int, Relations::Comment>& commentsInput, const std::unordered_map<int, Relations::UserWatchCont>& watchInput, float replyRatio, IdBatchManager& ids);

/**
 * @brief Adds random user interactions (likes, dislikes, etc.) with content.
 * 
 * @param interactionInput The map to populate with interaction data.
 * @param watchInput The watch context from which interactions may originate.
 * @param interactRatio Ratio of watches that result in an interaction.
 */
void addRandomInteractions(std::unordered_map<int, Relations::UserContInteraction>& interactionInput, const std::unordered_map<int, Relations::UserWatchCont>& watchInput, float interactRatio, IdBatchManager& ids);

}

#endif