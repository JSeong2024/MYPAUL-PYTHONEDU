#include <iomanip>
#include <iostream>

int main() {
    int sample_count{};
    std::cout << "Samples (1-6): " << std::flush;
    if (!(std::cin >> sample_count) ||
        sample_count < 1 || sample_count > 6) {
        std::cerr << "Error: sample count must be between 1 and 6.\n";
        return 1;
    }

    int total{};
    int minimum{100};
    int maximum{0};
    int high_readings{};

    for (int number{1}; number <= sample_count; ++number) {
        bool accepted{false};

        for (int attempt{1}; attempt <= 2; ++attempt) {
            std::cout << "Reading " << number << " (0-100): "
                      << std::flush;

            int reading{};
            if (!(std::cin >> reading)) {
                std::cerr << "Error: integer input required.\n";
                return 1;
            }

            if (reading < 0 || reading > 100) {
                std::cout << "Invalid reading\n";
                continue;
            }

            total += reading;
            if (reading < minimum) {
                minimum = reading;
            }
            if (reading > maximum) {
                maximum = reading;
            }
            if (reading >= 80) {
                ++high_readings;
            }
            accepted = true;
            break;
        }

        if (!accepted) {
            std::cerr << "Error: reading retry limit exceeded.\n";
            return 1;
        }
    }

    const double average{
        static_cast<double>(total) / sample_count
    };

    std::cout << "\n--- Sampling Report ---\n";
    std::cout << "Samples: " << sample_count << '\n';
    std::cout << "Total: " << total << '\n';
    std::cout << "Average: " << std::fixed
              << std::setprecision(2) << average << '\n';
    std::cout << "Minimum: " << minimum << '\n';
    std::cout << "Maximum: " << maximum << '\n';
    std::cout << "High readings (>=80): " << high_readings << '\n';
}
