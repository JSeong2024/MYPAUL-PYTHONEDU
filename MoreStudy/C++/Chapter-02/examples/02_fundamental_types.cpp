#include <iostream>
#include <string>

int main() {
    char channel{'B'};
    int count{24};
    long long total{1'000'000};
    float ratio{0.5F};
    double temperature_c{23.75};
    std::string label{"Thermal sensor"};

    std::cout << "Channel: " << channel << '\n';
    std::cout << "Count: " << count << '\n';
    std::cout << "Total: " << total << '\n';
    std::cout << "Ratio: " << ratio << '\n';
    std::cout << "Temperature: " << temperature_c << " C\n";
    std::cout << "Label: " << label << '\n';
}
