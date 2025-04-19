#include <gtest/gtest.h>
#include "../include/random_generators.h"
#include "../include/relation_properties.h"
#include <vector>

using namespace RandomRelations;

class IdBatchManagerTest : public testing::Test {
    public:
        IdBatchManagerTest();
        IdBatchManager idManager;

};
IdBatchManagerTest::IdBatchManagerTest() {}
TEST_F(IdBatchManagerTest, AllStartZero) {
    EXPECT_EQ(idManager.getNextUserId(), 0);
    EXPECT_EQ(idManager.getNextChannelId(), 0);
    EXPECT_EQ(idManager.getNextCommentId(), 0);
    EXPECT_EQ(idManager.getNextContentId(), 0);
    EXPECT_EQ(idManager.getNextInteractionId(), 0);
    EXPECT_EQ(idManager.getNextWatchId(), 0);
}
TEST_F(IdBatchManagerTest, HandlesNegativeIncrement) {
    EXPECT_ANY_THROW(idManager.getAndAdvanceUserId(-1));
    EXPECT_ANY_THROW(idManager.getAndAdvanceChannelId(-1));
    EXPECT_ANY_THROW(idManager.getAndAdvanceCommentId(-1));
    EXPECT_ANY_THROW(idManager.getAndAdvanceContentId(-1));
    EXPECT_ANY_THROW(idManager.getAndAdvanceInteractionId(-1));
    EXPECT_ANY_THROW(idManager.getAndAdvanceWatchId(-1));
}
TEST_F(IdBatchManagerTest, ZeroIncrementWorks) {
    EXPECT_EQ(idManager.getAndAdvanceUserId(0), 0);
    EXPECT_EQ(idManager.getNextUserId(), 0);

    EXPECT_EQ(idManager.getAndAdvanceChannelId(0), 0);
    EXPECT_EQ(idManager.getNextChannelId(), 0);

    EXPECT_EQ(idManager.getAndAdvanceCommentId(0), 0);
    EXPECT_EQ(idManager.getNextCommentId(), 0);

    EXPECT_EQ(idManager.getAndAdvanceContentId(0), 0);
    EXPECT_EQ(idManager.getNextContentId(), 0);

    EXPECT_EQ(idManager.getAndAdvanceInteractionId(0), 0);
    EXPECT_EQ(idManager.getNextInteractionId(), 0);

    EXPECT_EQ(idManager.getAndAdvanceWatchId(0), 0);
    EXPECT_EQ(idManager.getNextWatchId(), 0);
}
TEST_F(IdBatchManagerTest, SimpleIncrementWorks) {
    EXPECT_EQ(idManager.getAndAdvanceUserId(), 0);
    EXPECT_EQ(idManager.getAndAdvanceUserId(), 1);
    EXPECT_EQ(idManager.getAndAdvanceUserId(), 2);
    EXPECT_EQ(idManager.getNextUserId(), 3);

    EXPECT_EQ(idManager.getAndAdvanceChannelId(), 0);
    EXPECT_EQ(idManager.getAndAdvanceChannelId(), 1);
    EXPECT_EQ(idManager.getAndAdvanceChannelId(), 2);
    EXPECT_EQ(idManager.getNextChannelId(), 3);

    EXPECT_EQ(idManager.getAndAdvanceCommentId(), 0);
    EXPECT_EQ(idManager.getAndAdvanceCommentId(), 1);
    EXPECT_EQ(idManager.getAndAdvanceCommentId(), 2);
    EXPECT_EQ(idManager.getNextCommentId(), 3);

    EXPECT_EQ(idManager.getAndAdvanceContentId(), 0);
    EXPECT_EQ(idManager.getAndAdvanceContentId(), 1);
    EXPECT_EQ(idManager.getAndAdvanceContentId(), 2);
    EXPECT_EQ(idManager.getNextContentId(), 3);

    EXPECT_EQ(idManager.getAndAdvanceInteractionId(), 0);
    EXPECT_EQ(idManager.getAndAdvanceInteractionId(), 1);
    EXPECT_EQ(idManager.getAndAdvanceInteractionId(), 2);
    EXPECT_EQ(idManager.getNextInteractionId(), 3);

    EXPECT_EQ(idManager.getAndAdvanceWatchId(), 0);
    EXPECT_EQ(idManager.getAndAdvanceWatchId(), 1);
    EXPECT_EQ(idManager.getAndAdvanceWatchId(), 2);
    EXPECT_EQ(idManager.getNextWatchId(), 3);

}
TEST_F(IdBatchManagerTest, NonSimpleIncrementWorks) {
    EXPECT_EQ(idManager.getAndAdvanceUserId(42), 0);
    EXPECT_EQ(idManager.getAndAdvanceUserId(42), 42);
    EXPECT_EQ(idManager.getAndAdvanceUserId(42), 84);
    EXPECT_EQ(idManager.getNextUserId(), 126);

    EXPECT_EQ(idManager.getAndAdvanceChannelId(1000), 0);
    EXPECT_EQ(idManager.getAndAdvanceChannelId(1000), 1000);
    EXPECT_EQ(idManager.getAndAdvanceChannelId(1000), 2000);
    EXPECT_EQ(idManager.getNextChannelId(), 3000);

    EXPECT_EQ(idManager.getAndAdvanceCommentId(500), 0);
    EXPECT_EQ(idManager.getAndAdvanceCommentId(500), 500);
    EXPECT_EQ(idManager.getAndAdvanceCommentId(500), 1000);
    EXPECT_EQ(idManager.getNextCommentId(), 1500);

    EXPECT_EQ(idManager.getAndAdvanceContentId(12345), 0);
    EXPECT_EQ(idManager.getAndAdvanceContentId(12345), 12345);
    EXPECT_EQ(idManager.getAndAdvanceContentId(12345), 24690);
    EXPECT_EQ(idManager.getNextContentId(), 37035);

    EXPECT_EQ(idManager.getAndAdvanceInteractionId(99999), 0);
    EXPECT_EQ(idManager.getAndAdvanceInteractionId(99999), 99999);
    EXPECT_EQ(idManager.getAndAdvanceInteractionId(99999), 199998);
    EXPECT_EQ(idManager.getNextInteractionId(), 299997);

    EXPECT_EQ(idManager.getAndAdvanceWatchId(314159), 0);
    EXPECT_EQ(idManager.getAndAdvanceWatchId(314159), 314159);
    EXPECT_EQ(idManager.getAndAdvanceWatchId(314159), 628318);
    EXPECT_EQ(idManager.getNextWatchId(), 942477);
}
TEST_F(IdBatchManagerTest, Reset){
    idManager.getAndAdvanceUserId(42);
    EXPECT_NE(idManager.getNextUserId(), 0);
    idManager.getAndAdvanceChannelId(42);
    EXPECT_NE(idManager.getNextChannelId(), 0);
    idManager.getAndAdvanceCommentId(42);
    EXPECT_NE(idManager.getNextCommentId(), 0);
    idManager.getAndAdvanceContentId(42);
    EXPECT_NE(idManager.getNextContentId(), 0);
    idManager.getAndAdvanceInteractionId(42);
    EXPECT_NE(idManager.getNextInteractionId(), 0);
    idManager.getAndAdvanceWatchId(42);
    EXPECT_NE(idManager.getNextWatchId(), 0);
    idManager.reset();
    EXPECT_EQ(idManager.getNextUserId(), 0);
    EXPECT_EQ(idManager.getNextChannelId(), 0);
    EXPECT_EQ(idManager.getNextCommentId(), 0);
    EXPECT_EQ(idManager.getNextContentId(), 0);
    EXPECT_EQ(idManager.getNextInteractionId(), 0);
    EXPECT_EQ(idManager.getNextWatchId(), 0);
}
TEST_F(IdBatchManagerTest, HandlesLargeIncrement) {
    int startUser = idManager.getAndAdvanceUserId(100'000'000);
    EXPECT_EQ(startUser, 0);
    EXPECT_EQ(idManager.getNextUserId(), 100'000'000);

    int startChannel = idManager.getAndAdvanceChannelId(100'000'000);
    EXPECT_EQ(startChannel, 0);
    EXPECT_EQ(idManager.getNextChannelId(), 100'000'000);

    int startComment = idManager.getAndAdvanceCommentId(100'000'000);
    EXPECT_EQ(startComment, 0);
    EXPECT_EQ(idManager.getNextCommentId(), 100'000'000);

    int startContent = idManager.getAndAdvanceContentId(100'000'000);
    EXPECT_EQ(startContent, 0);
    EXPECT_EQ(idManager.getNextContentId(), 100'000'000);

    int startInteraction = idManager.getAndAdvanceInteractionId(100'000'000);
    EXPECT_EQ(startInteraction, 0);
    EXPECT_EQ(idManager.getNextInteractionId(), 100'000'000);

    int startWatch = idManager.getAndAdvanceWatchId(100'000'000);
    EXPECT_EQ(startWatch, 0);
    EXPECT_EQ(idManager.getNextWatchId(), 100'000'000);
}

class RandomGeneratorTest : public ::testing::Test {
    protected:
        IdBatchManager idManager;
        RandomGenerator generator;
    
        RandomGeneratorTest() : generator(idManager) {}
    
        Relations::UserArray users;
    };
TEST_F(RandomGeneratorTest, AddRandomUserBasicProperties) {
    const int numUsers = 100;
    generator.addRandomUser(users, numUsers);

    // Check the size
    EXPECT_EQ(users.size(), numUsers);

    // Check IDs sequential from 0
    for (int i = 0; i < numUsers; ++i) {
        EXPECT_EQ(users.userIds[i], i);
    }

    // Check userChannelIds are all -1
    for (int i = 0; i < numUsers; ++i) {
        EXPECT_EQ(users.userChannelIds[i], -1);
    }

    // Check userGenders are within enum range (0 or 1)
    for (int i = 0; i < numUsers; ++i) {
        auto gender = static_cast<unsigned char>(users.userGenders[i]);
        EXPECT_TRUE(gender == 0 || gender == 1);
    }

    // Check userAges between 13 and 100
    for (int i = 0; i < numUsers; ++i) {
        EXPECT_GE(users.userAges[i], 13);
        EXPECT_LE(users.userAges[i], 100);
    }

    // Check userOccupations within valid range (0..143)
    for (int i = 0; i < numUsers; ++i) {
        EXPECT_GE(users.userOccupations[i], 0);
        EXPECT_LE(users.userOccupations[i], 143);
    }

    // Check userLocations within valid range (0..60)
    for (int i = 0; i < numUsers; ++i) {
        EXPECT_GE(users.userLocations[i], 0);
        EXPECT_LE(users.userLocations[i], 60);
    }

    // Check userEducations reasonable — max 16 (as per binomial dist) + check min bound
    for (int i = 0; i < numUsers; ++i) {
        EXPECT_GE(users.userEducations[i], 0);
        EXPECT_LE(users.userEducations[i], 16);
    }

    // Check userLanguages indicator byte
    for (int i = 0; i < numUsers; ++i) {
        uint8_t indicator = users.userLanguages[i][3];
        EXPECT_TRUE(indicator == 1 || indicator == 2 || indicator == 3)
            << "Invalid language indicator value: " << static_cast<int>(indicator)
            << " at index " << i;
    }
}
TEST_F(RandomGeneratorTest, AddRandomUserCumulativeBehavior) {
    const int numUsers1 = 50;
    const int numUsers2 = 70;

    generator.addRandomUser(users, numUsers1);
    EXPECT_EQ(users.size(), numUsers1);

    generator.addRandomUser(users, numUsers2);
    EXPECT_EQ(users.size(), numUsers1 + numUsers2);

    // IDs should continue sequentially
    for (int i = 0; i < numUsers1 + numUsers2; ++i) {
        EXPECT_EQ(users.userIds[i], i);
    }
}
TEST_F(RandomGeneratorTest, HandlesNegativeIncrement){
    const int negativeUsers = -12;
    EXPECT_ANY_THROW(generator.addRandomUser(users, negativeUsers));
    EXPECT_EQ(users.size(), 0);
}
TEST_F(RandomGeneratorTest, HandlesZeroIncrement){
    const int zeroUsers = 0;
    EXPECT_ANY_THROW(generator.addRandomUser(users, zeroUsers));
    EXPECT_EQ(users.size(), 0);
}

class RandomChannelGeneratorTest : public ::testing::Test {
protected:
    IdBatchManager idManager;
    RandomGenerator generator;

    RandomChannelGeneratorTest() : generator(idManager) {}

    Relations::UserArray users;
    Relations::ChannelArray channels;

    void SetUp() override {
        // Prepare 100 users
        generator.addRandomUser(users, 100);
    }
};
TEST_F(RandomChannelGeneratorTest, InvalidArgumentsThrow) {
    EXPECT_THROW(generator.addRandomChannel(channels, users, 0.0f, 20240101), std::invalid_argument);
    EXPECT_THROW(generator.addRandomChannel(channels, users, 1.5f, 20240101), std::invalid_argument);
}
TEST_F(RandomChannelGeneratorTest, NoAvailableUsersDoesNothing) {
    // Make sure every user has a channel
    Relations::UserArray noUsers;
    EXPECT_THROW(generator.addRandomChannel(channels, noUsers, 0.5f, 20240101), std::invalid_argument);
}
TEST_F(RandomChannelGeneratorTest, ChannelsCreatedWithCorrectValues) {
    const float creationRatio = 0.5f;
    const int creationDate = 20240101;
    size_t expectedChannels = static_cast<size_t>((users.size()) * creationRatio);

    generator.addRandomChannel(channels, users, creationRatio, creationDate);

    EXPECT_EQ(channels.size(), expectedChannels);

    // Para validar unicidade de canais e consistência das ligações
    std::set<int64_t> usedOwners;
    std::set<int64_t> usedChannels;

    for (size_t i = 0; i < channels.size(); ++i) {
        int64_t channelId = channels.channelIds[i];
        int64_t ownerId = channels.channelOwnerIds[i];

        // O dono precisa existir
        EXPECT_GE(ownerId, 0);
        EXPECT_LE(ownerId, static_cast<int64_t>(users.size()));
        EXPECT_GE(channelId, 0);

        // Esse dono não pode já ter outro canal (unicidade)
        EXPECT_TRUE(usedOwners.find(ownerId) == usedOwners.end()) << "User " << ownerId << " already has a channel";
        usedOwners.insert(ownerId);

        // O channelId precisa ser único também
        EXPECT_TRUE(usedChannels.find(channelId) == usedChannels.end()) << "Channel ID " << channelId << " reused";
        usedChannels.insert(channelId);

        // O usuário deve apontar de volta para esse canal
        EXPECT_EQ(users.userChannelIds[ownerId], channelId);

        // Creation date correto
        EXPECT_EQ(channels.channelCreationDates[i], creationDate);

        // Linguagem dentro do limite do user
        unsigned char langIndicator = users.userLanguages[ownerId][3];
        EXPECT_GE(channels.channelLanguages[i], 1);
        EXPECT_LE(channels.channelLanguages[i], langIndicator);

        // Categoria válida
        EXPECT_GE(channels.channelCategories[i], 0);
        EXPECT_LE(channels.channelCategories[i], 14);

        // Localização batendo com a do user
        EXPECT_EQ(channels.channelLocations[channelId], users.userLocations[ownerId]);
    }

    // Nenhum outro usuário sem canal foi modificado indevidamente
    for (size_t i = 0; i < users.size(); ++i) {
        if (usedOwners.find(users.userIds[i]) == usedOwners.end()) {
            EXPECT_EQ(users.userChannelIds[i], -1);
        }
    }
}
TEST_F(RandomChannelGeneratorTest, ZeroRatioDoesNothing) {
    EXPECT_THROW(generator.addRandomChannel(channels, users, 0.0f, 20240101), std::invalid_argument);
}
TEST_F(RandomChannelGeneratorTest, FullRatioCreatesAllAvailableChannels) {
    const float creationRatio = 1.0f;
    const int creationDate = 20240101;
    size_t expectedChannels = static_cast<size_t>((users.size()));

    generator.addRandomChannel(channels, users, creationRatio, creationDate);

    EXPECT_EQ(channels.size(), expectedChannels);

    // All users should now have a non -1 channel id
    for (size_t i = 0; i < users.size(); ++i) {
        EXPECT_NE(users.userChannelIds[i], -1);
    }
}

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}