/**
 * @file random_generators.h
 * @brief Provides functions to generate randomized user, channel, content, and interaction data for simulation purposes.
 */

#ifndef RANDOM_GENERATORS_H
#define RANDOM_GENERATORS_H

#include <relations.h>
#include <vector>
#include <stdexcept>

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
    protected:
    int64_t _nextUserId = 0;            /// Next available user ID.
    int64_t _nextChannelId = 0;         /// Next available channel ID.
    int64_t _nextContentId = 0;         /// Next available content ID.
    int64_t _nextWatchId = 0;           /// Next available view ID.
    int64_t _nextCommentId = 0;         /// Next available comment ID.
    int64_t _nextInteractionId = 0;     /// Next available interaction ID.
    
    public:
    IdBatchManager();
    inline int64_t getNextUserId() { return _nextUserId; }                  /// Return next available user ID.
    inline int64_t getNextChannelId() { return _nextChannelId; }            /// Return next available channel ID.
    inline int64_t getNextContentId() { return _nextContentId; }            /// Return next available content ID.
    inline int64_t getNextWatchId() { return _nextWatchId; }                /// Return next available view ID.
    inline int64_t getNextCommentId() { return _nextCommentId; }            /// Return next available comment ID.
    inline int64_t getNextInteractionId() { return _nextInteractionId; }    /// Return next available interaction ID.

    /**
     * @brief Returns the next available user ID and advances.
     * @param amount Number of IDs to reserve (default = 1).
     * @return The first ID of the reserved sequence.
     */
    int64_t getAndAdvanceUserId(int64_t amount = 1) {
        if (amount < 0) {
            throw std::invalid_argument("Amount must be non-negative");
        }
        int64_t start =  _nextUserId;
        _nextUserId += amount;
        return start;
    }

    /**
     * @brief Returns the next available channel ID and advances.
     * @param amount Number of IDs to reserve (default = 1).
     * @return The first ID of the reserved sequence.
     */
    int64_t getAndAdvanceChannelId(int64_t amount = 1) {
        if (amount < 0) {
            throw std::invalid_argument("Amount must be non-negative");
        }
        int64_t start =  _nextChannelId;
        _nextChannelId += amount;
        return start;
    }

    /**
     * @brief Returns the next available content ID and advances.
     * @param amount Number of IDs to reserve (default = 1).
     * @return The first ID of the reserved sequence.
     */
    int64_t getAndAdvanceContentId(int64_t amount = 1) {
        if (amount < 0) {
            throw std::invalid_argument("Amount must be non-negative");
        }
        int64_t start =  _nextContentId;
        _nextContentId += amount;
        return start;
    }

    /**
     * @brief Returns the next available view ID and advances.
     * @param amount Number of IDs to reserve (default = 1).
     * @return The first ID of the reserved sequence.
     */
    int64_t getAndAdvanceWatchId(int64_t amount = 1) {
        if (amount < 0) {
            throw std::invalid_argument("Amount must be non-negative");
        }
        int64_t start =  _nextWatchId;
        _nextWatchId += amount;
        return start;
    }

    /**
     * @brief Returns the next available comment ID and advances.
     * @param amount Number of IDs to reserve (default = 1).
     * @return The first ID of the reserved sequence.
     */
    int64_t getAndAdvanceCommentId(int64_t amount = 1) {
        if (amount < 0) {
            throw std::invalid_argument("Amount must be non-negative");
        }
        int64_t start =  _nextCommentId;
        _nextCommentId += amount;
        return start;
    }

    /**
     * @brief Returns the next available interaction ID and advances.
     * @param amount Number of IDs to reserve (default = 1).
     * @return The first ID of the reserved sequence.
     */
    int64_t getAndAdvanceInteractionId(int64_t amount = 1) {
        if (amount < 0) {
            throw std::invalid_argument("Amount must be non-negative");
        }
        int64_t start =  _nextInteractionId;
        _nextInteractionId += amount;
        return start;
    }

    void reset() {
        _nextUserId = 0;
        _nextChannelId = 0;
        _nextContentId = 0;
        _nextWatchId = 0;
        _nextCommentId = 0;
        _nextInteractionId = 0;
    }
};

/**
 * @brief A constant representing an invalid ID (-1).
 */
constexpr int64_t invalidId = -1;

class RandomGenerator {
    public:
    explicit RandomGenerator(IdBatchManager& idManager, bool debugMode = false) : ids(idManager), debugMode(debugMode) {}

    void addRandomUser(Relations::UserArray& userInput, int numberOfUsers);
    void addRandomChannel(Relations::ChannelArray& channelInput, Relations::UserArray& userInput, float creationRatio, int creationDate);
    void addRandomSubs(Relations::UserSubChannelArray& subsInput, const Relations::ChannelArray& channelInput, const Relations::UserArray& userInput);
    void addRandomContent(Relations::ContentArray& contentInput, const Relations::ChannelArray& channelInput, float creationRatio);
    void addRandomWatch(Relations::UserWatchContArray& watchInput, const Relations::UserArray& userInput, const Relations::ContentArray& contentInput, int maxWatchSameTime, float userWatchRatio);
    void addRandomComment(Relations::CommentArray& commentsInput, const Relations::UserWatchContArray& watchInput, float commentRatio);
    void addRandomReplies(Relations::ReplyArray& repliesInput, const Relations::CommentArray& commentsInput, const Relations::UserWatchContArray& watchInput, float replyRatio);
    void addRandomInteractions(Relations::UserContInteractionArray& interactionInput, const Relations::UserWatchContArray& watchInput, float interactRatio);

    private:
    IdBatchManager& ids;
    bool debugMode;
};

}
#endif