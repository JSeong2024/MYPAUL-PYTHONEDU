#include <iostream>
#include <string>

int main() {
    int sample_count{12};
    bool connected{true};
    std::string sensor_name{"Sensor-A"};

    std::cout << std::boolalpha;
    std::cout << "Sensor: " << sensor_name << '\n';
    std::cout << "Samples: " << sample_count << '\n';
    std::cout << "Connected: " << connected << '\n';

    sample_count = 15;
    std::cout << "Updated samples: " << sample_count << '\n';
}
