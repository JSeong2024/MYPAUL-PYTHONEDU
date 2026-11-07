#include <print>
#include <string>
#include <utility>
#include <vector>

struct SensorBatch {
    std::string source;
    std::vector<int> readings;
};

int main() {
    SensorBatch first{"sensor-A", {12, 15, 14}};
    SensorBatch copied = first;
    SensorBatch moved = std::move(first);
    std::println("Copy samples: {}", copied.readings.size());
    std::println("Move samples: {}", moved.readings.size());
}
