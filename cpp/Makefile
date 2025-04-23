# Compilador e flags
CXX = g++
CXXFLAGS = -std=c++20 -I include -I utils -I C:/Dev/pcg-cpp-0.98/include -I$(GTEST_INCLUDE)
OPTFLAGS = -O3 -fopenmp -mavx2 -march=native

# GoogleTest paths
GTEST_INCLUDE = C:/Dev/googletest/googletest/include
GTEST_LIB = C:/Dev/googletest/build/lib

# Diretórios
SRC_DIR = src
TEST_DIR = test
BUILD_DIR = build
UTILS_DIR = utils

# Executáveis
MAIN_EXE = $(BUILD_DIR)/main.exe
TEST_RECOMMENDATOR_EXE = $(BUILD_DIR)/test_recommendator.exe
TEST_RANDOM_EXE = $(BUILD_DIR)/test_random_generators.exe

# Targets padrão
all: $(MAIN_EXE) $(TEST_RECOMMENDATOR_EXE) $(TEST_RANDOM_EXE)

# Dependências comuns
COMMON_OBJS = \
	$(BUILD_DIR)/random_generators.o \
	$(BUILD_DIR)/fast_copy.o \
	$(BUILD_DIR)/random_utils.o \
	$(BUILD_DIR)/timer.o \
	$(BUILD_DIR)/recommendator.o

# Main
$(MAIN_EXE): $(BUILD_DIR)/main.o $(COMMON_OBJS)
	$(CXX) $(OPTFLAGS) $^ -o $@

$(BUILD_DIR)/main.o: $(SRC_DIR)/main.cpp
	$(CXX) $(OPTFLAGS) $(CXXFLAGS) -c $< -o $@

# Teste: random_generators
$(TEST_RANDOM_EXE): $(BUILD_DIR)/test_random_generators.o $(COMMON_OBJS)
	$(CXX) $^ -L$(GTEST_LIB) $(OPTFLAGS) -lgtest -lgtest_main -pthread -o $@

$(BUILD_DIR)/test_random_generators.o: $(TEST_DIR)/test_random_generators.cpp
	$(CXX) $(CXXFLAGS) $(OPTFLAGS) -c $< -o $@

# Teste: recommendator
$(TEST_RECOMMENDATOR_EXE): $(BUILD_DIR)/test_recommendator.o $(COMMON_OBJS)
	$(CXX) $^ -L$(GTEST_LIB) $(OPTFLAGS) -lgtest -lgtest_main -pthread -o $@

$(BUILD_DIR)/test_recommendator.o: $(TEST_DIR)/test_recommendator.cpp
	$(CXX) $(CXXFLAGS) $(OPTFLAGS) -c $< -o $@

# Objetos auxiliares
$(BUILD_DIR)/random_generators.o: $(SRC_DIR)/random_generators.cpp include/random_generators.h
	$(CXX) $(OPTFLAGS) $(CXXFLAGS) -c $< -o $@

$(BUILD_DIR)/fast_copy.o: $(UTILS_DIR)/fast_copy.cpp
	$(CXX) $(OPTFLAGS) $(CXXFLAGS) -c $< -o $@

$(BUILD_DIR)/random_utils.o: $(UTILS_DIR)/random_utils.cpp include/random_utils.h
	$(CXX) $(OPTFLAGS) $(CXXFLAGS) -c $< -o $@

$(BUILD_DIR)/timer.o: $(UTILS_DIR)/timer.cpp
	$(CXX) $(OPTFLAGS) $(CXXFLAGS) -c $< -o $@

$(BUILD_DIR)/recommendator.o: $(SRC_DIR)/recommendator.cpp include/recommendator.h
	$(CXX) $(OPTFLAGS) $(CXXFLAGS) -c $< -o $@

# Limpar
clean:
	del /Q $(BUILD_DIR)\*

# Criação automática do diretório build (Windows CMD)
$(shell if not exist $(BUILD_DIR) mkdir $(BUILD_DIR))