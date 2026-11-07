#include <print>

void print_temperature(const int* reading) {
    if (reading == nullptr) {
        std::println("No sensor reading");
        return;
    }
    std::println("Sensor: {} C", *reading);
}

int main() {
    const int measured{23};
    print_temperature(&measured);
    print_temperature(nullptr);
}
