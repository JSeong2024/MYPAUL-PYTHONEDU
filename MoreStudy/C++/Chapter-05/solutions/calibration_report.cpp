#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>

// TODO: 측정값에 보정값을 더합니다.
double apply_offset(double reading, double offset) {
    return reading + offset;
}

// TODO: 세 측정값의 평균을 계산합니다.
double average_of_three(double first, double second, double third) {
    return (first + second + third) / 3.0;
}

// TODO: 보정 평균이 35.0 초과이면 "HIGH", 아니면 "NORMAL"을 반환합니다.
std::string status_of(double adjusted_average) {
    return adjusted_average > 35.0 ? "HIGH" : "NORMAL";
}

int main() {
    std::string device;
    std::cout << "Device: " << std::flush;
    if (!std::getline(std::cin, device) || device.empty()) {
        std::cerr << "Error: invalid device name.\n";
        return 1;
    }

    double offset{};
    double first{};
    double second{};
    double third{};
    std::cout << "Offset (C): " << std::flush;
    if (!(std::cin >> offset)) {
        std::cerr << "Error: invalid measurement.\n";
        return 1;
    }
    std::cout << "Reading 1 (C): " << std::flush;
    if (!(std::cin >> first)) {
        std::cerr << "Error: invalid measurement.\n";
        return 1;
    }
    std::cout << "Reading 2 (C): " << std::flush;
    if (!(std::cin >> second)) {
        std::cerr << "Error: invalid measurement.\n";
        return 1;
    }
    std::cout << "Reading 3 (C): " << std::flush;
    if (!(std::cin >> third)) {
        std::cerr << "Error: invalid measurement.\n";
        return 1;
    }

    if (!std::isfinite(offset) || !std::isfinite(first) ||
        !std::isfinite(second) || !std::isfinite(third) ||
        offset < -20.0 || offset > 20.0 ||
        first < -50.0 || first > 150.0 ||
        second < -50.0 || second > 150.0 ||
        third < -50.0 || third > 150.0) {
        std::cerr << "Error: invalid measurement.\n";
        return 1;
    }

    const double raw_average{average_of_three(first, second, third)};
    const double adjusted_average{apply_offset(raw_average, offset)};

    std::cout << std::fixed << std::setprecision(2)
              << "\n--- Calibration Report ---\n"
              << "Device: " << device << '\n'
              << "Offset: " << offset << " C\n"
              << "Average (raw): " << raw_average << " C\n"
              << "Average (adjusted): " << adjusted_average << " C\n"
              << "Status: " << status_of(adjusted_average) << '\n';
}
