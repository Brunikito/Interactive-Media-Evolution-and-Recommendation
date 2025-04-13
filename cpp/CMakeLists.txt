cmake_minimum_required(VERSION 3.20)
project(FasterModule)

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(C:/Dev/googletest googletest_build)
set(CMAKE_TOOLCHAIN_FILE "C:/Dev/vcpkg/scripts/buildsystems/vcpkg.cmake"
    CACHE STRING "Vcpkg toolchain file")


find_package(GTest REQUIRED)
find_package(Arrow REQUIRED)
find_package(Parquet REQUIRED)

add_executable(. main.cpp)
add_executable(tests
    tests/test_generators.cpp
    # outros arquivos de teste
)

# Include das libs do GTest
target_include_directories(tests PUBLIC
    ${gtest_SOURCE_DIR}/include
    ${gmock_SOURCE_DIR}/include
)

target_link_libraries(tests
    gtest
    gtest_main
)

enable_testing()
add_test(NAME MeuTeste COMMAND tests)

target_link_libraries(. PRIVATE Arrow::arrow_shared Parquet::parquet_shared)
target_link_libraries(. GTest::gtest GTest::gtest_main)
