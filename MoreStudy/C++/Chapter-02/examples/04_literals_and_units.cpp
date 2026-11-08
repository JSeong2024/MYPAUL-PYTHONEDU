#include <iostream>

int main() {
    int sampling_rate_hz{1'000};
    int status_mask{0b0000'0101};
    int color_value{0xFF};
    double distance_m{2.5};

    std::cout << "Sampling rate: " << sampling_rate_hz << " Hz\n";
    std::cout << "Status mask: " << status_mask << '\n';
    std::cout << "Color value: " << color_value << '\n';
    std::cout << "Distance: " << distance_m << " m\n";
}
