#include <gtest/gtest.h>
#include "../include/recommendator.h"
#include "../include/relation_properties.h"
#include "../include/aligned_alocator.h"
#include "../include/relation_properties.h"
#include <vector>
#include <unordered_set>

using namespace Recommendations;
using namespace Relations;

class RecommendatorTest : public ::testing::Test {
    protected:
        UserArray users;
        ContentArray contents;
        UserSubChannelArray subscriptions;
        UserWatchContArray watches;
        CommentArray comments;
        UserContInteractionArray interactions;
    
        std::vector<id, AlignedAllocator<id, 32>> userIds;
        uint8_t numRecs = 3;
    
        void SetUp() override {
            users.resize(1);
            users.userIds[0] = 0;
            users.userChannelIds[0] = 10;
    
            contents.resize(3);
            for (int i = 0; i < 3; i++) {
                contents.contentIds[i] = i;
                contents.contentChannelIds[i] = 10;
                contents.contentTags[i] = { static_cast<unsigned char>(i % RelationProperties::NUMTAGS), 0, 0, 1 };
            }
    
            watches.resize(1);
            watches.userWatcherIds[0] = 0;
            watches.contentWatchedIds[0] = 0;
            watches.watchDurations[0] = 1;
    
            comments.resize(1);
            comments.commentAuthorIds[0] = 0;
            comments.commentContentIds[0] = 1;
    
            interactions.resize(1);
            interactions.userInteractIds[0] = 0;
            interactions.contentInteractedIds[0] = 2;
            interactions.interactionTypes[0] = LIKE;
    
            subscriptions.resizeUsers(1);
            subscriptions.userIdSubscriptions[0] = new ULL();
            subscriptions.userIdSubscriptions[0]->insert(10);  // subscribed to channel 10
    
            userIds.push_back(0);
        }
    
        void TearDown() override {
            for (auto* ptr : subscriptions.userIdSubscriptions) {
                delete ptr;
            }
        }
};

TEST_F(RecommendatorTest, ReturnsRecommendations) {
    auto result = recommendateSelectedUsers(
        users,
        contents,
        subscriptions,
        watches,
        comments,
        interactions,
        userIds,
        numRecs
    );

    ASSERT_EQ(result.size(), users.size());
    ASSERT_NE(result[0], nullptr);
    for (int i = 0; i < numRecs; i++) {
        EXPECT_GE(result[0][i], 0);
        EXPECT_LT(result[0][i], contents.size());
    }

    delete[] result[0];
}



int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}