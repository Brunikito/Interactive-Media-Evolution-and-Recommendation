cmake_minimum_required(VERSION 3.10)
project(RandomGeneratorsTest)

enable_testing()

find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

add_executable(test_random_generators test_random_generators.cpp)
target_link_libraries(test_random_generators ${GTEST_LIBRARIES} pthread)

add_test(NAME RandomGeneratorsTest COMMAND test_random_generators)