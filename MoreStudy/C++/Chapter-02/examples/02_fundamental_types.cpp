#include <print>
#include <string>

int main() {
    using std::println;

    bool ready{true};
    char channel{'A'};
    int sample_count{12};
    double temperature_c{23.75};
    std::string sensor_name{"Temperature-01"};

    println("Sensor: {}", sensor_name);
    println("Channel: {}", channel);
    println("Ready: {}", ready);
    println("Samples: {}", sample_count);
    println("Temperature: {:.2f} C", temperature_c);
}
