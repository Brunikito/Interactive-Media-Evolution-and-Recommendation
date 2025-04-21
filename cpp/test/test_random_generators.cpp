#include <gtest/gtest.h>
#include "../include/random_generators.h"
#include "../include/relation_properties.h"
#include "../include/aligned_alocator.h"
#include "../include/relation_properties.h"
#include <vector>
#include <unordered_set>

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
TEST_F(RandomGeneratorTest, AddRandomUserSingle) {
    generator.addRandomUser(users, 1);
    EXPECT_EQ(users.size(), 1);
    EXPECT_EQ(users.userIds[0], 0);
}
TEST_F(RandomGeneratorTest, AddRandomUserSIMDEdgeCases) {
    generator.addRandomUser(users, 31);
    EXPECT_EQ(users.size(), 31);
    users.resize(0);
    idManager.reset();

    generator.addRandomUser(users, 32);
    EXPECT_EQ(users.size(), 32);
    users.resize(0);
    idManager.reset();

    generator.addRandomUser(users, 33);
    EXPECT_EQ(users.size(), 33);
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
        EXPECT_TRUE(channels.channelLanguages[i] == users.userLanguages[ownerId][0] || channels.channelLanguages[i] == users.userLanguages[ownerId][1] || channels.channelLanguages[i] == users.userLanguages[ownerId][2]);

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
TEST_F(RandomChannelGeneratorTest, AddChannelWhenFull) {
    generator.addRandomChannel(channels, users, 1.0, 0);
    EXPECT_THROW(generator.addRandomChannel(channels, users, 0.5, 0), std::invalid_argument);
}
TEST_F(RandomChannelGeneratorTest, AddChannelAlmostFull) {
    generator.addRandomChannel(channels, users, 0.999f, 0);
    EXPECT_NE(channels.size(), 0);
}

class RandomSubsGeneratorTest : public ::testing::Test {
    protected:
    IdBatchManager idManager;
    RandomGenerator generator;

    RandomSubsGeneratorTest() : generator(idManager) {}

    Relations::UserArray users;
    Relations::ChannelArray channels;
    Relations::UserSubChannelArray subs;

    void SetUp() override {
        // Prepare 200 users
        generator.addRandomUser(users, 200);
        // Prepare 100 channels
        generator.addRandomChannel(channels, users, 0.5, 0);
    }
};
TEST_F(RandomSubsGeneratorTest, InvalidArgumentsThrow){
    EXPECT_ANY_THROW(generator.addRandomSubs(subs, channels, users, -1));
    EXPECT_ANY_THROW(generator.addRandomSubs(subs, channels, users, 0));
    EXPECT_ANY_THROW(generator.addRandomSubs(subs, channels, users, 2));
    Relations::UserArray emptyUsers;
    Relations::ChannelArray emptyChannels;
    EXPECT_ANY_THROW(generator.addRandomSubs(subs, channels, emptyUsers, 0.5));
    EXPECT_ANY_THROW(generator.addRandomSubs(subs, emptyChannels, users, 0.5));
    EXPECT_ANY_THROW(generator.addRandomSubs(subs, emptyChannels, emptyUsers, 0.5));
}
TEST_F(RandomSubsGeneratorTest, SingleInput) {
    IdBatchManager idManagerSingleInput;
    Relations::UserSubChannelArray singleSub;
    Relations::UserArray singleUser;
    Relations::ChannelArray singleChannel;
    RandomGenerator generatorSingleInput(idManagerSingleInput); 
    generatorSingleInput.addRandomUser(singleUser, 1); 
    generatorSingleInput.addRandomChannel(singleChannel, singleUser, 1, 0); 
    generatorSingleInput.addRandomSubs(singleSub, singleChannel, singleUser, 1);
    EXPECT_EQ(singleSub.sizeChannels(), 1);
    EXPECT_EQ(singleSub.sizeUsers(), 1);
    EXPECT_EQ(singleSub.userIdSubscriptions[0]->size, 1);
    EXPECT_EQ(singleSub.channelIdSubscribers[0]->size, 1);
    EXPECT_EQ(singleSub.userIdSubscriptions[0]->head->value, 0);
    EXPECT_EQ(singleSub.channelIdSubscribers[0]->head->value, 0);
}
TEST_F(RandomSubsGeneratorTest, ValidSize){
    generator.addRandomSubs(subs, channels, users, 0.5);
    EXPECT_EQ(subs.sizeChannels(), channels.size());
    EXPECT_EQ(subs.sizeUsers(), users.size());
    int totalAlocatedUsers = 0;
    for (int i = 0; i <subs.sizeUsers(); i++){
        if (subs.userIdSubscriptions[i]) {
            totalAlocatedUsers++;
        }
    }
    EXPECT_LE(totalAlocatedUsers, channels.size());
    int totalAlocatedChannels = 0;
    for (int i = 0; i <subs.sizeChannels(); i++){
        if (subs.channelIdSubscribers[i]) {
            totalAlocatedChannels++;
        }
    }
    EXPECT_LE(totalAlocatedChannels, users.size());
}
TEST_F(RandomSubsGeneratorTest, BidirectionalListConsistency) {
    generator.addRandomSubs(subs, channels, users, 1.0);

    // Para cada usuário
    for (int64_t userId = 0; userId < users.size(); userId++) {
        auto* userList = subs.userIdSubscriptions[userId];
        if (!userList) continue;

        // Para cada canal que o usuário está inscrito
        auto* node = userList->head;
        while (node) {
            int64_t channelId = node->value;

            // A lista do canal deve conter o userId
            auto* channelList = subs.channelIdSubscribers[channelId];
            ASSERT_NE(channelList, nullptr) << "Canal " << channelId << " não possui lista de inscritos.";
            bool found = channelList->search(userId);
            EXPECT_TRUE(found) << "Usuário " << userId << " está inscrito no canal " << channelId << ", mas não foi encontrado na lista de inscritos do canal.";
            node = node->nextNode;
        }
    }

    // Para cada canal
    for (int64_t channelId = 0; channelId < channels.size(); channelId++) {
        auto* channelList = subs.channelIdSubscribers[channelId];
        if (!channelList) continue;

        // Para cada usuário inscrito no canal
        auto* node = channelList->head;
        while (node) {
            int64_t userId = node->value;

            // A lista do usuário deve conter o channelId
            auto* userList = subs.userIdSubscriptions[userId];
            ASSERT_NE(userList, nullptr) << "Usuário " << userId << " não possui lista de inscrições.";
            bool found = userList->search(channelId);
            EXPECT_TRUE(found) << "Canal " << channelId << " possui usuário " << userId << " na lista de inscritos, mas o usuário não está inscrito no canal.";
            node = node->nextNode;
        }
    }
}
TEST_F(RandomSubsGeneratorTest, NoDuplicateSubscriptions) {
    generator.addRandomSubs(subs, channels, users, 1.0);

    // Para cada usuário, checa se não há canais repetidos
    for (int64_t userId = 0; userId < users.size(); userId++) {
        auto* userList = subs.userIdSubscriptions[userId];
        if (!userList) continue;

        std::unordered_set<int64_t> seenChannels;
        auto* node = userList->head;
        while (node) {
            int64_t channelId = node->value;
            auto result = seenChannels.insert(channelId);
            EXPECT_TRUE(result.second) << "Usuário " << userId << " está inscrito mais de uma vez no canal " << channelId;
            node = node->nextNode;
        }
    }

    // Para cada canal, checa se não há usuários repetidos
    for (int64_t channelId = 0; channelId < channels.size(); channelId++) {
        auto* channelList = subs.channelIdSubscribers[channelId];
        if (!channelList) continue;

        std::unordered_set<int64_t> seenUsers;
        auto* node = channelList->head;
        while (node) {
            int64_t userId = node->value;
            auto result = seenUsers.insert(userId);
            EXPECT_TRUE(result.second) << "Canal " << channelId << " contém o usuário " << userId << " mais de uma vez";
            node = node->nextNode;
        }
    }
}
TEST_F(RandomSubsGeneratorTest, MaxUserRatioOneUserOneChannel) {
    Relations::UserArray singleUser;
    Relations::ChannelArray singleChannel;
    Relations::UserSubChannelArray singleSubs;
    IdBatchManager localManager;
    RandomGenerator localGen(localManager);

    localGen.addRandomUser(singleUser, 1);
    localGen.addRandomChannel(singleChannel, singleUser, 1.0, 0);
    localGen.addRandomSubs(singleSubs, singleChannel, singleUser, 1.0);

    EXPECT_EQ(singleSubs.sizeChannels(), 1);
    EXPECT_EQ(singleSubs.sizeUsers(), 1);
    EXPECT_EQ(singleSubs.userIdSubscriptions[0]->size, 1);
    EXPECT_EQ(singleSubs.channelIdSubscribers[0]->size, 1);
}
TEST_F(RandomSubsGeneratorTest, AllUsersAlreadyHaveChannels) {
    generator.addRandomChannel(channels, users, 1, 0);
    Relations::UserSubChannelArray localSubs;
    EXPECT_NO_THROW(generator.addRandomSubs(localSubs, channels, users, 1.0));
}

class RandomContentGeneratorTest : public ::testing::Test {
    protected:
        IdBatchManager idManager;
        RandomGenerator generator;
    
        RandomContentGeneratorTest() : generator(idManager) {}
    
        Relations::ChannelArray channels;
        Relations::ContentArray content;
    
        void SetUp() override {
            // Gerar 100 canais (sem usuários, pois só os canais são necessários aqui)
            Relations::UserArray dummyUsers;
            generator.addRandomUser(dummyUsers, 100); // usuários só para gerar canais
            generator.addRandomChannel(channels, dummyUsers, 1.0, 0);
        }
};
TEST_F(RandomContentGeneratorTest, InvalidArgumentsThrow) {
    Relations::ContentArray content;
    Relations::ChannelArray emptyChannels;

    EXPECT_ANY_THROW(generator.addRandomContent(content, emptyChannels, 0.5, 0));
    EXPECT_ANY_THROW(generator.addRandomContent(content, channels, 0, 0));
    EXPECT_ANY_THROW(generator.addRandomContent(content, channels, -0.1, 0));
    EXPECT_ANY_THROW(generator.addRandomContent(content, channels, 1.1, 0));
}
TEST_F(RandomContentGeneratorTest, CorrectNumberGenerated) {
    Relations::ContentArray content;
    generator.addRandomContent(content, channels, 1.0, 12345);

    EXPECT_EQ(content.size(), channels.size());
    for (size_t i = 0; i < content.size(); i++) {
        EXPECT_GE(content.contentIds[i], 0);
        EXPECT_GE(content.contentChannelIds[i], 0);
        EXPECT_LT(content.contentChannelIds[i], channels.size());
    }
}
TEST_F(RandomContentGeneratorTest, CreationDateApplied) {
    Relations::ContentArray content;
    int creationDate = 54321;
    generator.addRandomContent(content, channels, 1.0, creationDate);

    for (size_t i = 0; i < content.size(); i++) {
        EXPECT_EQ(content.contentPubDateTimes[i], creationDate);
    }
}
TEST_F(RandomContentGeneratorTest, DefaultCountsAreZero) {
    Relations::ContentArray content;
    generator.addRandomContent(content, channels, 1.0, 0);

    for (size_t i = 0; i < content.size(); i++) {
        EXPECT_EQ(content.contentLikeCounts[i], 0);
        EXPECT_EQ(content.contentDislikeCounts[i], 0);
        EXPECT_EQ(content.contentViewCounts[i], 0);
        EXPECT_EQ(content.contentCommentCounts[i], 0);
    }
}
TEST_F(RandomContentGeneratorTest, FullVideoIdsDefault) {
    Relations::ContentArray content;
    generator.addRandomContent(content, channels, 1.0, 0);

    for (size_t i = 0; i < content.size(); i++) {
        EXPECT_EQ(content.fullvideoIds[i], -1);
    }
}
TEST_F(RandomContentGeneratorTest, DistributesTypesAndStatuses) {
    Relations::ContentArray content;
    generator.addRandomContent(content, channels, 1.0, 0);

    std::set<uint8_t> typesFound;
    std::set<uint8_t> statusesFound;

    for (size_t i = 0; i < content.size(); i++) {
        typesFound.insert(content.contentTypes[i]);
        statusesFound.insert(content.contentStatuses[i]);
    }

    EXPECT_GE(typesFound.size(), 2) << "Esperado pelo menos dois tipos diferentes de conteúdo.";
    EXPECT_GE(statusesFound.size(), 2) << "Esperado pelo menos dois statuses diferentes.";
}
TEST_F(RandomContentGeneratorTest, ContentTagsHaveCorrectUniqueCount) {
    generator.addRandomContent(content, channels, 1.0, 0);

    for (size_t i = 0; i < content.size(); ++i) {
        uint8_t tag1 = content.contentTags[i][0];
        uint8_t tag2 = content.contentTags[i][1];
        uint8_t tag3 = content.contentTags[i][2];

        // Calcula a quantidade de tags únicas de acordo com a regra definida
        uint8_t calculatedUniqueCount = 3; // Assume 3 únicas por padrão

        if (tag1 == tag2) {
            calculatedUniqueCount = 1; // Todas as tags são iguais
        } else if (tag1 == tag3 || tag2 == tag3) {
            calculatedUniqueCount = 2; // Duas tags são iguais, uma diferente
        } else {
            calculatedUniqueCount = 3; // Todas as tags são diferentes
        }

        uint8_t declaredUniqueCount = content.contentTags[i][3];

        // Verifica se o número calculado de tags únicas corresponde ao declarado
        EXPECT_EQ(calculatedUniqueCount, declaredUniqueCount)
            << "Content ID " << content.contentIds[i]
            << " declarou " << static_cast<int>(declaredUniqueCount)
            << " tags únicas, mas foram encontradas " << static_cast<int>(calculatedUniqueCount);
    }
}
TEST_F(RandomContentGeneratorTest, CreationRatioEdgeCases) {
    EXPECT_NO_THROW(generator.addRandomContent(content, channels, 0.999f, 0));
    EXPECT_EQ(content.size(), static_cast<size_t>(channels.size() * 0.999f));
}
TEST_F(RandomContentGeneratorTest, CreationRatioFull){
    EXPECT_NO_THROW(generator.addRandomContent(content, channels, 1.0f, 0));
    EXPECT_EQ(content.size(), channels.size());
}
TEST_F(RandomContentGeneratorTest, ContentDurationsWithinLimits) {
    Relations::ContentArray content;
    generator.addRandomContent(content, channels, 1.0f, 0);

    for (size_t i = 0; i < content.size(); i++) {
        auto type = content.contentTypes[i];
        auto dur = content.contentDurations[i];
        if (type == Relations::ContentType::VIDEO)
            EXPECT_LE(dur, 3600);
        else if (type == Relations::ContentType::SHORT)
            EXPECT_LE(dur, 600); // porque beta(4,2)*60 pode variar
        else if (type == Relations::ContentType::LIVE)
            EXPECT_LE(dur, 18000);
    }
}

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}