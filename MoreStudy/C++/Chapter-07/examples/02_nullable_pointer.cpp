#include <iostream>

void print_temperature(const int* reading) {
    if (reading == nullptr) {
        std::cout << "No sensor reading\n";
        return;
    }
    std::cout << "Sensor: " << *reading << " C\n";
}

int main() {
    const int measured{23};
    print_temperature(&measured);
    print_temperature(nullptr);
}
