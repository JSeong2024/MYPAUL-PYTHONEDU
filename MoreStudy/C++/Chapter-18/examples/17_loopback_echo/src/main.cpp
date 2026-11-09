#include "echo.hpp"
#include <iostream>
int main() {
    std::cout << "Echo: " << echo::round_trip("sensor-ready") << '\n';
}
