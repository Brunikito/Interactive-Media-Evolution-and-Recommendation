cmake_minimum_required(VERSION 3.20)
project(FasterModule)

set(CMAKE_CXX_STANDARD 17)

set(CMAKE_TOOLCHAIN_FILE "C:/Dev/vcpkg/scripts/buildsystems/vcpkg.cmake"
    CACHE STRING "Vcpkg toolchain file")


find_package(GTest REQUIRED)
find_package(Arrow REQUIRED)
find_package(Parquet REQUIRED)

add_executable(. main.cpp)

target_link_libraries(. PRIVATE Arrow::arrow_shared Parquet::parquet_shared)
target_link_libraries(. GTest::gtest GTest::gtest_main)
