#include <iostream>
#include <chrono>
#include <string>
#include <unordered_map>

class TimerManager {
private:
    using Clock = std::chrono::high_resolution_clock;
    using TimePoint = std::chrono::time_point<Clock>;

    std::unordered_map<std::string, TimePoint> startTimes;
    std::unordered_map<std::string, double> durations;

public:
    // Inicia o timer com o nome dado
    void start(const std::string& name) {
        startTimes[name] = Clock::now();
    }

    // Finaliza o timer com o nome dado
    void stop(const std::string& name) {
        auto endTime = Clock::now();
        auto startTime = startTimes[name];
        double duration = std::chrono::duration<double>(endTime - startTime).count();
        durations[name] = duration;
    }

    // Mostra todos os tempos registrados
    void showTimes() const {
        std::cout << "\n=== Tempos registrados ===\n";
        for (const auto& pair : durations) {
            std::cout << pair.first << ": " << pair.second << " segundos\n";
        }
    }
};