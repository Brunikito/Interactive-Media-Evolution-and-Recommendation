# Compilador e flags
CXX = g++
CXXFLAGS = -std=c++20 -I include -I utils -I C:/Dev/pcg-cpp-0.98/include
OPTFLAGS = -O3 -fopenmp -mavx2

# GoogleTest paths
GTEST_INCLUDE = C:/Dev/googletest/googletest/include
GTEST_LIB = C:/Dev/googletest/build/lib

# Diretórios
SRC_DIR = src
TEST_DIR = test
BUILD_DIR = build
UTILS_DIR = utils

# Arquivos objeto principais
MAIN_OBJS = $(BUILD_DIR)/main.o $(BUILD_DIR)/random_generators.o $(BUILD_DIR)/fast_copy.o $(BUILD_DIR)/random_utils.o $(BUILD_DIR)/timer.o $(BUILD_DIR)/recommendator.o
# Arquivos objeto para os testes
TEST_OBJS = $(BUILD_DIR)/test_random_generators.o $(BUILD_DIR)/random_generators.o $(BUILD_DIR)/fast_copy.o $(BUILD_DIR)/random_utils.o $(BUILD_DIR)/timer.o $(BUILD_DIR)/recommendator.o

# Executáveis
MAIN_EXE = $(BUILD_DIR)/main.exe
TEST_EXE = $(BUILD_DIR)/test_runner.exe

# Target padrão
all: $(MAIN_EXE) $(TEST_EXE)

# Compilar executável principal
$(MAIN_EXE): $(MAIN_OBJS)
	$(CXX) $(OPTFLAGS) $^ -o $@

# Compilar testes
$(TEST_EXE): $(TEST_OBJS)
	$(CXX) $^ -I$(GTEST_INCLUDE) -L$(GTEST_LIB) $(OPTFLAGS) -lgtest -lgtest_main -pthread -o $@

# Compilar objetos
$(BUILD_DIR)/main.o: $(SRC_DIR)/main.cpp
	$(CXX) $(OPTFLAGS) $(CXXFLAGS) -c $< -o $@

$(BUILD_DIR)/random_generators.o: $(SRC_DIR)/random_generators.cpp include/random_generators.h
	$(CXX) $(OPTFLAGS) $(CXXFLAGS) -c $< -o $@

$(BUILD_DIR)/test_random_generators.o: $(TEST_DIR)/test_random_generators.cpp
	$(CXX) $(CXXFLAGS) -I$(GTEST_INCLUDE) $(OPTFLAGS) -c $< -o $@

# Compilar fast_copy.cpp
$(BUILD_DIR)/fast_copy.o: $(UTILS_DIR)/fast_copy.cpp
	$(CXX) $(OPTFLAGS) $(CXXFLAGS) -c $< -o $@

# Compilar random_utils.cpp
$(BUILD_DIR)/random_utils.o: $(UTILS_DIR)/random_utils.cpp include/random_utils.h
	$(CXX) $(OPTFLAGS) $(CXXFLAGS) -c $< -o $@

# Compilar timer.cpp
$(BUILD_DIR)/timer.o: $(UTILS_DIR)/timer.cpp
	$(CXX) $(OPTFLAGS) $(CXXFLAGS) -c $< -o $@

# Compilar recommendator.cpp
$(BUILD_DIR)/recommendator.o: $(SRC_DIR)/recommendator.cpp include/recommendator.h
	$(CXX) $(OPTFLAGS) $(CXXFLAGS) -c $< -o $@


# Limpar
clean:
	del /Q $(BUILD_DIR)\*

# Criar build/ se não existir
$(shell if not exist $(BUILD_DIR) mkdir $(BUILD_DIR))